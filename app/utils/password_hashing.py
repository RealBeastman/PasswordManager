import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HASH_PATH = "app/data/hash.key"
SALT_PATH = "app/data/salt.bin"

def load_salt() -> bytes:
    with open(SALT_PATH, "rb") as f:
        return f.read()
    
def hash_password(password: str) -> str:
    salt = load_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode())).decode()

def save_hash(password: str):
    hashed = hash_password(password)
    with open(HASH_PATH, "w") as f:
        f.write(hashed)

def verify_password(password: str) -> bool:
    try:
        with open(HASH_PATH, "r") as f:
            stored_hash = f.read()
        return hash_password(password) == stored_hash
    except:
        return False