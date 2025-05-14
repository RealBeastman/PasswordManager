from PySide6.QtWidgets import (
     QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox, 
     QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from app.views.new_password import NewPasswordDialog
from app.utils.db import SessionLocal
from app.utils.encryption import decrypt
from app.models.password_entry import PasswordEntry

class PasswordListItem(QWidget):
    def __init__(self, entry: PasswordEntry, fernet, refresh_callback, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.fernet = fernet
        self.refresh_callback = refresh_callback

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Password Entry Favicon
        self.favicon_label = QLabel()
        self.favicon_label.setFixedSize(24, 24)
        if self.entry.favicon_url:
            pixmap = QPixmap(self.entry.favicon_url)
        else:
            pixmap = QPixmap("app/assets/favicons/default_favicon.png")
        self.favicon_label.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.favicon_label)

        # Password Entry Name
        self.name_label = QLabel(entry.name)
        layout.addWidget(self.name_label)

        # Password Entry Username
        self.username_label = QLabel(entry.username)
        layout.addWidget(self.username_label)

        # Password Entry URL
        self.url_label = QLabel(entry.url)
        layout.addWidget(self.url_label)
        layout.addStretch()

        # Copy Button
        self.copy_button = QPushButton("🔑 Copy")
        self.copy_button.clicked.connect(self.copy_password)
        layout.addWidget(self.copy_button)

        # Edit Button
        self.edit_button = QPushButton("✏️ Edit")
        self.edit_button.clicked.connect(self.edit_password)
        layout.addWidget(self.edit_button)

        # Delete Button
        self.delete_button = QPushButton("🗑️ Delete")
        self.delete_button.clicked.connect(self.delete_password)
        layout.addWidget(self.delete_button)

    def copy_password(self):
        try:
            decrypted_password = decrypt(self.entry.password, self.fernet)
            QApplication.clipboard().setText(decrypted_password)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to decrypt password: {str(e)}")

    def edit_password(self):
        dialog = NewPasswordDialog(self.fernet, self, existing_entry=self.entry)
        if dialog.exec():
            self.refresh_callback()

    def delete_password(self):
        confirm = QMessageBox.question(
            self, "Delete", f"Delete password for {self.entry.name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            db = SessionLocal()
            db.delete(self.entry)
            db.commit()
            db.close()
            self.refresh_callback()