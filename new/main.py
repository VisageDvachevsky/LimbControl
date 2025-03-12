import sys
from PyQt5.QtWidgets import QApplication
from gui.app import TrackerApp

def main() -> None:
    app = QApplication(sys.argv)
    window = TrackerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
