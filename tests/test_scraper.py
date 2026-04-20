import responses
import requests
from scraper import get_candidate_urls

WIKI_URL = "https://en.wikipedia.org/wiki/Anna%27s_Archive?oldformat=true"

SAMPLE_HTML = """
<html><body>
<h2><span id="URL">URL</span></h2>
<ul>
  <li><a href="https://annas-archive.org">annas-archive.org</a></li>
  <li><a href="https://annas-archive.se">annas-archive.se</a></li>
  <li><a href="/wiki/InternalLink">internal</a></li>
</ul>
</body></html>
"""

NO_SECTION_HTML = """
<html><body>
<h2><span id="History">History</span></h2>
<p>Some text</p>
</body></html>
"""


@responses.activate
def test_returns_external_https_urls():
    responses.add(responses.GET, WIKI_URL, body=SAMPLE_HTML, status=200)
    urls = get_candidate_urls()
    assert urls == ["https://annas-archive.org", "https://annas-archive.se"]


@responses.activate
def test_excludes_wikipedia_internal_links():
    responses.add(responses.GET, WIKI_URL, body=SAMPLE_HTML, status=200)
    urls = get_candidate_urls()
    assert not any(u.startswith("/wiki/") for u in urls)


@responses.activate
def test_returns_empty_list_when_no_url_section():
    responses.add(responses.GET, WIKI_URL, body=NO_SECTION_HTML, status=200)
    urls = get_candidate_urls()
    assert urls == []


@responses.activate
def test_raises_on_wikipedia_http_error():
    responses.add(responses.GET, WIKI_URL, status=503)
    try:
        get_candidate_urls()
        assert False, "Expected exception"
    except Exception as e:
        assert "Wikipedia" in str(e)
