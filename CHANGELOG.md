# Changelog

Plain-language notes about what changed, why it changed, and what was verified. New development entries go first.

## 2026-09-18 — Webcam preview

- Added a Python/OpenCV webcam preview as the first step toward learning computer vision for an ASL learning app.
- Mirrored the video and added Q, Escape, and window-close controls to stop the preview. The camera is released when the program exits, including on errors.
- Added a 5-second retry window for failed frame reads. The first version stopped immediately when the camera had not yet supplied a frame.
- Made the camera index an explicit variable, currently set to `1` to try the MacBook camera after index `0` selected the phone. Camera numbering depends on connected devices.
- Added the OpenCV dependency, virtual environment setup instructions, macOS camera permission guidance, and ignores for local Python environment files.
- Added a changelog and a prompt-driven documentation workflow for future pushes.

Validation: Python syntax and Git whitespace checks passed. The user confirmed the preview worked with the phone camera after the retry change. The MacBook camera selection still needs confirmation.
