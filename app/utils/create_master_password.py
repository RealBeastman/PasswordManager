# app/utils/create_master_password.py

import os
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

SALT_PATH = "app/data/salt.bin"
KEY_OUTPUT_PATH = "app/data/derived_key.key"

def generate_or_load_salt() -> bytes:
    """Load existing salt or generate a new one if it doesn't exist or is invalid."""
    if os.path.exists(SALT_PATH):
        with open(SALT_PATH, "rb") as f:
            salt = f.read()
        if len(salt) == 16:
            return salt
        else:
            print("⚠️ Existing salt was invalid. Regenerating.")
    
    # Generate new 16-byte salt
    salt = os.urandom(16)
    with open(SALT_PATH, "wb") as f:
        f.write(salt)
    return salt

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible encryption key from the password + salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=150_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def main():
    print("🔐 Set your master password")
    password = getpass.getpass("Enter master password: ")
    confirm = getpass.getpass("Confirm master password: ")

    if password != confirm:
        print("❌ Passwords do not match.")
        return

    salt = generate_or_load_salt()
    derived_key = derive_key(password, salt)

    # Save the derived key
    with open(KEY_OUTPUT_PATH, "wb") as f:
        f.write(derived_key)

    print("✅ Master password key successfully derived and saved.")
    print(f"📁 Salt saved to: {SALT_PATH}")
    print(f"🔑 Key saved to: {KEY_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
