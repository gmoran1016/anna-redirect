import time
import logging
import os
from flask import Flask, redirect
from scraper import get_candidate_urls
from checker import find_live_url

VERSION = "1.0.2"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

log.info("Starting Anna Redirect v%s", VERSION)

app = Flask(__name__)

CACHE_TTL = 3600

_cached_url: str | None = None
_cache_time: float | None = None


@app.route("/")
def redirect_to_anna():
    global _cached_url, _cache_time

    now = time.time()
    if _cached_url and _cache_time and (now - _cache_time) < CACHE_TTL:
        log.info("[v%s] Redirecting to %s (cached)", VERSION, _cached_url)
        return redirect(_cached_url, code=302)

    try:
        candidates = get_candidate_urls()
    except Exception as e:
        log.error("[v%s] Wikipedia fetch failed: %s", VERSION, e)
        return "Could not reach Wikipedia", 503

    if not candidates:
        log.error("[v%s] No URLs found in Wikipedia URL section", VERSION)
        return "Could not parse URLs from Wikipedia", 503

    live = find_live_url(candidates)
    if not live:
        log.error("[v%s] All candidate URLs are unreachable", VERSION)
        return "No live Anna's Archive URL found", 503

    _cached_url = live
    _cache_time = now
    log.info("[v%s] Cache refreshed: %s", VERSION, live)
    log.info("[v%s] Redirecting to %s", VERSION, live)
    return redirect(live, code=302)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
