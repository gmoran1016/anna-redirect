import requests


def find_live_url(urls: list[str]) -> str | None:
    for url in urls:
        try:
            resp = requests.head(url, timeout=5, allow_redirects=True)
            if resp.status_code < 400:
                return url
        except requests.exceptions.RequestException:
            continue
    return None
