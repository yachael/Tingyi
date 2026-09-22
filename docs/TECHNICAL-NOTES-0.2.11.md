# Tingyi 0.2.11 technical notes

Existing delivery validation: Release build with 0 warnings and 0 errors; 306 core checks, 604 native UI/runtime checks, 104 local replay checks, 116 OpenAI/Google offline checks and 16 ByteDance offline checks passed. Local process-exclusion capture start, frames and stop were checked without saving or uploading audio.

Public packaging preserves the delivered application and runtime files byte for byte, adds English/French startup instructions and the official 7-Zip self-extractor with its license and corresponding source, and verifies extraction and download hashes. It does not rebuild the app or run new translation API sessions.

This version includes the audio scheduling fixes from 0.2.10 and the connection completion, retry classification, window activation, accessibility and contrast-theme fixes from 0.2.11.
