# Maintaining the index

Run these commands from the repository root. The checked-in data records the October 15, 2026 research snapshot. Collectors retain the observation dates used for that run; review those dates and the response cache before starting a fresh survey.

## Rebuild the Markdown

Python 3.10 or newer:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_index.py
```

The checked-in JSON metadata is sufficient to rebuild the Markdown without network access. Re-running collection scripts makes public HTTP requests. They cache responses in ignored `.cache/`; HTTP errors are also cached, so remove only a failed response's cache file before a deliberate retry. No API credentials are required by the collectors.

Collection entry points:

```sh
.venv/bin/python scripts/research.py
.venv/bin/python scripts/history.py
.venv/bin/python scripts/ceramic.py
.venv/bin/python scripts/threebox_history.py
.venv/bin/python scripts/external.py
.venv/bin/python scripts/supplement.py
.venv/bin/python scripts/mirror.py
.venv/bin/python scripts/listings.py
.venv/bin/python scripts/linked.py
.venv/bin/python scripts/build_index.py
```

Some supplemental metadata was extracted with a web reader after ordinary HTTP reads failed. Those observations are retained in the checked-in web and reader JSON files; the collection scripts do not regenerate them. Bibliographic metadata and URLs are checked in. Cached article bodies, environments, and temporary downloads are ignored.
