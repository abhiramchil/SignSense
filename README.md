# SignSense

A project for learning Python and machine learning while building toward an ASL learning app.

See [CHANGELOG.md](CHANGELOG.md) for development progress and the reasons behind changes.

## Run the webcam preview

From the project folder, create a virtual environment and install OpenCV and MediaPipe:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python webcam.py
```

Allow camera access if prompted. On macOS, if access is blocked, open **System Settings → Privacy & Security → Camera** and enable access for the terminal or editor running Python. You may need to restart that app afterward.

On first run, the script downloads Google's hand landmark model to `models/hand_landmarker.task` (internet required). Later runs reuse the downloaded file, which is ignored by Git.

Hold one or both hands in view to see orange landmark dots and green connections. Click the preview window and press **Q** or **Escape** to quit. Closing the window also stops the preview.

## How it works

- `cv2.VideoCapture(camera_index)` opens the selected camera. `camera_index` currently defaults to `1` to try the MacBook camera because `0` selected the phone during setup. Device numbering can change; try `0` if `1` is unavailable or selects the wrong camera.
- `camera.read()` retrieves one frame (an image) at a time.
- The loop retries failed reads for up to 5 seconds to allow camera startup or brief interruptions, then reports an error if no frames arrive.
- `cv2.flip(frame, 1)` mirrors that image horizontally.
- Each frame is converted from OpenCV's BGR colors to RGB (RGBA on macOS), then passed to MediaPipe's Hand Landmarker in VIDEO mode with an increasing timestamp. Processing one frame at a time keeps the overlay aligned with its image. On macOS the script selects the Metal GPU backend to avoid a graphics-service crash observed with MediaPipe 1.0.1's default backend.
- `draw_landmarks()` converts the model's normalized coordinates to pixel positions and draws the hand connections and points for up to two hands.
- `cv2.imshow(...)` displays the image, and `cv2.waitKey(1)` keeps the window responsive while checking for a key press.
- The `finally` block releases the webcam and closes the window when the program stops.

The preview processes video locally and does not save or upload camera frames. The landmarker is closed when the camera loop exits. This detects hand positions; recognizing ASL signs will require a separate classification step.

Reference: [MediaPipe Hand Landmarker Python guide](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python).

## Documenting changes before a push

Before committing and pushing, ask the coding assistant to update the project documentation. It will review the changes, update `CHANGELOG.md`, and adjust this README when setup or usage changes. Include those documentation updates in your commit.

This is a prompt-driven workflow; `git push` itself does not update the files.
