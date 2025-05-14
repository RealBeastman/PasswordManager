import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def get_favicon_url(homepage_url: str) -> str | None:
    try:
        response = requests.get(homepage_url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Prioritize exact match: rel="icon", rel="shortcut icon", etc.
        for rel_type in ["icon", "shortcut icon", "mask-icon", "apple-touch-icon"]:
            icon_link = soup.find("link", rel=lambda x: x and rel_type in x.lower())
            if icon_link and icon_link.get("href"):
                return urljoin(homepage_url, icon_link["href"])

        # Fallback to default
        parsed = urlparse(homepage_url)
        return f"{parsed.scheme}://{parsed.netloc}/favicon.ico"
    except Exception as e:
        print(f"[ERROR] Failed to fetch favicon: {e}")
        return None