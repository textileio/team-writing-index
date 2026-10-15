# Coverage and evidence

Research date: **2026-10-15**. Counts and unresolved URL totals are generated in [counts.json](counts.json).

Ceramic and 3Box publications are included as a separate historical section.

The [second-pass recovery audit](recovery-pass-2/report.md) reconciles the original 88 unresolved URLs: **56 are now catalogued, 25 are excluded routes, and seven remain unresolved**. It added 40 works and merged one existing duplicate, bringing the total to 484. Fourteen previously undated entries gained verified publication dates; six remain undated.

## Publications and discovery routes

| Source | Enumeration and evidence | Scope and limits |
| --- | --- | --- |
| [Textile blog](https://blog.textile.io/) | Both sitemaps, all eight pagination pages, RSS, and rendered publication-card metadata | All **77** currently listed post URLs captured. Five article pages returned HTTP 500; their bibliographic fields were recovered from publication cards. |
| [Recall blog](https://blog.recall.network/) | Sitemaps, pagination, and RSS | All **19** currently listed posts captured. The Recall homepage's blog links were reconciled with this publication. |
| [Textile on Medium](https://medium.com/textileio) | Publication overview/about, public author profiles/feeds, Internet Archive CDX, accessible articles, and web-reader metadata | CDX exposed **86** distinct article-shaped publication URLs. This is an observed archive inventory, not a publisher-confirmed lifetime total. Some live pages reject HTTP clients; web-reader evidence is retained separately. |
| Textile's former Ghost blog | [Archived sitemap](https://web.archive.org/web/20220827033537/https://blog.textile.io/sitemap-posts.xml), CDX URL inventory, archived articles, and historical publication listings | All **140** post URLs in the preserved sitemap are now represented in the catalogue. CDX also exposes later URLs and aliases. This accounts for that sitemap, not the publisher's lifetime total. |
| [Tableland Weeknotes on Substack](https://tableland.substack.com/) | Public archive API, article metadata, RSS | All **23** entries returned by the public archive endpoint captured; the final page contains fewer than the requested 50 entries. Exact dates and bylines come from its archive records. |
| [Tableland's migrated Mirror publication](https://paragraph.com/@tableland-2) | Original `mirror.xyz/tableland.eth/...` links followed into Paragraph; sitemaps, all three pagination pages, RSS, and publication cards | All **30** currently listed post URLs captured. The separate [@tableland publication](https://paragraph.com/@tableland) contributes another **2** listed posts. Migration aliases are retained where observed in source links. |
| [Ceramic blog](https://blog.ceramic.network/) | Complete post sitemap and individual article metadata | All **153** post URLs captured. Image locations inside the sitemap are excluded. Kept in the separate related-history section. |
| [3Box on Medium](https://medium.com/3box) | Public RSS feed, CDX inventory, archived articles, and primary-source web reads | All **78** article-shaped Medium URLs enumerated from **362** CDX rows are now represented in the catalogue, supplemented by the latest ten feed entries and primary-source search/reader records. The old `blog.3box.io` host is unavailable; an additional CDX query returned an empty inventory. CDX is an observed historical inventory, not a publisher-confirmed lifetime total. |
| Outside publishers | Author profiles/feeds, article citations, focused byline searches, and individual article metadata | Includes verified appearances on freeCodeCamp and HackerNoon. A quote in a press article is not treated as a team-authored post. Unlinked articles on undiscovered accounts remain an open discovery gap. |
| Linked reading | Article-body links from accessible company posts | Article-shaped destinations are indexed with referring posts and access status. The complete unfiltered URL inventory is preserved in `data/outbound-links.json`. These links do not by themselves establish team authorship. |

## Requested entry points

[Seed observations](seed-status.json) preserve final URLs and HTTP results for every requested entry point, plus discovered publications.

- [textile.io](https://textile.io/) and [recalllabs.ai](https://recalllabs.ai/) redirect to [Recall Labs on Linktree](https://linktr.ee/recalllabs).
- [Recall's homepage](https://recall.network/) links to the Recall publication.
- [Textile's Linktree](https://linktr.ee/textileio) and Recall Labs' Linktree currently expose company, team, jobs, and social links. Linktree's unrelated discovery recommendations and platform marketing articles are excluded.
- The old [Tableland blog route](https://tableland.xyz/blog) also redirects to Linktree. Its old website source points to `blog.textile.io`, supporting inclusion of Tableland/Basin content there.
- The old [Mirror publication root](https://mirror.xyz/tableland.eth) redirects to the generic Paragraph homepage, while individual Mirror post URLs still resolve to `@tableland-2` articles. Following only the root would have missed this collection.

## What the index means

1. A confirmed article has a title supported by an article page, feed, or publication listing. Unknown publication dates remain unknown.
2. Dates from `datePublished`, feeds, or a publication card are distinguished from sitemap modification dates and archive capture timestamps.
3. Migrated company bylines are preserved. They do not establish the identity of the original individual author.
4. Canonical URLs and Medium IDs establish duplicate editions directly. Matching normalized titles within 45 days, or with one unknown date, provide an additional grouping rule; this is a bibliographic inference, not a full-text equality check. Edition-specific dates, source-level date observations, and sources remain available in JSON. Two editions currently have differing source dates.
5. HTTP status describes the ordinary client observation. A web reader can establish article metadata even when that client received HTTP 403. An archive reading link is supplied only after a successful metadata read, except in the explicitly unverified historical candidate appendix.
6. Only titles, bibliographic fields, URLs, link provenance, and public archive metadata are included in the repository. Article bodies remain in ignored local response caches.

## Remaining gaps

- Article text and images are not preserved in the repository. Reading links and ignored local HTTP caches do not make it an independently readable full-text archive.

- The 3Box Medium CDX inventory and the preserved Ghost sitemap are accounted for, but public archives do not prove a complete lifetime total. Successful empty CDX queries for `blog.3box.io` and `blog.textile.photos` do not prove that those hosts never published anything.

- Seven [URL-only candidates](../indexes/unresolved.md), all on Medium, have CDX evidence but still lack confirmed article metadata. They are retained and excluded from confirmed article counts. One has a similarly named Ghost counterpart; its identity is still unverified.
- Ghost-era posts absent from the current Paragraph migration need a complete publisher export or reliably accessible archive replay to establish all dates/bylines and extract every outbound link.
- Medium and Internet Archive access is uneven. Failed reads do not establish that a post was deleted or that a collection is empty.
- A public-web survey cannot establish a definitive lifetime total for unlinked, unpublished, deleted, private, or undiscovered personal-account articles. No private publishing exports were accessed.
- A complete contributor/account roster and publisher exports remain the strongest next inputs. Pre-company personal writing and short Medium responses discovered in the author-route sweep are retained as research leads, not counted as company posts.

## Reproducibility

The checked-in per-source JSON records feed `scripts/build_index.py`. `data/catalogue.json` groups editions while preserving their individual sources and access observations. `research/*coverage.json`, the CDX inventories, the archived Ghost sitemap, and `seed-status.json` provide the discovery ledger. The raw CDX tables are URL/capture metadata, not article content.
