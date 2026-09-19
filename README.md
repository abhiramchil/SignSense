# SignSense

A project for learning Python and machine learning while building toward an ASL learning app.

See [CHANGELOG.md](CHANGELOG.md) for development progress and the reasons behind changes.

## Run the webcam preview

From the project folder, create a virtual environment and install OpenCV:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python webcam.py
```

Allow camera access if prompted. On macOS, if access is blocked, open **System Settings → Privacy & Security → Camera** and enable access for the terminal or editor running Python. You may need to restart that app afterward.

Click the preview window and press **Q** or **Escape** to quit. Closing the window also stops the preview.

## How it works

- `cv2.VideoCapture(camera_index)` opens the selected camera. `camera_index` currently defaults to `1` to try the MacBook camera because `0` selected the phone during setup. Device numbering can change; try `0` if `1` is unavailable or selects the wrong camera.
- `camera.read()` retrieves one frame (an image) at a time.
- The loop retries failed reads for up to 5 seconds to allow camera startup or brief interruptions, then reports an error if no frames arrive.
- `cv2.flip(frame, 1)` mirrors that image horizontally.
- `cv2.imshow(...)` displays the image, and `cv2.waitKey(1)` keeps the window responsive while checking for a key press.
- The `finally` block releases the webcam and closes the window when the program stops.

The preview runs locally and does not save or upload video. Later, you can add hand detection inside the loop to process each frame before displaying it.

## Documenting changes before a push

Before committing and pushing, ask the coding assistant to update the project documentation. It will review the changes, update `CHANGELOG.md`, and adjust this README when setup or usage changes. Include those documentation updates in your commit.

This is a prompt-driven workflow; `git push` itself does not update the files.
