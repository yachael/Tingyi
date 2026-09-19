# Tingyi 0.2.9 technical notes

The 0.2.9 delivery record reports:

- Release build: 0 warnings and 0 errors.
- Core checks: 285 passed.
- Native WinUI and runtime checks: 572 passed.
- Local caption event replay: 104 passed.
- Local process-exclusion capture: start, frames and stop checked.

These are the existing build results. Public packaging does not rebuild the application or run new translation sessions.

The public package retains all 473 original runtime and license files byte for byte. The README adds English and French startup instructions. The self-extracting wrapper uses the same official 7-Zip 26.03 component as the previous public package, with its license and corresponding source included. The extracted package is checked against the staging files before publication.

Voice conversation models have been removed. Older settings and saved conversations remain readable; continuing an older voice-model conversation uses a dedicated translation model. Some migrated language selections may need to be selected again.

System audio capture excludes Tingyi and its child processes, allowing meeting audio and translated speech on the same headphones. Other applications' audio, including notification sounds, is still part of system capture.
