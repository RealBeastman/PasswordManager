# app/views/saved_passwords.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt
from app.views.new_password import NewPasswordDialog


class SavedPasswordsWidget(QWidget):
    def __init__(self, fernet, parent=None):
        super().__init__(parent)
        self.fernet = fernet

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header with title and "Add" button
        header = QHBoxLayout()
        title = QLabel("Saved Passwords")
        title.setObjectName("sectionTitle")
        title.setAlignment(Qt.AlignLeft)

        add_button = QPushButton("➕ Add Password")
        add_button.clicked.connect(self.open_add_dialog)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(add_button)

        layout.addLayout(header)

        # Placeholder content
        placeholder = QLabel("No saved passwords yet.")
        placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(placeholder)

    def open_add_dialog(self):
        dialog = NewPasswordDialog(self.fernet, self)
        dialog.exec()
