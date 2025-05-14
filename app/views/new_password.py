from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt
from app.utils.db import SessionLocal
from app.utils.encryption import encrypt
from app.models.password_entry import PasswordEntry
from app.utils.site_icon import get_favicon_local_path


class NewPasswordDialog(QDialog):
    def __init__(self, fernet, parent=None, existing_entry: PasswordEntry = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Password" if existing_entry else "Add New Password")
        self.fernet = fernet
        self.existing_entry = existing_entry
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("Edit Password" if existing_entry else "Add New Password")
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
        self.submit_button.clicked.connect(self.save_password)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # Pre-fill fields if editing
        if existing_entry:
            self.name_input.setText(existing_entry.name)
            self.url_input.setText(existing_entry.url or "")
            self.username_input.setText(existing_entry.username or "")
            self.password_input.setText("••••••••")  # Mask for security

    def save_password(self):
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not name:
            print("Name is required.")
            return

        # Only re-encrypt if the user typed a new password
        if self.existing_entry and password == "••••••••":
            encrypted_password = self.existing_entry.password
        else:
            if not password:
                print("Password is required.")
                return
            encrypted_password = encrypt(password, self.fernet)


        encrypted_password = encrypt(password, self.fernet)
        favicon_path = get_favicon_local_path(url) if url else None

        db = SessionLocal()
        if self.existing_entry:
            # Update existing entry
            self.existing_entry.name = name
            self.existing_entry.url = url
            self.existing_entry.username = username
            self.existing_entry.password = encrypted_password
            self.existing_entry.favicon_url = favicon_path
            db.add(self.existing_entry)
        else:
            # New entry
            entry = PasswordEntry(
                name=name,
                url=url,
                username=username,
                password=encrypted_password,
                favicon_url=favicon_path
            )
            db.add(entry)

        db.commit()
        db.close()

        print("✅ Password saved successfully.")
        self.accept()
