# Password Manager

> A secure, modern GUI password manager built with Python and PySide6.

---

## Overview

This application provides a local password vault with encryption, a professional PySide6 interface, and a clean structure for future expansion. It was built to practice GUI design, database integration, and cryptographic security — all without relying on third-party password services.

---

## Features

- Master password unlock screen
- Add, view, edit, and delete password entries
- Clipboard copy functionality
- Encrypted password storage (Fernet + hashed key)
- SQLite database using SQLAlchemy
- Clean PySide6 GUI with a dark theme
- Structured for scalability (MVC-inspired)

---

## Usage

### Run Locally

```bash
# Clone the repo
git clone https://github.com/RealBeastman/PasswordManager.git
cd PasswordManager

# Set up a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt # Future addition, not currently available

# Launch the application
python main.py
```

---

## File Structure

```
PasswordManager/
├── main.py
├── requirements.txt
├── .env
├── views/
├── utils/
├── models/
└── app/data/passwords.db
```

---

## Requirements

- Python 3.10+
- `PySide6`
- `cryptography`
- `SQLAlchemy`

---

## Status

🟢 **Active Development** — This project is still evolving with regular improvements.

---

## License

MIT License

---

## Author

Joshua Eastman — [contact@joshuaeastman.dev](mailto:contact@joshuaeastman.dev)
