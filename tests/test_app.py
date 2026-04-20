import time
import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def reset_cache():
    import app as a
    a._cached_url = None
    a._cache_time = None


def test_redirects_to_live_url(client):
    reset_cache()
    with patch("app.get_candidate_urls", return_value=["https://annas-archive.org"]), \
         patch("app.find_live_url", return_value="https://annas-archive.org"):
        resp = client.get("/")
    assert resp.status_code == 302
    assert resp.headers["Location"] == "https://annas-archive.org"


def test_uses_cache_on_second_request(client):
    reset_cache()
    with patch("app.get_candidate_urls", return_value=["https://annas-archive.org"]) as mock_scraper, \
         patch("app.find_live_url", return_value="https://annas-archive.org"):
        client.get("/")
        client.get("/")
    assert mock_scraper.call_count == 1


def test_503_when_wikipedia_unreachable(client):
    reset_cache()
    with patch("app.get_candidate_urls", side_effect=RuntimeError("Wikipedia returned HTTP 503")):
        resp = client.get("/")
    assert resp.status_code == 503
    assert b"Could not reach Wikipedia" in resp.data


def test_503_when_no_urls_parsed(client):
    reset_cache()
    with patch("app.get_candidate_urls", return_value=[]), \
         patch("app.find_live_url", return_value=None):
        resp = client.get("/")
    assert resp.status_code == 503
    assert b"Could not parse URLs from Wikipedia" in resp.data


def test_503_when_all_urls_dead(client):
    reset_cache()
    with patch("app.get_candidate_urls", return_value=["https://annas-archive.org"]), \
         patch("app.find_live_url", return_value=None):
        resp = client.get("/")
    assert resp.status_code == 503
    assert b"No live Anna" in resp.data


def test_cache_expires_after_ttl(client):
    reset_cache()
    with patch("app.get_candidate_urls", return_value=["https://annas-archive.org"]) as mock_scraper, \
         patch("app.find_live_url", return_value="https://annas-archive.org"), \
         patch("app.time") as mock_time:
        mock_time.time.return_value = 0.0
        client.get("/")
        mock_time.time.return_value = 3601.0
        client.get("/")
    assert mock_scraper.call_count == 2
