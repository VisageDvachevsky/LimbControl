import cv2
import threading
import numpy as np
import time
from typing import Optional

class VideoProcessor:
    def __init__(self) -> None:
        self.reference_video_capture: Optional[cv2.VideoCapture] = None
        self.webcam_capture: Optional[cv2.VideoCapture] = None
        self.reference_frame: Optional[np.ndarray] = None
        self.webcam_frame: Optional[np.ndarray] = None
        self.reference_thread: Optional[threading.Thread] = None
        self.webcam_thread: Optional[threading.Thread] = None
        self.reference_running: bool = False
        self.webcam_running: bool = False
        self.reference_start_time: Optional[float] = None
        self.reference_fps: Optional[float] = None

    def load_reference_video(self, video_path: str) -> bool:
        if self.reference_running:
            self.stop_reference_video()

        self.reference_video_capture = cv2.VideoCapture(video_path)
        if not self.reference_video_capture.isOpened():
            print(f"Ошибка открытия видео: {video_path}")
            return False

        self.reference_fps = self.reference_video_capture.get(cv2.CAP_PROP_FPS)
        self.reference_running = True
        self.reference_thread = threading.Thread(target=self._process_reference_video, daemon=True)
        self.reference_thread.start()
        self.reference_start_time = time.time()
        return True

    def start_webcam(self, camera_id: int = 0) -> bool:
        if self.webcam_running:
            self.stop_webcam()

        self.webcam_capture = cv2.VideoCapture(camera_id)
        if not self.webcam_capture.isOpened():
            print(f"Ошибка открытия камеры: {camera_id}")
            return False

        self.webcam_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.webcam_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.webcam_running = True
        self.webcam_thread = threading.Thread(target=self._process_webcam, daemon=True)
        self.webcam_thread.start()
        return True

    def _process_reference_video(self) -> None:
        frame_count: int = 0
        while self.reference_running:
            if self.reference_video_capture is None:
                break

            ret, frame = self.reference_video_capture.read()
            if not ret:
                self.reference_video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                if self.reference_fps:
                    self.reference_start_time = time.time() - (1.0 / self.reference_fps)
                else:
                    self.reference_start_time = time.time()
                frame_count = 0
                continue

            self.reference_frame = frame
            frame_count += 1

            if self.reference_fps:
                expected_frame = (time.time() - self.reference_start_time) * self.reference_fps
                if frame_count < expected_frame - 1:
                    continue
                elif frame_count > expected_frame + 1:
                    time.sleep((frame_count - expected_frame) / self.reference_fps)

    def _process_webcam(self) -> None:
        while self.webcam_running:
            if self.webcam_capture is None:
                break

            ret, frame = self.webcam_capture.read()
            if not ret:
                continue

            self.webcam_frame = frame

    def get_reference_frame(self) -> Optional[np.ndarray]:
        return self.reference_frame

    def get_webcam_frame(self) -> Optional[np.ndarray]:
        return self.webcam_frame

    def stop_reference_video(self) -> None:
        self.reference_running = False
        if self.reference_thread:
            self.reference_thread.join(timeout=1.0)
        if self.reference_video_capture:
            self.reference_video_capture.release()
            self.reference_video_capture = None

    def stop_webcam(self) -> None:
        self.webcam_running = False
        if self.webcam_thread:
            self.webcam_thread.join(timeout=1.0)
        if self.webcam_capture:
            self.webcam_capture.release()
            self.webcam_capture = None

    def release_all(self) -> None:
        self.stop_reference_video()
        self.stop_webcam()
