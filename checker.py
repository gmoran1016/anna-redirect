import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AnnaRedirect/1.0)"}


def find_live_url(urls: list[str]) -> str | None:
    """Check each URL and return the first that responds with HTTP < 400."""
    for url in urls:
        try:
            resp = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
            if resp.status_code < 400:
                return url
        except requests.exceptions.RequestException:
            continue
    return None
