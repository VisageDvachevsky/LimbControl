from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from typing import Dict

class ScoreDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMaximumHeight(200)
        
        main_layout = QVBoxLayout(self)
        
        title_label = QLabel("Отклонения по ключевым точкам")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(title_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        self.style_good: str = "color: green; font-weight: bold;"
        self.style_medium: str = "color: orange;"
        self.style_bad: str = "color: red; font-weight: bold;"
        
        self.metrics_container = QWidget()
        self.metrics_layout = QHBoxLayout(self.metrics_container)
        scroll_area.setWidget(self.metrics_container)
        
        self.metric_labels: Dict[str, QLabel] = {}
        
        self.init_key_points()
    
    def init_key_points(self) -> None:
        key_points = [
            "Нос", "Левое плечо", "Правое плечо", "Левый локоть", "Правый локоть",
            "Левое запястье", "Правое запястье", "Левое бедро", "Правое бедро",
            "Левое колено", "Правое колено", "Левая лодыжка", "Правая лодыжка"
        ]
        
        for point in key_points:
            point_widget = QWidget()
            point_layout = QVBoxLayout(point_widget)
            
            point_name = QLabel(point)
            point_name.setAlignment(Qt.AlignCenter)
            point_value = QLabel("0.0")
            point_value.setAlignment(Qt.AlignCenter)
            
            point_layout.addWidget(point_name)
            point_layout.addWidget(point_value)
            
            self.metric_labels[point] = point_value
            self.metrics_layout.addWidget(point_widget)
    
    def update_scores(self, metrics: Dict[int, float]) -> None:
        index_to_name: Dict[int, str] = {
            0: "Нос", 
            11: "Левое плечо", 12: "Правое плечо",
            13: "Левый локоть", 14: "Правый локоть",
            15: "Левое запястье", 16: "Правое запястье",
            23: "Левое бедро", 24: "Правое бедро",
            25: "Левое колено", 26: "Правое колено",
            27: "Левая лодыжка", 28: "Правая лодыжка"
        }
        
        for idx, name in index_to_name.items():
            if idx in metrics:
                accuracy = max(0, 100 - metrics[idx] * 100)
                label = self.metric_labels[name]
                new_text = f"{accuracy:.1f}%"
                
                if label.text() != new_text:
                    label.setText(new_text)
                    if accuracy >= 90 and label.styleSheet() != self.style_good:
                        label.setStyleSheet(self.style_good)
                    elif 70 <= accuracy < 90 and label.styleSheet() != self.style_medium:
                        label.setStyleSheet(self.style_medium)
                    elif accuracy < 70 and label.styleSheet() != self.style_bad:
                        label.setStyleSheet(self.style_bad)
    
    def reset_scores(self) -> None:
        for label in self.metric_labels.values():
            label.setText("0.0")
            label.setStyleSheet("")
