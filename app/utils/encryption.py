import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def load_salt():
    with open("app/data/salt.bin", "rb") as f:
        return f.read()
    
def derive_key_from_password(password:str, salt:bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=150000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt(plaintext: str, fernet: Fernet) -> bytes:
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt(ciphertext: str, fernet: Fernet) -> str:
    return fernet.decrypt(ciphertext.encode()).decode()