from app.utils.encryption import derive_key_from_password, load_salt
from cryptography.fernet import Fernet

def unlock_app(master_password: str) -> Fernet:
    salt = load_salt()
    key = derive_key_from_password(master_password, salt)
    return Fernet(key)