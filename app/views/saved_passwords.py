from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt
from app.views.new_password import NewPasswordDialog
from app.views.components.password_list_item import PasswordListItem
from app.utils.db import SessionLocal
from app.models.password_entry import PasswordEntry


class SavedPasswordsWidget(QWidget):
    def __init__(self, fernet, parent=None):
        super().__init__(parent)
        self.fernet = fernet

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header: Title and Add Button
        header = QHBoxLayout()
        title = QLabel("Saved Passwords")
        title.setObjectName("sectionTitle")
        title.setAlignment(Qt.AlignLeft)

        add_button = QPushButton("New Password")
        add_button.clicked.connect(self.open_add_dialog)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(add_button)
        layout.addLayout(header)

        # Password List
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.load_passwords()

    def load_passwords(self):
        self.list_widget.clear()
        db = SessionLocal()
        entries = db.query(PasswordEntry).order_by(PasswordEntry.name).all()
        db.close()

        for entry in entries:
            item_widget = PasswordListItem(entry, self.fernet, self.load_passwords)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)

    def open_add_dialog(self):
        dialog = NewPasswordDialog(self.fernet, self)
        if dialog.exec():
            self.load_passwords()