"""Open the webcam and display a live preview. Press Q to quit."""

import time

import cv2


def main():
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

        while True:
            # A frame is one image from the camera's video stream.
            success, frame = camera.read()
            if success and frame is not None and frame.size > 0:
                frame_deadline = time.monotonic() + 5
                # Flip horizontally so the preview behaves like a mirror.
                frame = cv2.flip(frame, 1)
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
