# Tingyi 0.2.5 — Windows x64 development preview

Portable live translated captions and personal headphone audio for Windows 11 x64 (build 22000 or later).

## Download and start

[Download `Tingyi-Windows-x64-0.2.5-preview.exe`](https://github.com/yachael/Tingyi/releases/download/v0.2.5-preview/Tingyi-Windows-x64-0.2.5-preview.exe) and run this self-extracting archive. Choose a writable folder and click **Extract**. Open the extracted folder, then run `Tingyi.exe`. Keep all bundled files together. The .NET and Windows App SDK runtimes are included. The extracted README provides English, French and Chinese instructions. [SHA256SUMS.txt](https://github.com/yachael/Tingyi/releases/download/v0.2.5-preview/SHA256SUMS.txt) contains the checksum of the downloaded self-extracting EXE.

Internet access and your own OpenAI, Google or ByteDance API key are required. Provider permissions, quota and charges apply. Live audio is transmitted to the selected provider. Translated audio requires a Windows-recognized headphone device and your confirmation after the test tone; captions remain available without headphones.

## Changes in 0.2.5

- Reduced runtime dependencies by using the required Windows App SDK component packages. Unused AI, machine-learning, Widgets and Search dependencies were removed from the dependency graph. Native Windows tray and power notifications replace the Windows Forms dependency.
- Completed the retirement of the old WPF interface and separated Windows audio, session runtime, credentials and recording into a shared Windows module. Settings, credential identifiers and session formats remain compatible.
- Unified reading behavior in the main view and floating captions, including history navigation, follow mode and restoring hidden views. Fixed an issue where returning to the latest captions while hidden did not refresh the view snapshot.
- Separated translated-audio playback lifecycle from session orchestration and moved UI simulation and replay code into a separate test assembly that is not distributed.

The public self-extracting package omits developer documentation, evidence/logs and debug symbols. Application executables, runtime libraries, resources and third-party notices are retained without modification; no software rebuild was performed for this packaging step. The required SoundTouch.Net corresponding-source archive remains under `licenses/` in the extracted folder.

## Validation and limitations

The existing 0.2.5 validation record reports a Release build with zero warnings/errors, 260/260 core checks, 372/372 native UI/runtime regression checks and 104/104 local replay checks. Those checks used isolated settings, simulated service connections/devices and existing events. They made no new translation API calls and uploaded no audio. These results are the existing build evidence, not newly rerun tests for this public packaging step. They do not establish clean-machine acceptance of the self-extracting package.

**This is an unsigned development preview, not a fully validated stable release.** Full physical-device and all-provider validation is incomplete. Long-running use, real device unplugging, sleep/wake, clean Windows installations and installer workflows have not received full acceptance testing. The full pre-start dialog also lacks complete offline test coverage. Recognition, translation and language routing can be incorrect; model visibility or a key check does not establish live-session permissions, quota or compatibility. Previous limited OpenAI API checks do not establish acceptance for every provider or audio device. Windows may display an unsigned-app warning.

Third-party terms are in `THIRD-PARTY-NOTICES.md` and `licenses/`. No public open-source license has been chosen for the original Tingyi code. This preview provides the portable binary distribution in a self-extracting archive; no Tingyi application source archive is attached.

## Français

[Télécharger `Tingyi-Windows-x64-0.2.5-preview.exe`](https://github.com/yachael/Tingyi/releases/download/v0.2.5-preview/Tingyi-Windows-x64-0.2.5-preview.exe) et lancer cette archive auto-extractible. Choisir un dossier accessible en écriture et cliquer sur **Extract**, puis ouvrir le dossier extrait et lancer `Tingyi.exe`. Conserver tous les fichiers fournis. Windows 11 x64 (version 22000 ou ultérieure), une connexion Internet et votre propre clé API sont nécessaires. Les frais API vous incombent et l’audio est transmis au fournisseur choisi. Pour la traduction audio, utiliser un casque reconnu par Windows et confirmer le son d’essai ; les sous-titres fonctionnent sans casque.

La version 0.2.5 réduit les dépendances, retire l’ancienne interface WPF, unifie la lecture des sous-titres et sépare les modules de lecture audio et de test. Cette préversion n’est pas signée. Les tests existants reposent sur des connexions et périphériques simulés et une relecture locale, sans nouveaux appels API de traduction. Les appareils réels, tous les fournisseurs, les longues sessions et les installations propres ne sont pas entièrement validés. La précision de la reconnaissance, de la traduction et du routage n’est pas garantie.

## 中文说明

0.2.5 精简运行依赖，改用 Windows 原生托盘与电源通知，完成旧 WPF 界面退役，统一主窗口和悬浮字幕阅读逻辑，并分离播放控制及测试模块。公开包保留原程序、运行时、资源和全部第三方许可；不含开发文档、测试证据、调试符号或听译原创源码包，所需 SoundTouch.Net 对应源码仍随许可提供。

[下载 `Tingyi-Windows-x64-0.2.5-preview.exe`](https://github.com/yachael/Tingyi/releases/download/v0.2.5-preview/Tingyi-Windows-x64-0.2.5-preview.exe)，运行这个自解压文件，选择可写文件夹并点击 **Extract**。进入展开后的文件夹，再打开 `Tingyi.exe`，保留所有配套文件。[SHA256SUMS.txt](../downloads/SHA256SUMS.txt) 提供下载的自解压 EXE 校验值。

需要 Windows 11 x64、网络和自己的 API Key，API 费用自理；实时音频发送给所选服务商。译音需选择 Windows 识别的耳机，试听并确认；无耳机仍可使用字幕。本版未签名，真实设备、全部服务商及长时间使用尚未完整验收，不是正式稳定版。本轮现有验证为模拟连接／设备与本地回放，未新增翻译 API 调用；不保证识别、翻译及路由准确性。
