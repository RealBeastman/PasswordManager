from cryptography.fernet import Fernet
from app.utils.password_hashing import verify_password
from app.utils.encryption import get_fernet

def unlock_app(master_password: str) -> Fernet:
    if not verify_password(master_password):
        raise ValueError("Invalid master password.")
    return get_fernet(master_password)