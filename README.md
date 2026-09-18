# Tingyi / 听译

Inspired by the Tower of Babel, Tingyi helps people understand each other across languages. It is optimized for in-person, face-to-face conversations, with live translated captions and personal headphone audio, starting on Windows. An Internet connection is required for translation.

**Windows preview: 0.2.5 — unsigned development preview for Windows 11 x64.** Validation is incomplete.

[Download the Windows preview](https://github.com/yachael/Tingyi/releases/download/v0.2.5-preview/Tingyi-Windows-x64-0.2.5-preview.exe) · [SHA-256 checksum](downloads/SHA256SUMS.txt) · [Version notes](docs/RELEASE-NOTES-0.2.5.md)

## Get started

1. Use **Windows 11 x64, build 22000 or later**. Download and run `Tingyi-Windows-x64-0.2.5-preview.exe`, a self-extracting archive. Choose a writable folder and click **Extract**. Open the extracted folder, then run `Tingyi.exe`. Keep all bundled files together. The .NET and Windows App SDK runtimes are included.
2. Connect to the Internet. In Settings, add **your own OpenAI, Google or ByteDance API key** and set it as the provider default. No account or key is supplied. Your account needs the required service/model permissions and quota; API charges are yours. ByteDance requires a Volcengine voice console key, not an Ark key.
3. Choose the audio source/device, provider, model and languages, then start translation. Allow Windows desktop microphone access when using a microphone. **Live audio is sent to the selected provider.**
4. Captions work without headphones. For translated audio, select headphones recognized by Windows, play the test tone and **confirm that you hear it in the headphones you are wearing**. Reconfirm after device or relevant route changes. Speakers and unknown device types remain captions-only. System capture and translated output cannot share the same endpoint.

The package includes English, French and Chinese instructions. Use [SHA256SUMS.txt](downloads/SHA256SUMS.txt) to check the downloaded self-extracting EXE.

## Interface preview

The following English and French screenshots come from the **0.2.3 demonstration build**, with **demo captions**. They illustrate the interface and are not screenshots of the current 0.2.5 preview.

English interface:

![English interface from the Tingyi 0.2.3 demonstration build, with demo captions](images/tingyi-interface-en.png)

French interface:

![French interface from the Tingyi 0.2.3 demonstration build, with demo captions](images/tingyi-interface-fr.png)

## Preview limitations

Full physical-device and all-provider acceptance testing is incomplete, including long sessions, device unplugging, sleep/wake, clean Windows installations and installer workflows. Existing 0.2.5 checks used simulated connections/devices and local event replay, with no new translation API calls. The full pre-start dialog lacks complete offline test coverage; a successful key check or visible model does not establish live-session permissions, quota or compatibility. Recognition, translation, language routing and audio compatibility can fail. Windows may display an unsigned-app warning.

API keys are stored in Windows Credential Manager. Caption history and optional recordings are local files without additional file encryption. Recording requires explicit activation and confirmation.

## Distribution and roadmap

This repository distributes portable Windows binaries in a self-extracting archive. No public open-source license has been chosen for the original Tingyi code, and no Tingyi application source archive is attached. Component terms and the required SoundTouch.Net corresponding source are included under `THIRD-PARTY-NOTICES.md` and `licenses/` in the extracted folder.

Windows acceptance comes first. iPhone development is planned after Windows acceptance; no iPhone release is available here.

## Français

Inspiré par la tour de Babel, Tingyi est optimisé pour les conversations en face à face avec des sous-titres traduits en direct et une traduction audio personnelle au casque. La version **0.2.5 est une préversion de développement non signée** pour Windows 11 x64, dont la validation reste incomplète.

[Télécharger la préversion](https://github.com/yachael/Tingyi/releases/download/v0.2.5-preview/Tingyi-Windows-x64-0.2.5-preview.exe) et lancer l’archive auto-extractible `Tingyi-Windows-x64-0.2.5-preview.exe`. Choisir un dossier accessible en écriture et cliquer sur **Extract**, puis ouvrir le dossier extrait et lancer `Tingyi.exe`. Conserver tous les fichiers fournis. Une connexion Internet et **votre propre clé API** sont nécessaires ; les frais API vous incombent et l’audio est transmis au fournisseur choisi. Pour le son traduit, sélectionner un casque reconnu par Windows, écouter le son d’essai et confirmer qu’il sort du casque porté. Les sous-titres fonctionnent sans casque. Le développement iPhone est prévu après la validation de Windows.

Les captures ci-dessus proviennent de la version de démonstration **0.2.3** et contiennent des **sous-titres de démonstration** ; elles ne montrent pas la préversion actuelle 0.2.5.

## 简体中文

听译以“巴别塔”为核心概念，希望帮助人们跨越语言障碍，重点针对线下面对面对话优化，提供实时翻译字幕和个人耳机译音。当前 **0.2.5 为 Windows 11 x64 未签名开发预览版**，真实设备、全部服务商及长时间使用等尚未完整验收，不是正式稳定版。

[下载预览版](https://github.com/yachael/Tingyi/releases/download/v0.2.5-preview/Tingyi-Windows-x64-0.2.5-preview.exe)，运行自解压文件 `Tingyi-Windows-x64-0.2.5-preview.exe`，选择可写文件夹并点击 **Extract**。进入展开后的文件夹，再运行 `Tingyi.exe`，保留所有配套文件。线下对话指面对面使用场景，翻译仍需联网并使用**自己的 API Key**，费用自理，实时音频发送给所选服务商。需要译音时，选择 Windows 识别的耳机，试听短音并确认声音来自佩戴中的耳机；无耳机仍可使用字幕。iPhone 开发计划在 Windows 验收后推进。

上方英文、法语界面截图来自 **0.2.3 展示构建**，字幕为**演示内容**，不是当前 0.2.5 预览版的截图。
