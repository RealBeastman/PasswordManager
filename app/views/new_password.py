# app/views/new_password.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt


class NewPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Password")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("Add New Password")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)

        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Service name (e.g., Gmail, GitHub)")
        layout.addWidget(self.name_input)

        # URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Homepage URL")
        layout.addWidget(self.url_input)

        # Username/Email
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or email")
        layout.addWidget(self.username_input)

        # Password + Generate
        password_row = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter or generate password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.generate_button = QPushButton("Generate")
        password_row.addWidget(self.password_input)
        password_row.addWidget(self.generate_button)
        layout.addLayout(password_row)

        # Save
        self.submit_button = QPushButton("Save Password")
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
