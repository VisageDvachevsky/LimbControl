import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Any, Dict, Tuple

def draw_pose_landmarks(frame: Optional[np.ndarray], pose_results: Any) -> Optional[np.ndarray]:
    if frame is None or not pose_results.pose_landmarks:
        return frame

    annotated_frame = frame.copy()
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    mp_drawing.draw_landmarks(
        annotated_frame,
        pose_results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
    )

    return annotated_frame

def draw_comparison_metrics(frame: Optional[np.ndarray], metrics: Optional[Dict[int, float]]) -> Optional[np.ndarray]:
    if frame is None or not metrics:
        return frame

    annotated_frame = frame.copy()

    keypoint_names = {
        0: "Нос", 11: "Л.Плечо", 12: "П.Плечо",
        13: "Л.Локоть", 14: "П.Локоть", 15: "Л.Запястье",
        16: "П.Запястье", 23: "Л.Бедро", 24: "П.Бедро",
        25: "Л.Колено", 26: "П.Колено", 27: "Л.Лодыжка",
        28: "П.Лодыжка"
    }

    h, w = annotated_frame.shape[:2]
    mean_error = np.mean(list(metrics.values())) if metrics else 0
    accuracy = max(0, 100 - mean_error * 100)

    cv2.rectangle(annotated_frame, (0, 0), (w, 40), (0, 0, 0), -1)
    cv2.putText(annotated_frame, f"Accuracy: {accuracy:.1f}%", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                (255, 255, 255), 2)

    return annotated_frame

def get_error_color(error_value: float) -> Tuple[int, int, int]:
    if error_value < 0.3:
        return (0, 255, 0)
    elif error_value < 0.7:
        return (0, 255, int(255 * (error_value - 0.3) / 0.4))
    else:
        return (0, int(255 * (1 - (error_value - 0.7) / 0.3)), 255)
