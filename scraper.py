import requests
from bs4 import BeautifulSoup

WIKI_URL = "https://en.wikipedia.org/wiki/Anna%27s_Archive?oldformat=true"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AnnaRedirect/1.0)"}


def get_candidate_urls() -> list[str]:
    """Fetch Anna's Archive mirror URLs from the Wikipedia URL section.

    Returns external HTTPS URLs in order of appearance. Returns [] if the
    URL section is not found. Raises RuntimeError if Wikipedia is unreachable.
    """
    resp = requests.get(WIKI_URL, headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"Wikipedia returned HTTP {resp.status_code}")

    soup = BeautifulSoup(resp.text, "html.parser")

    url_heading = soup.find(id="URL") or soup.find(id="URLs")
    if not url_heading:
        return []

    urls = []
    for tag in url_heading.find_parent().find_all_next("a", href=True):
        href = tag["href"]
        if href.startswith("https://") and "wikipedia.org" not in href:
            urls.append(href)
        elif href.startswith("#") or href.startswith("/wiki/"):
            break
    return urls
