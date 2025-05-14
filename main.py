import os
import sys
from PySide6.QtWidgets import QApplication, QInputDialog, QLineEdit, QMessageBox
from app.utils.auth import unlock_app
from app.views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    with open("app/styles/dark_theme.qss", "r") as f:
        app.setStyleSheet(f.read())

    password, ok = QInputDialog.getText(None, "Unlock Vault", "Master Password:", QLineEdit.Password)
    if not ok or not password:
        sys.exit()

    try:
        fernet = unlock_app(password)
    except Exception:
        QMessageBox.critical(None, "Access Denied", "Invalid password.")
        sys.exit()

    window = MainWindow(fernet)
    window.show()
    sys.exit(app.exec())

def setup_password():
    from app.utils.password_hashing import save_hash
    import os

    def create_salt():
        if not os.path.exists("app/data/salt.bin"):
            with open("app/data/salt.bin", "wb") as f:
                f.write(os.urandom(16))

    create_salt()

    password = input("Enter a new master password: ")
    confirm = input("Confirm the master password: ")

    if password != confirm:
        print("Passwords do not match.")
    else:
        save_hash(password)
        print("Master password saved.")

def setup_database():
    from app.utils.db import Base, engine
    from app.models.password_entry import PasswordEntry
    Base.metadata.create_all(engine)
    print("Database setup complete.")


if __name__ == "__main__":
    if not os.path.exists("app/data/hash.key"):
        setup_password()
    else:
        print("Master password already set.")

    if not os.path.exists("app/data/passwords.db"):
        setup_database()
    else:
        print("Database already exists.")

    main()
