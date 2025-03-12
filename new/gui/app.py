from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QCloseEvent
from typing import Optional, Any
import cv2
import numpy as np

from core.video_processor import VideoProcessor
from core.pose_detector import PoseDetector
from core.pose_comparison import PoseComparison
from gui.components import ScoreDisplay
from utils.visualization import draw_pose_landmarks, draw_comparison_metrics


class TrackerApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tracker")
        self.setMinimumSize(1200, 700)

        self.video_processor: VideoProcessor = VideoProcessor()
        self.pose_detector: PoseDetector = PoseDetector()
        self.pose_comparison: PoseComparison = PoseComparison()

        self.video_path: Optional[str] = None
        self.webcam_active: bool = False
        self.comparison_active: bool = False
        self.webcam_id: int = 1

        self._setup_ui()

        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)

    def _setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        video_layout = QHBoxLayout()

        self.reference_video_label: QLabel = QLabel("Загрузите видео")
        self.reference_video_label.setAlignment(Qt.AlignCenter)
        self.reference_video_label.setMinimumSize(480, 360)
        self.reference_video_label.setStyleSheet("border: 1px solid gray;")

        self.webcam_video_label: QLabel = QLabel("Веб-камера")
        self.webcam_video_label.setAlignment(Qt.AlignCenter)
        self.webcam_video_label.setMinimumSize(480, 360)
        self.webcam_video_label.setStyleSheet("border: 1px solid gray;")

        video_layout.addWidget(self.reference_video_label)
        video_layout.addWidget(self.webcam_video_label)

        controls_layout = QHBoxLayout()

        self.load_video_btn: QPushButton = QPushButton("Загрузить видео")
        self.load_video_btn.clicked.connect(self.load_video)

        self.start_webcam_btn: QPushButton = QPushButton("Включить камеру")
        self.start_webcam_btn.clicked.connect(self.toggle_webcam)

        self.start_comparison_btn: QPushButton = QPushButton("Начать сравнение")
        self.start_comparison_btn.clicked.connect(self.toggle_comparison)
        self.start_comparison_btn.setEnabled(False)

        controls_layout.addWidget(self.load_video_btn)
        controls_layout.addWidget(self.start_webcam_btn)
        controls_layout.addWidget(self.start_comparison_btn)

        self.score_display: ScoreDisplay = ScoreDisplay()

        accuracy_layout = QHBoxLayout()
        accuracy_label: QLabel = QLabel("Общая точность:")
        self.accuracy_bar: QProgressBar = QProgressBar()
        self.accuracy_bar.setRange(0, 100)
        self.accuracy_bar.setValue(0)
        accuracy_layout.addWidget(accuracy_label)
        accuracy_layout.addWidget(self.accuracy_bar)

        main_layout.addLayout(video_layout)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.score_display)
        main_layout.addLayout(accuracy_layout)

    def load_video(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите видео", "", "Video Files (*.mp4 *.avi *.mkv)")
        if file_path:
            self.video_path = file_path
            success: bool = self.video_processor.load_reference_video(file_path)
            if success:
                self.load_video_btn.setText("Видео загружено")
                if self.webcam_active:
                    self.start_comparison_btn.setEnabled(True)
            else:
                self.load_video_btn.setText("Ошибка загрузки")

    def toggle_webcam(self) -> None:
        self.webcam_active = not self.webcam_active

        if self.webcam_active:
            success: bool = self.video_processor.start_webcam(self.webcam_id)
            if success:
                self.start_webcam_btn.setText("Выключить камеру")
                if self.video_path:
                    self.start_comparison_btn.setEnabled(True)
            else:
                self.webcam_active = False
                self.start_webcam_btn.setText("Ошибка камеры")
        else:
            self.video_processor.stop_webcam()
            self.start_webcam_btn.setText("Включить камеру")
            self.start_comparison_btn.setEnabled(False)
            self.comparison_active = False
            self.start_comparison_btn.setText("Начать сравнение")

    def toggle_comparison(self) -> None:
        self.comparison_active = not self.comparison_active

        if self.comparison_active:
            self.start_comparison_btn.setText("Остановить сравнение")
            self.score_display.reset_scores()
        else:
            self.start_comparison_btn.setText("Начать сравнение")

    def update_frames(self) -> None:
        ref_pose_results: Optional[Any] = None

        if self.video_path and self.video_processor.reference_video_capture:
            ref_frame: Optional[np.ndarray] = self.video_processor.get_reference_frame()
            if ref_frame is not None:
                ref_pose_results = self.pose_detector.detect_pose(ref_frame)
                ref_frame_with_landmarks: np.ndarray = draw_pose_landmarks(ref_frame, ref_pose_results)

                height, width, channel = ref_frame_with_landmarks.shape
                bytes_per_line: int = 3 * width
                q_image: QImage = QImage(
                    ref_frame_with_landmarks.data, width, height, bytes_per_line, QImage.Format_RGB888
                ).rgbSwapped()
                self.reference_video_label.setPixmap(
                    QPixmap.fromImage(q_image).scaled(
                        self.reference_video_label.width(),
                        self.reference_video_label.height(),
                        Qt.KeepAspectRatio,
                    )
                )

        if self.webcam_active and self.video_processor.webcam_capture:
            webcam_frame: Optional[np.ndarray] = self.video_processor.get_webcam_frame()
            if webcam_frame is not None:
                webcam_pose_results: Any = self.pose_detector.detect_pose(webcam_frame)
                webcam_frame_with_landmarks: np.ndarray = draw_pose_landmarks(webcam_frame, webcam_pose_results)

                if self.comparison_active and ref_pose_results is not None and webcam_pose_results is not None:
                    comparison_metrics: Any = self.pose_comparison.compare_poses(ref_pose_results, webcam_pose_results)
                    webcam_frame_with_landmarks = draw_comparison_metrics(webcam_frame_with_landmarks, comparison_metrics)

                    overall_accuracy: float = self.pose_comparison.calculate_overall_accuracy(comparison_metrics)
                    self.accuracy_bar.setValue(int(overall_accuracy * 100))
                    self.score_display.update_scores(comparison_metrics)

                height, width, channel = webcam_frame_with_landmarks.shape
                bytes_per_line: int = 3 * width
                q_image: QImage = QImage(
                    webcam_frame_with_landmarks.data, width, height, bytes_per_line, QImage.Format_RGB888
                ).rgbSwapped()
                self.webcam_video_label.setPixmap(
                    QPixmap.fromImage(q_image).scaled(
                        self.webcam_video_label.width(),
                        self.webcam_video_label.height(),
                        Qt.KeepAspectRatio,
                    )
                )

    def closeEvent(self, event: QCloseEvent) -> None:
        self.video_processor.release_all()
        event.accept()
