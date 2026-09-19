"""Open the webcam and display a live preview. Press Q to quit."""

import sys
import time
from pathlib import Path
from urllib.request import urlopen

import cv2
import mediapipe as mp


MODEL_PATH = Path(__file__).resolve().parent / "models" / "hand_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
)
# MediaPipe 1.0.1 on macOS needs the Metal GPU backend and RGBA input.
USE_METAL = sys.platform == "darwin"


def download_model():
    """Download the trained model once, then reuse the local copy."""
    if MODEL_PATH.is_file():
        return
    print("Downloading the hand landmark model (first run only)...")
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = MODEL_PATH.with_suffix(".part")
    try:
        with urlopen(MODEL_URL, timeout=30) as response:
            temporary_path.write_bytes(response.read())
        temporary_path.replace(MODEL_PATH)
    except OSError as error:
        raise RuntimeError(
            "Could not download the hand model. Check your internet connection "
            "and try again. You can also download MODEL_URL manually and save "
            f"it to {MODEL_PATH}."
        ) from error
    finally:
        temporary_path.unlink(missing_ok=True)


def draw_landmarks(frame, result):
    """Convert normalized landmark coordinates into pixels and draw each hand."""
    height, width = frame.shape[:2]
    for hand in result.hand_landmarks:
        points = [(int(point.x * width), int(point.y * height)) for point in hand]
        for connection in mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS:
            cv2.line(frame, points[connection.start], points[connection.end],
                     (0, 220, 0), 2)
        for point in points:
            cv2.circle(frame, point, 4, (0, 140, 255), -1)


def main():
    download_model()
    # VIDEO mode processes frames in order, keeping tracking between frames.
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(MODEL_PATH),
            delegate=(mp.tasks.BaseOptions.Delegate.GPU if USE_METAL
                      else mp.tasks.BaseOptions.Delegate.CPU),
        ),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=2,
    )
    with mp.tasks.vision.HandLandmarker.create_from_options(options) as landmarker:
        run_camera(landmarker)


def run_camera(landmarker):
    # Index 0 selected your phone; try index 1 for the MacBook camera.
    # Camera numbering can change when devices connect or disconnect.
    camera_index = 1
    camera = cv2.VideoCapture(camera_index)
    window_name = "SignSense - Press Q to quit"

    try:
        if not camera.isOpened():
            raise RuntimeError(
                "Could not open the webcam. Check camera permissions and "
                "close any other apps using it."
            )

        cv2.namedWindow(window_name)
        # Allow startup time and brief interruptions in the video stream.
        frame_deadline = time.monotonic() + 5
        previous_timestamp_ms = -1

        while True:
            # A frame is one image from the camera's video stream.
            success, frame = camera.read()
            if success and frame is not None and frame.size > 0:
                frame_deadline = time.monotonic() + 5
                # Flip horizontally so the preview behaves like a mirror.
                frame = cv2.flip(frame, 1)
                # Metal needs an alpha channel; CPU inference uses RGB.
                color_conversion = cv2.COLOR_BGR2RGBA if USE_METAL else cv2.COLOR_BGR2RGB
                image_format = mp.ImageFormat.SRGBA if USE_METAL else mp.ImageFormat.SRGB
                model_frame = cv2.cvtColor(frame, color_conversion)
                image = mp.Image(image_format=image_format, data=model_frame)
                # MediaPipe requires strictly increasing timestamps in milliseconds.
                timestamp_ms = max(time.monotonic_ns() // 1_000_000,
                                   previous_timestamp_ms + 1)
                previous_timestamp_ms = timestamp_ms
                result = landmarker.detect_for_video(image, timestamp_ms)
                draw_landmarks(frame, result)
                cv2.imshow(window_name, frame)
            else:
                if time.monotonic() >= frame_deadline:
                    raise RuntimeError(
                        "The camera opened but supplied no frames for 5 seconds. "
                        "Close other camera apps and check that Photo Booth works. "
                        "If you have multiple cameras, try another camera_index."
                    )
                time.sleep(0.05)

            # Process window events and check for a key press every frame.
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q"), 27):
                break
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
    finally:
        # Always release the camera, even if something goes wrong.
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
