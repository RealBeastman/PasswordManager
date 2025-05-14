import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from hashlib import sha1

FAVICON_DIR = "app/assets/favicons"
DEFAULT_ICON = "app/assets/default_favicon.ico"

def get_favicon_url(homepage_url: str) -> str:
    """Try to get favicon URL from page <link> or fallback to /favicon.ico"""
    try:
        response = requests.get(homepage_url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for common favicon <link> rel attributes
        for rel_type in ["icon", "shortcut icon", "mask-icon", "apple-touch-icon"]:
            link = soup.find("link", rel=lambda x: x and rel_type in x.lower())
            if link and link.get("href"):
                return urljoin(homepage_url, link["href"])
    except Exception as e:
        print(f"[ERROR] Failed to extract favicon link: {e}")

    # Fallback: /favicon.ico
    parsed = urlparse(homepage_url)
    return f"{parsed.scheme}://{parsed.netloc}/favicon.ico"

def save_favicon(favicon_url: str) -> str:
    """Download favicon and return local path"""
    os.makedirs(FAVICON_DIR, exist_ok=True)

    parsed = urlparse(favicon_url)
    domain = parsed.netloc
    ext = os.path.splitext(favicon_url)[-1]
    ext = ext if ext else ".ico"
    key = sha1(domain.encode()).hexdigest()
    local_path = os.path.join(FAVICON_DIR, f"{key}{ext}")

    if os.path.exists(local_path):
        return local_path

    try:
        response = requests.get(favicon_url, timeout=5)
        if response.status_code == 200 and response.content:
            with open(local_path, "wb") as f:
                f.write(response.content)
            return local_path
    except Exception as e:
        print(f"[ERROR] Failed to save favicon: {e}")

    return DEFAULT_ICON

def get_favicon_local_path(homepage_url: str) -> str:
    """Returns a local path to the downloaded favicon, or a default"""
    url = get_favicon_url(homepage_url)
    return save_favicon(url)
