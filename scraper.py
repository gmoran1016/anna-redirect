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

    # URLs are in the infobox: find the <th> whose text is "URL" or "Website",
    # then extract https:// links from the sibling <td>.
    url_cell = None
    for th in soup.find_all("th"):
        if th.get_text(strip=True) in ("URL", "Website", "URLs"):
            url_cell = th.find_next_sibling("td")
            break

    if not url_cell:
        return []

    return [
        a["href"]
        for a in url_cell.find_all("a", href=True)
        if a["href"].startswith("https://") and "wikipedia.org" not in a["href"]
    ]
