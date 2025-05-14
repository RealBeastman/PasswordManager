# app/views/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFrame
)
from PySide6.QtCore import QSize
from app.views.saved_passwords import SavedPasswordsWidget

def framed_widget(widget, name: str) -> QFrame:
    frame = QFrame()
    frame.setObjectName(name)
    frame.setFrameShape(QFrame.StyledPanel)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.addWidget(widget)
    frame.setLayout(layout)
    return frame

class MainWindow(QMainWindow):
    def __init__(self, fernet):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.resize(QSize(1280, 720))

        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        # Only show SavedPasswordsWidget now
        right_panel = framed_widget(SavedPasswordsWidget(fernet), "SavedPasswordsPanel")
        layout.addWidget(right_panel)
