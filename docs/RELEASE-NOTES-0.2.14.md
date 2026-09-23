# Tingyi 0.2.14

Tingyi now chooses CPU or GPU separately for local speech recognition and translation, based on the computer you use.

- Automatic hardware selection, with a manual CPU option.
- If a GPU stage cannot load, that stage can fall back to CPU after a memory check.
- Local bilingual captions work without uploading audio or using a cloud API key, after the optional models are installed.
- When upgrading, existing TranslateGemma files are reused; the new Qwen model and audio encoder are downloaded as needed.

Local models and optional Vulkan components are downloaded separately from the app. Local mode produces subtitles; translated audio is available through supported cloud providers. Actual model speed depends on your computer.

**[Download for Windows](https://github.com/yachael/Tingyi/releases/download/v0.2.14-preview/Tingyi-Windows-x64-0.2.14-preview.zip)** · Windows 11 x64 · 68.39 MiB

Extract the ZIP, open the folder and run `Tingyi.exe`. Keep all extracted files together. Configure a cloud provider or install the optional models from the Local models page.

## Français

Tingyi choisit désormais le CPU ou le GPU séparément pour la reconnaissance vocale et la traduction locales, selon votre ordinateur.

- Sélection automatique du matériel, avec une option CPU manuelle.
- Si une étape ne peut pas charger le modèle sur le GPU, elle peut revenir au CPU après vérification de la mémoire.
- Après installation des modèles optionnels, les sous-titres bilingues locaux fonctionnent sans envoyer votre audio ni utiliser de clé API cloud.
- Lors de la mise à niveau, les fichiers TranslateGemma existants sont réutilisés ; le nouveau modèle Qwen et son encodeur audio sont téléchargés si nécessaire.

Les modèles et composants Vulkan optionnels se téléchargent séparément. Le mode local produit des sous-titres ; l’audio traduit reste disponible auprès des services cloud compatibles. La vitesse dépend de votre ordinateur.

**[Télécharger pour Windows](https://github.com/yachael/Tingyi/releases/download/v0.2.14-preview/Tingyi-Windows-x64-0.2.14-preview.zip)**

Décompressez le ZIP, ouvrez le dossier et lancez `Tingyi.exe`. Conservez tous les fichiers ensemble, puis configurez votre service cloud ou installez les modèles locaux.

## 中文

0.2.14 会根据电脑配置，分别为本地语音识别和翻译选择 CPU 或 GPU。

- 默认自动选择，也可以手动选择 CPU。
- 某个环节无法在 GPU 上加载时，会检查内存，再尝试让该环节改用 CPU。
- 安装可选模型后，可以在本机生成双语字幕，不上传语音，也不需要云端 API 密钥。
- 升级时复用已有 TranslateGemma 文件，按需补装新版 Qwen 模型和音频编码器。

模型和可选 Vulkan 组件需另行下载。本地模式提供字幕；需要耳机译音时，可选择支持该功能的云端服务。实际运行速度取决于电脑配置。

**[下载 Windows 版](https://github.com/yachael/Tingyi/releases/download/v0.2.14-preview/Tingyi-Windows-x64-0.2.14-preview.zip)** · Windows 11 x64 · 68.39 MiB

解压 ZIP，进入文件夹，运行 `Tingyi.exe`，保留完整配套文件。选择云端服务，或在“本地模型”页安装模型。

---

Validation: 362 core checks and 698 WinUI checks passed. Local model workflows were checked with offline fixtures; complete model inference and speed benchmarks were not run for this release.
