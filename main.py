import sys
from PySide6.QtWidgets import QApplication
from app.views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    with open("app/styles/dark_theme.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()

    exit_code = app.exec()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()