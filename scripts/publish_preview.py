#!/usr/bin/env python3
"""Assemble Tingyi's fixed preview; remote writes require --publish in Actions."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request


REPOSITORY = "yachael/Tingyi"
TAG = "v0.2.9-preview"
TITLE = "Tingyi 0.2.9 — Windows preview"
FILENAME = "Tingyi-Windows-x64-0.2.9-preview.exe"
SIZE = 45324167
SHA256 = "41487fa463d0d239b60dc0209a2244ea8179c971386ab61bec0737dd6d96f663"
PART_SIZE = 4 * 1024 * 1024
PART_COUNT = (SIZE + PART_SIZE - 1) // PART_SIZE
CHECKSUM_NAME = "SHA256SUMS.txt"
CHECKSUM = f"{SHA256}  {FILENAME}\n".encode("ascii")
API_ROOT = f"https://api.github.com/repos/{REPOSITORY}"
RELEASE_URL = f"https://github.com/{REPOSITORY}/releases/tag/{TAG}"


class ReleaseError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    # API credentials must never be forwarded to a redirected host.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def request_bytes(url, *, method="GET", data=None, token=None,
                  content_type=None, limit=5 * 1024 * 1024):
    allowed = ("https://raw.githubusercontent.com/" + REPOSITORY + "/",
               API_ROOT + "/",
               "https://uploads.github.com/repos/" + REPOSITORY + "/")
    if not any(url.startswith(prefix) for prefix in allowed):
        raise ReleaseError("Request is outside the fixed repository endpoints.")
    if token and url.startswith(allowed[0]):
        raise ReleaseError("Raw downloads must be unauthenticated.")
    headers = {"User-Agent": "Tingyi-preview-publisher",
               "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = "Bearer " + token
        headers["X-GitHub-Api-Version"] = "2026-03-10"
    if content_type:
        headers["Content-Type"] = content_type
    attempts = 3 if method == "GET" else 1
    for attempt in range(attempts):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with OPENER.open(req, timeout=120) as response:
                payload = response.read(limit + 1)
                if len(payload) > limit:
                    raise ReleaseError("Server response exceeded its expected size limit.")
                return payload
        except urllib.error.HTTPError as exc:
            if method == "GET" and exc.code in (429, 500, 502, 503, 504) and attempt + 1 < attempts:
                time.sleep(2 ** attempt)
                continue
            # Do not echo response bodies, request headers, or credentials.
            raise ReleaseError(f"GitHub {method} failed with HTTP {exc.code}.") from None
        except (urllib.error.URLError, TimeoutError, OSError):
            if method == "GET" and attempt + 1 < attempts:
                time.sleep(2 ** attempt)
                continue
            raise ReleaseError(f"GitHub {method} failed due to a network error.") from None


def api(path, token, *, method="GET", payload=None):
    if not path.startswith("/") or ".." in path or "#" in path:
        raise ReleaseError("Invalid API path.")
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    result = request_bytes(API_ROOT + path, method=method, data=data, token=token,
                           content_type="application/json" if data is not None else None)
    try:
        return json.loads(result)
    except (ValueError, UnicodeDecodeError):
        raise ReleaseError("GitHub returned invalid JSON.") from None


def valid_commit(value):
    if not value or not re.fullmatch(r"[0-9a-fA-F]{40}", value):
        raise ReleaseError("A complete 40-character commit SHA is required for raw downloads.")
    return value.lower()


def publish_context(args):
    expected = {"CI": "true", "GITHUB_ACTIONS": "true",
                "GITHUB_REPOSITORY": REPOSITORY, "GITHUB_REF": "refs/heads/main"}
    if any(os.environ.get(key) != value for key, value in expected.items()):
        raise ReleaseError("Publishing is restricted to GitHub Actions on yachael/Tingyi main.")
    if os.environ.get("GITHUB_EVENT_NAME") not in ("push", "workflow_dispatch"):
        raise ReleaseError("Publishing requires a push or workflow_dispatch event.")
    if args.parts_dir or args.notes_file or args.commit:
        raise ReleaseError("Publishing only accepts files from the exact GITHUB_SHA.")
    commit = valid_commit(os.environ.get("GITHUB_SHA"))
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token or token.strip() != token or any(c.isspace() for c in token):
        raise ReleaseError("A valid built-in GITHUB_TOKEN is required.")
    return commit, token


def raw_file(commit, path, limit):
    # All paths come from constants below, never from remote metadata.
    return request_bytes(f"https://raw.githubusercontent.com/{REPOSITORY}/{commit}/{path}", limit=limit)


def local_part(directory, name, limit):
    root = directory.resolve(strict=True)
    candidate = root / name
    if candidate.is_symlink() or candidate.resolve(strict=True).parent != root:
        raise ReleaseError("Local part must be a regular file directly inside the parts directory.")
    if not candidate.is_file():
        raise ReleaseError("A local distribution part is missing or is not a regular file.")
    with candidate.open("rb") as handle:
        return handle.read(limit + 1)


def write_verified(path, data):
    if path.is_symlink():
        raise ReleaseError("Refusing to overwrite a symlink.")
    if path.exists():
        if path.is_file() and path.read_bytes() == data:
            return
        raise ReleaseError("Output exists with different content; choose another output directory.")
    with path.open("xb") as handle:
        handle.write(data)


def assemble(parts_dir, commit, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir = output_dir.resolve(strict=True)
    digest = hashlib.sha256()
    total = 0
    with tempfile.TemporaryFile(dir=output_dir) as assembled:
        for index in range(1, PART_COUNT + 1):
            name = f"{FILENAME}.part{index:02d}"
            expected_size = min(PART_SIZE, SIZE - (index - 1) * PART_SIZE)
            part = (local_part(parts_dir, name, expected_size) if parts_dir else
                    raw_file(commit, f".distribution/0.2.9/{name}", expected_size))
            if len(part) != expected_size:
                raise ReleaseError(f"Part {index:02d} has an unexpected size.")
            digest.update(part)
            assembled.write(part)
            total += len(part)
        if total != SIZE or digest.hexdigest() != SHA256:
            raise ReleaseError("Assembled executable failed size or SHA-256 verification.")
        assembled.seek(0)
        write_verified(output_dir / FILENAME, assembled.read())
    write_verified(output_dir / CHECKSUM_NAME, CHECKSUM)
    print(f"Verified {FILENAME}: {SIZE} bytes; SHA256 {SHA256}")
    return output_dir / FILENAME


def release_id(release):
    value = release.get("id")
    if type(value) is not int or value <= 0:
        raise ReleaseError("GitHub returned an invalid release identifier.")
    return value


def find_release(token):
    for page in range(1, 21):
        releases = api(f"/releases?per_page=100&page={page}", token)
        if not isinstance(releases, list):
            raise ReleaseError("Invalid release listing.")
        matches = [item for item in releases if item.get("tag_name") == TAG]
        if len(matches) > 1:
            raise ReleaseError("Multiple releases use the requested tag.")
        if matches:
            return matches[0]
        if len(releases) < 100:
            return None
    raise ReleaseError("Release lookup exceeded its bounded pagination limit.")


def asset_matches(asset, name, data):
    return (asset.get("name") == name and asset.get("state") == "uploaded"
            and asset.get("size") == len(data)
            and asset.get("digest") == "sha256:" + hashlib.sha256(data).hexdigest())


def existing_assets(release, token, expected):
    assets = api(f"/releases/{release_id(release)}/assets?per_page=100", token)
    if not isinstance(assets, list) or len(assets) > len(expected):
        raise ReleaseError("Release contains unexpected assets; no files were replaced.")
    result = {}
    for asset in assets:
        name = asset.get("name")
        if name in result or name not in expected or not asset_matches(asset, name, expected[name]):
            raise ReleaseError("Existing asset differs or has no verifiable digest; no files were replaced.")
        result[name] = asset
    return result


def publish(executable, commit, token, notes):
    expected = {FILENAME: executable.read_bytes(), CHECKSUM_NAME: CHECKSUM}
    if len(expected[FILENAME]) != SIZE or hashlib.sha256(expected[FILENAME]).hexdigest() != SHA256:
        raise ReleaseError("The executable changed after assembly.")
    release = find_release(token)
    if release is not None:
        if release.get("prerelease") is not True:
            raise ReleaseError("An existing release is not a prerelease; no changes made.")
        assets = existing_assets(release, token, expected)
        if release.get("draft") is False:
            if set(assets) == set(expected):
                print(f"Already published with matching verified assets: {RELEASE_URL}")
                return
            raise ReleaseError("Published release is incomplete; refusing to modify it.")
        if release.get("draft") is not True or release.get("name") != TITLE or release.get("body") != notes:
            raise ReleaseError("Existing draft metadata differs; no changes made.")
    else:
        release = api("/releases", token, method="POST", payload={
            "tag_name": TAG, "target_commitish": commit, "name": TITLE,
            "body": notes, "draft": True, "prerelease": True, "make_latest": "false"})
        if release.get("draft") is not True or release.get("tag_name") != TAG:
            raise ReleaseError("GitHub did not create the expected draft.")
        assets = {}
    identifier = release_id(release)
    expected_upload_url = f"https://uploads.github.com/repos/{REPOSITORY}/releases/{identifier}/assets"
    upload_url = release.get("upload_url", "").split("{", 1)[0]
    if upload_url != expected_upload_url:
        raise ReleaseError("GitHub returned an unexpected upload endpoint.")
    for name, data in expected.items():
        if name in assets:
            continue
        response = request_bytes(upload_url + "?" + urllib.parse.urlencode({"name": name}),
                                 method="POST", data=data, token=token,
                                 content_type="application/octet-stream")
        asset = json.loads(response)
        if not asset_matches(asset, name, data):
            raise ReleaseError("Uploaded asset failed digest verification; release remains a draft.")
        print(f"Uploaded and verified {name}")
    if set(existing_assets(release, token, expected)) != set(expected):
        raise ReleaseError("Draft does not contain both verified assets.")
    published = api(f"/releases/{identifier}", token, method="PATCH",
                    payload={"draft": False, "prerelease": True, "make_latest": "false"})
    if published.get("draft") is not False or published.get("prerelease") is not True:
        raise ReleaseError("GitHub did not confirm prerelease publication.")
    print(f"Published: {RELEASE_URL}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="Publish only within the allowed Actions environment")
    parser.add_argument("--parts-dir", type=Path, help="Local directory containing the eleven fixed-name parts")
    parser.add_argument("--notes-file", type=Path, help="Local notes to validate without publishing")
    parser.add_argument("--commit", help="Exact commit for read-only raw downloads")
    parser.add_argument("--output-dir", type=Path, default=Path("publication-output"))
    args = parser.parse_args()
    if args.publish:
        commit, token = publish_context(args)
    else:
        commit = None if args.parts_dir else valid_commit(args.commit or os.environ.get("GITHUB_SHA"))
        token = None
    executable = assemble(args.parts_dir, commit, args.output_dir)
    if args.publish:
        notes_bytes = raw_file(commit, "docs/RELEASE-NOTES-0.2.9.md", 64 * 1024)
        notes = notes_bytes.decode("utf-8-sig").strip()
        if not notes or "0.2.9" not in notes:
            raise ReleaseError("Release notes are empty or identify an unexpected version.")
        publish(executable, commit, token, notes)
    else:
        if args.notes_file:
            notes = args.notes_file.read_text(encoding="utf-8-sig").strip()
            if not notes or "0.2.9" not in notes:
                raise ReleaseError("Local release notes are empty or identify an unexpected version.")
        print("Assembly only. No GitHub release was created or changed.")


if __name__ == "__main__":
    try:
        main()
    except (ReleaseError, OSError, ValueError) as exc:
        # Known exception text never contains request headers or the token.
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
