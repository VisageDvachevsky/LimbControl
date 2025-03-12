import numpy as np
from scipy.spatial import distance
from typing import Dict, Any, List

class PoseComparison:
    def __init__(self) -> None:
        self.keypoint_weights: Dict[int, float] = {
            0: 0.5,      # Нос
            11: 1.0,     # Левое плечо
            12: 1.0,     # Правое плечо
            13: 1.0,     # Левый локоть
            14: 1.0,     # Правый локоть
            15: 1.2,     # Левое запястье
            16: 1.2,     # Правое запястье
            23: 0.8,     # Левое бедро
            24: 0.8,     # Правое бедро
            25: 1.0,     # Левое колено
            26: 1.0,     # Правое колено
            27: 1.0,     # Левая лодыжка
            28: 1.0      # Правая лодыжка
        }
        self.visibility_threshold: float = 0.65
        self.smoothing_window: int = 5
        self.previous_metrics: List[Dict[int, float]] = []
        self.score_history: List[float] = []
        self.max_history: int = 100

    def calculate_overall_accuracy(self, metrics: Dict[int, float]) -> float:
        if not metrics:
            return 0.0

        total_weighted_error: float = 0.0
        total_weight: float = 0.0

        for idx, error in metrics.items():
            idx_int: int = int(idx) if isinstance(idx, str) else idx
            weight: float = self.keypoint_weights.get(idx_int, 1.0)
            total_weighted_error += error * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0

        avg_error: float = total_weighted_error / total_weight
        accuracy: float = max(0.0, min(1.0, 1.0 - avg_error))
        return accuracy

    def compare_poses(self, reference_pose: Any, webcam_pose: Any) -> Dict[int, float]:
        if not reference_pose.pose_landmarks or not webcam_pose.pose_landmarks:
            return {}

        metrics: Dict[int, float] = {}
        ref_landmarks: Dict[int, Dict[str, float]] = self._get_normalized_landmarks(reference_pose.pose_landmarks)
        webcam_landmarks: Dict[int, Dict[str, float]] = self._get_normalized_landmarks(webcam_pose.pose_landmarks)

        for idx in self.keypoint_weights.keys():
            if idx in ref_landmarks and idx in webcam_landmarks:
                ref_point: Dict[str, float] = ref_landmarks[idx]
                webcam_point: Dict[str, float] = webcam_landmarks[idx]
                if ref_point['visibility'] < self.visibility_threshold or webcam_point['visibility'] < self.visibility_threshold:
                    continue
                dist_val: float = self._calculate_distance(ref_point, webcam_point)
                weighted_dist: float = dist_val * self.keypoint_weights[idx]
                metrics[idx] = weighted_dist

        return self._smooth_metrics(metrics)

    def _get_normalized_landmarks(self, pose_landmarks: Any) -> Dict[int, Dict[str, float]]:
        landmarks: Dict[int, Dict[str, float]] = {}
        for idx, landmark in enumerate(pose_landmarks.landmark):
            landmarks[idx] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }
        return landmarks

    def _calculate_distance(self, point1: Dict[str, float], point2: Dict[str, float]) -> float:
        p1 = np.array([point1['x'], point1['y']])
        p2 = np.array([point2['x'], point2['y']])
        dist_val: float = distance.euclidean(p1, p2)
        return min(1.0, dist_val)

    def _smooth_metrics(self, current_metrics: Dict[int, float]) -> Dict[int, float]:
        self.previous_metrics.append(current_metrics)
        if len(self.previous_metrics) > self.smoothing_window:
            self.previous_metrics.pop(0)

        smoothed_metrics: Dict[int, List[float]] = {}
        for metrics in self.previous_metrics:
            for idx, value in metrics.items():
                if idx not in smoothed_metrics:
                    smoothed_metrics[idx] = []
                smoothed_metrics[idx].append(value)

        for idx in list(smoothed_metrics.keys()):
            smoothed_metrics[idx] = float(np.mean(smoothed_metrics[idx]))
        return smoothed_metrics
