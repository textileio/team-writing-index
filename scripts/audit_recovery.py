"""Reconcile the second pass against its immutable 88-URL baseline."""
import collections
import json
import subprocess
from pathlib import Path

from build_index import ROOT, DAY, key, link

OUT = ROOT / 'research/recovery-pass-2'
BASELINE_COMMIT = '160ce4a7de47ae9f4da8fdcda208a13a23628f30'


def main():
    old = json.loads(subprocess.check_output(['git', 'show', BASELINE_COMMIT + ':data/catalogue.json'], cwd=ROOT, text=True))
    catalogue = json.loads((ROOT / 'data/catalogue.json').read_text())
    baseline = json.loads((OUT / 'baseline-unresolved.json').read_text())
    counts = json.loads((ROOT / 'research/counts.json').read_text())
    oldkeys = {key(e['url']) for a in old for e in a['editions']}
    indexed = {key(e['url']): a for a in catalogue for e in a['editions']}
    unresolved = {key(a['url']) for a in json.loads((ROOT / 'data/unresolved-urls.json').read_text())}
    exclusions = {key(a['url']): a for a in json.loads((ROOT / 'data/url-resolutions.json').read_text())}
    added = [a for a in catalogue if not any(key(e['url']) in oldkeys for e in a['editions'])]
    ledger = []
    for candidate in baseline:
        url = candidate['url']
        k = key(url)
        assert sum([k in indexed, k in unresolved, k in exclusions]) == 1, url
        if k in indexed:
            a = indexed[k]
            ledger.append({'url': url, 'outcome': 'catalogued', 'title': a['title'], 'date': a['date'],
                           'new_work': not any(key(e['url']) in oldkeys for e in a['editions']),
                           'editions': a['editions']})
        elif k in exclusions:
            ledger.append(dict(exclusions[k], outcome=exclusions[k]['classification']))
        else:
            ledger.append({'url': url, 'outcome': 'unresolved', 'note': 'Title, byline, and publication date not verified for this edition.'})
    merged = []
    for a in catalogue:
        keys = {key(e['url']) for e in a['editions']}
        prior = [b for b in old if any(key(e['url']) in keys for e in b['editions'])]
        if len(prior) > 1:
            merged.append({'title': a['title'], 'prior_entries': [{'title': b['title'], 'date': b['date']} for b in prior],
                           'evidence': sorted({u for e in a['editions'] for u in e['sources']})})
    summary = {'checked': DAY, 'baseline_commit': BASELINE_COMMIT, 'baseline_candidates': len(baseline),
               'outcomes': dict(collections.Counter(a['outcome'] for a in ledger)),
               'new_works': len(added), 'new_works_by_collection': dict(collections.Counter(a['collection'] for a in added)),
               'baseline_entries_merged': merged, 'net_article_increase': len(catalogue) - len(old),
               'counts': counts}
    (OUT / 'url-outcomes.json').write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + '\n')
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
    def reading(a):
        return next((e['archive_url'] for e in a['editions'] if e.get('archive_url')), a['editions'][0]['url'])
    lines = ['# Second-pass recovery and completeness audit', '', f'Checked {DAY}. Baseline: commit `{BASELINE_COMMIT[:7]}`, 445 articles, 565 edition URLs, and 88 unresolved URLs.', '',
        '## Result', '',
        f'**{len(added)} additional works recovered**: 35 Textile / Tableland / Basin and five 3Box posts. The catalogue now contains **484 distinct works across 621 edition URLs**. One pair of existing entries was confirmed to be the same work, so the net increase is 39.', '',
        '| Outcome for the original 88 URLs | Count |', '| --- | ---: |',
        '| Accounted for in the catalogue | 56 |', '| Non-article routes excluded | 23 |', '| Malformed paths excluded | 2 |', '| Still unresolved | 7 |', '| **Total** | **88** |', '',
        'The 56 catalogue URLs include alternate editions as well as new works. They are not 56 new articles. Every original URL has an outcome in [the reconciliation ledger](url-outcomes.json); the [baseline](baseline-unresolved.json) is retained.', '',
        'The excluded routes comprise 19 width-parameter paths, two publication landing routes, a newsletter signup, and a Powergate request form. One sampled width route replays the publication homepage; the other width variants are excluded by that route pattern and absence from publication inventories. All 19 currently return 404. The two malformed paths append a backslash to an already indexed article URL. Exclusions are preserved in [url-resolutions.json](../../data/url-resolutions.json).', '',
        '## What recovered the posts', '',
        '- Retried ordinary requests in a separate cache, preserving the first survey and its failures.',
        '- Queried later CDX captures, and tried raw and standard Wayback replay URLs over both HTTP and HTTPS. Several early snapshots failed while another capture or replay form succeeded.',
        '- Read archived Ghost pages that retain their original Medium canonical URLs. These established edition identity directly, including several Medium pages that could not be read at their publication URL.',
        '- Revisited 20 undated entries: 14 exposed publication dates in an archived article. Six dates remain unknown; capture dates were not substituted.',
        '- Found an original Medium canonical URL connecting “Thread subscriptions” and “Thread streams.” Those two earlier catalogue entries are now one work.',
        '- Corrected the IDX article date to October 23, 2020 after re-reading its header. The earlier May 10, 2021 extraction had used a publication-footer date.', '',
        'The catalogue now also retains source-level date observations for each edition. Two editions still have differing publication dates in their primary sources; those observations remain visible rather than being silently discarded.', '',
        '## Additional recovered works', '', '| Publication date | Work | Collection |', '| --- | --- | --- |']
    for a in added:
        lines.append('| ' + (a['date'] or 'Unknown') + ' | ' + link(a['title'], reading(a)) + ' | ' + a['collection'] + ' |')
    lines += ['', '## Seven unresolved editions', '',
        'These remain Medium URL candidates. A similarly named Ghost article exists for the AltConf URL, but that identity has not been established by a canonical link or an accessible Medium record. The other six may contain writing absent from the catalogue. URL slugs are discovery leads, not verified titles.', '',
        '| Candidate | Status |', '| --- | --- |']
    for a in ledger:
        if a['outcome'] == 'unresolved':
            lines.append('| ' + link(a['url'], a['url']) + ' | No verified metadata for this edition |')
    lines += ['', '## What still makes the archive incomplete', '',
        '1. **The repository is a bibliography, not a durable full-text archive.** Article bodies and images are only present in ignored local HTTP caches or on the original/archive services. The repository alone cannot reconstruct every post offline. HTTP 200 and a title do not prove that an entire article and its assets have been preserved.',
        '2. **Publisher lifetime totals remain unverified.** The checked publication inventories are accounted for, including the 140-post Ghost sitemap, but CDX and platform migrations do not prove that deleted or never-captured posts are represented. Ghost, Medium, Paragraph/Mirror, and Substack exports would provide stronger reconciliation.',
        '3. **External author archives are not exhaustive.** The public author-route sweep found no additional in-scope post IDs beyond those already catalogued or flagged, but it is not a complete survey of every past contributor or personal account. Five earlier author-route leads, including apparent short responses and pre-Textile mapping posts, are retained in [author-candidates.json](author-candidates.json) for scope review. These have not been counted as company writing.',
        '4. **Outbound citations depend on accessible bodies.** This pass expanded the outbound inventory from 2,844 to 3,419 URLs, and linked reading from 233 to 270 destinations; 74 have article metadata, up from 66. Unread article bodies, client-rendered embeds, and lost attachments can still conceal links. A citation does not establish team authorship.',
        '5. **Some attribution and dates were lost or changed in migrations.** Six works have no verified publication date. Company bylines can mask original contributors; conflicting source dates and edition-specific provenance are retained.', '',
        'Additional CDX queries for `blog.3box.io` and `blog.textile.photos` returned successful empty inventories. That is an observed query result, not evidence that those hosts never published anything. See [additional CDX observations](additional-cdx-observations.json).', '',
        'The next useful preservation step is to reconcile publishing exports and a contributor/account roster, then save article text and assets with per-file provenance and checksums. That would make completeness and offline readability measurable.', '',
        '## Verification', '',
        'All 88 baseline URLs are partitioned exactly once between the catalogue, exclusions, and the remaining candidates. The current publication inventories and archived Ghost sitemap are reconciled in [validation.json](../validation.json). Rebuild and collection commands are documented in [maintaining.md](../maintaining.md).', '']
    (OUT / 'report.md').write_text('\n'.join(lines))
    print(json.dumps({k: v for k, v in summary.items() if k not in ['baseline_entries_merged', 'counts']}, indent=2))


if __name__ == '__main__':
    main()
