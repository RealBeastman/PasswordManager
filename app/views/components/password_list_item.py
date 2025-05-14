from PySide6.QtWidgets import (
     QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox, 
     QApplication, QVBoxLayout
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
        self.setObjectName("listItemFrame")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)  # More breathing room
        layout.setSpacing(20)  # Padding between elements

        # Favicon
        self.favicon_label = QLabel()
        self.favicon_label.setFixedSize(32, 32)
        if self.entry.favicon_url:
            pixmap = QPixmap(self.entry.favicon_url)
        else:
            pixmap = QPixmap("app/assets/favicons/default_favicon.png")
        self.favicon_label.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.favicon_label)

        # Label group layout (stacked left section)
        label_layout = QVBoxLayout()
        label_layout.setSpacing(2)

        self.name_label = QLabel()
        self.name_label.setTextFormat(Qt.RichText)
        self.name_label.setText(f"🔒 <b>{entry.name}</b>")
        self.username_label = QLabel(f"👤 {entry.username}")
        self.url_label = QLabel(f"🌐 {entry.url}")

        for lbl in [self.name_label, self.username_label, self.url_label]:
            lbl.setStyleSheet("color: #ccc; font-size: 13px;")
            label_layout.addWidget(lbl)

        layout.addLayout(label_layout)
        layout.addStretch()

        # Action buttons
        self.copy_button = QPushButton("🔑 Copy")
        self.copy_button.clicked.connect(self.copy_password)

        self.edit_button = QPushButton("✏️ Edit")
        self.edit_button.clicked.connect(self.edit_password)

        self.delete_button = QPushButton("🗑️ Delete")
        self.delete_button.clicked.connect(self.delete_password)

        for btn in [self.copy_button, self.edit_button, self.delete_button]:
            layout.addWidget(btn)


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