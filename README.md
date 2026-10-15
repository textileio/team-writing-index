# Textile and Recall team writing

A local research catalogue of writing published by Textile, Tableland, Basin, and Recall, including historical Medium/Ghost posts, newsletters, migrated Mirror posts, and outside bylines. Ceramic/3Box history is included as a separate section.

Start with **[the Markdown index](INDEX.md)**.

- [Ceramic / 3Box history](indexes/ceramic-3box.md)
- [Linked articles and reading](indexes/linked-reading.md)
- [Historical URLs awaiting metadata](indexes/unresolved.md)
- [Coverage, evidence, and remaining gaps](research/coverage.md)
- [Machine-readable bibliography](data/catalogue.json)
- [Counts](research/counts.json)

Cross-posted editions are grouped when canonical URLs, Medium post IDs, or matching titles and nearby dates establish the connection. Original URLs, alternate editions, archive links, source references, and observed access failures are retained. Guest posts in official publications are included; inclusion does not establish that every contributor was an employee.

This is a bibliographic index, not a full-text backup. It does not claim to prove that every article ever written has been found. Inaccessible historical URLs and unresolved publication archives are recorded instead of silently omitted.

## Local status

Prepared locally for the proposed repository `textileio/team-writing-index`. No GitHub repository has been created and nothing has been pushed. Remote creation and push require the user's approval.

## Rebuild

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

Some supplemental metadata was extracted with the web reader after ordinary HTTP reads failed. Those observations are retained in `data/web-medium-*.json`; the collection scripts do not regenerate them. Bibliographic metadata and URLs are checked in. Cached article bodies, environments, and temporary downloads are ignored.
