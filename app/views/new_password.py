from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt
from app.utils.db import SessionLocal
from app.utils.encryption import encrypt
from app.models.password_entry import PasswordEntry
from app.utils.site_icon import get_favicon_url


class NewPasswordDialog(QDialog):
    def __init__(self, fernet, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Password")
        self.fernet = fernet
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
        self.submit_button.clicked.connect(self.save_password)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def save_password(self):
        # Obtain the data from the input fields
        name = self.name_input.text()
        url = self.url_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not name or not password:
            print("Name and password are required.")
            return
        
        # Encrypt the password
        encrypted_password = encrypt(password, self.fernet)

        # Create a new PasswordEntry object and save to db
        db = SessionLocal()
        entry = PasswordEntry(
            name=name,
            url=url,
            username=username,
            password=encrypted_password,
            favicon_url=get_favicon_url(url) if url else None
        )
        db.add(entry)
        db.commit()
        db.close()

        print("Password saved successfully.")
        self.accept() # Close the dialog
