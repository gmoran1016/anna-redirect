import responses
from checker import find_live_url


@responses.activate
def test_returns_first_live_url():
    responses.add(responses.HEAD, "https://annas-archive.org", status=200)
    result = find_live_url(["https://annas-archive.org", "https://annas-archive.se"])
    assert result == "https://annas-archive.org"


@responses.activate
def test_skips_dead_url_and_returns_next():
    responses.add(responses.HEAD, "https://annas-archive.org", status=503)
    responses.add(responses.HEAD, "https://annas-archive.se", status=200)
    result = find_live_url(["https://annas-archive.org", "https://annas-archive.se"])
    assert result == "https://annas-archive.se"


@responses.activate
def test_returns_none_when_all_dead():
    responses.add(responses.HEAD, "https://annas-archive.org", status=503)
    responses.add(responses.HEAD, "https://annas-archive.se", status=503)
    result = find_live_url(["https://annas-archive.org", "https://annas-archive.se"])
    assert result is None


@responses.activate
def test_returns_none_for_empty_list():
    result = find_live_url([])
    assert result is None


@responses.activate
def test_accepts_3xx_as_live():
    responses.add(responses.HEAD, "https://annas-archive.org", status=301)
    result = find_live_url(["https://annas-archive.org"])
    assert result == "https://annas-archive.org"


def test_handles_connection_error(mocker):
    import requests as req
    mocker.patch("checker.requests.head", side_effect=req.exceptions.ConnectionError)
    result = find_live_url(["https://annas-archive.org"])
    assert result is None
