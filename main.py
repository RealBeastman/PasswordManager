import sys
from PySide6.QtWidgets import QApplication, QInputDialog, QLineEdit, QMessageBox
from app.utils.auth import unlock_app
from app.views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Prompt for master password
    password, ok = QInputDialog.getText(None, "Unlock Vault", "Enter Master Password:", QLineEdit.Password)
    if not ok or not password:
        sys.exit()

    try:
        fernet = unlock_app(password)
    except Exception:
        QMessageBox.critical(None, "Error", "Invalid master password.")
        sys.exit()

    # Load main window with fernet
    window = MainWindow(fernet)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()