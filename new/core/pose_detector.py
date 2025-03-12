import cv2
import numpy as np
import mediapipe as mp
from typing import Any, Dict, Tuple

class PoseDetector:
    def __init__(self, detection_confidence: float = 0.5, tracking_confidence: float = 0.5) -> None:
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
    
    def detect_pose(self, frame: np.ndarray) -> Any:
        frame_rgb: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results: Any = self.pose.process(frame_rgb)
        return results
    
    def get_pose_landmarks(self, results: Any) -> Dict[int, Dict[str, float]]:
        landmarks_dict: Dict[int, Dict[str, float]] = {}
        if not results.pose_landmarks:
            return landmarks_dict
        
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            landmarks_dict[idx] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }
        return landmarks_dict
    
    def get_pose_angles(self, landmarks_dict: Dict[int, Dict[str, float]]) -> Dict[str, float]:
        angles_dict: Dict[str, float] = {}
        key_connections: Dict[str, list[int]] = {
            'left_elbow': [11, 13, 15],
            'right_elbow': [12, 14, 16],
            'left_shoulder': [13, 11, 23],
            'right_shoulder': [14, 12, 24],
            'left_hip': [11, 23, 25],
            'right_hip': [12, 24, 26],
            'left_knee': [23, 25, 27],
            'right_knee': [24, 26, 28]
        }
        
        for angle_name, points in key_connections.items():
            if all(p in landmarks_dict for p in points):
                p1, p2, p3 = points
                angle: float = self._calculate_angle(
                    (landmarks_dict[p1]['x'], landmarks_dict[p1]['y']),
                    (landmarks_dict[p2]['x'], landmarks_dict[p2]['y']),
                    (landmarks_dict[p3]['x'], landmarks_dict[p3]['y'])
                )
                angles_dict[angle_name] = angle
        
        return angles_dict
    
    def _calculate_angle(self, p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
        a: np.ndarray = np.array([p1[0] - p2[0], p1[1] - p2[1]])
        b: np.ndarray = np.array([p3[0] - p2[0], p3[1] - p2[1]])
        cos_angle: float = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle: float = np.arccos(cos_angle) * 180.0 / np.pi
        return angle
