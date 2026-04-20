# Anna Redirect

A bookmarkable URL that always redirects to a live [Anna's Archive](https://en.wikipedia.org/wiki/Anna%27s_Archive) mirror.

When you visit it, the service fetches the current mirror URLs from Wikipedia, checks which ones are reachable, and redirects you to the first live one. The result is cached for 1 hour so Wikipedia isn't hit on every request.

## How it works

1. `GET /` is received
2. If a live URL is cached and less than 1 hour old → immediate `302` redirect
3. Otherwise: scrape the **URL section** of the [Anna's Archive Wikipedia article](https://en.wikipedia.org/wiki/Anna%27s_Archive?oldformat=true), HEAD-check each candidate, cache the first live one, redirect

Returns `503` with a plain-text message if Wikipedia is unreachable or no live mirror is found.

## Installing on Unraid

1. Go to the **Docker** tab
2. Scroll to the bottom and click **ADD CONTAINER**
3. Fill in the following fields:
   - **Name:** `AnnaRedirect`
   - **Repository:** `ghcr.io/gmoran1016/anna-redirect:latest`
   - **Network Type:** Bridge
4. Click **Add another Path, Port, Variable, Label or Device**
   - Type: `Port`
   - Name: `Web UI`
   - Container Port: `5000`
   - Host Port: `5000`
   - Protocol: `TCP`
5. Click **Apply**

Bookmark `http://<unraid-ip>:5000/`.

## Running with Docker manually

```bash
docker run -d -p 5000:5000 ghcr.io/gmoran1016/anna-redirect:latest
```

The port is configurable via the `PORT` environment variable:

```bash
docker run -d -p 8080:8080 -e PORT=8080 ghcr.io/gmoran1016/anna-redirect:latest
```

Bookmark `http://<your-server-ip>:<port>/`.

## Versioning

The current version is defined in `version.py`:

```python
VERSION = "1.0.0"
```

It appears in startup and redirect logs. Bump it before each push:

```bash
# edit version.py, then:
git add version.py
git commit -m "v1.1.0 — describe what changed"
git push
git tag v1.1.0 && git push origin v1.1.0
```

## Development

```bash
pip install -r requirements.txt
pytest -v
```

All 16 tests run offline using mocked HTTP — no real network calls needed.
