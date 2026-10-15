"""Check catalogue conservation, source inventories, and local index links."""
import datetime as dt
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import unquote

from build_index import ROOT, DAY, key
from audit_recovery import BASELINE_COMMIT


def read(path):
    return json.loads((ROOT / path).read_text())


def main():
    cat = read('data/catalogue.json')
    known = {key(e['url']) for a in cat for e in a['editions']}
    unresolved = {key(a['url']) for a in read('data/unresolved-urls.json')}
    excluded = {key(a['url']) for a in read('data/url-resolutions.json')}
    accounted = known | unresolved | excluded
    checks = {}
    for name, path, allow_candidates in [
        ('current_paragraph_posts', 'data/paragraph-listing-articles.json', False),
        ('ceramic_posts', 'data/ceramic-articles.json', False),
        ('substack_posts', 'data/substack-articles.json', False),
        ('historical_textile_medium_records', 'data/historical-articles.json', True),
        ('historical_3box_medium_records', 'data/3box-historical-articles.json', False),
    ]:
        expected = {key(a['url']) for a in read(path)}
        missing = expected - (accounted if allow_candidates else known)
        assert not missing, (name, sorted(missing))
        checks[name] = {'expected_urls': len(expected), 'all_accounted_for': True}
    sitemap = ET.fromstring((ROOT / 'research/textile-ghost-sitemap.xml').read_text())
    expected = {key(n.text) for n in sitemap.findall('./{*}url/{*}loc')}
    assert expected <= known, sorted(expected - known)
    checks['archived_ghost_sitemap'] = {'expected_urls': len(expected), 'all_catalogued': True}
    baseline = {key(a['url']) for a in read('research/recovery-pass-2/baseline-unresolved.json')}
    assert len(baseline) == 88
    assert not (known & unresolved or known & excluded or unresolved & excluded)
    assert baseline <= accounted
    checks['baseline_88_partition'] = {
        'catalogued': len(baseline & known), 'excluded': len(baseline & excluded),
        'unresolved': len(baseline & unresolved), 'disjoint_and_exhaustive': True}
    old = json.loads(subprocess.check_output(['git', 'show', BASELINE_COMMIT + ':data/catalogue.json'], cwd=ROOT, text=True))
    assert all(any(key(e['url']) in known for e in a['editions']) for a in old)
    checks['baseline_articles_preserved'] = {'entries': len(old), 'all_represented': True}
    owners = {}
    for index, a in enumerate(cat):
        assert isinstance(a['title'], str) and a['title'] and a['editions']
        assert not a['title'].startswith(('500:', '404:', 'Just a moment'))
        assert a['date'] is None or dt.date.fromisoformat(a['date']) <= dt.date.fromisoformat(DAY)
        assert all(isinstance(n, str) and n and not any(0xe000 <= ord(c) <= 0xf8ff for c in n) for n in a['authors'])
        for e in a['editions']:
            k = key(e['url'])
            assert '/web/' not in e['url'] and 'storage.ghost.io' not in e['url']
            assert k not in owners or owners[k] == index, ('Duplicate edition identity', k)
            owners[k] = index
            assert isinstance(e['sources'], list) and e['sources']
    checks['metadata_schema_and_unique_editions'] = True
    for a in read('data/recovery-pass-2-articles.json'):
        assert a.get('archive_url') and a.get('archive_status') == 200, ('Missing verified archive link', a['url'])
    checks['retry_reading_links_preserved'] = True
    missing_links = []
    pages = list(ROOT.glob('*.md')) + list((ROOT / 'indexes').rglob('*.md')) + list((ROOT / 'research').rglob('*.md'))
    for path in pages:
        for url in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if url.startswith(('https://', 'http://', '#')):
                continue
            if not (path.parent / unquote(url.split('#')[0])).exists():
                missing_links.append((str(path.relative_to(ROOT)), url))
    assert not missing_links, missing_links
    checks['local_markdown_links'] = True
    forbidden = {'body', 'body_html', 'body_json', 'content:encoded', 'raw_html'}
    def body_fields(value):
        if isinstance(value, dict):
            return bool(forbidden & value.keys()) or any(body_fields(v) for v in value.values())
        if isinstance(value, list):
            return any(body_fields(v) for v in value)
        return False
    for folder in ['data', 'research']:
        for path in (ROOT / folder).rglob('*.json'):
            assert not body_fields(json.loads(path.read_text())), ('Article body field', str(path))
    checks['article_bodies_excluded'] = True
    counts = read('research/counts.json')
    assert counts['distinct_articles'] == len(cat)
    assert counts['edition_urls'] == sum(len(a['editions']) for a in cat)
    assert counts['url_only_candidates'] == len(unresolved)
    assert counts['articles_without_publication_date'] == sum(not a['date'] for a in cat)
    checks['generated_counts'] = True
    result = {'checked': DAY, 'checks': checks}
    (ROOT / 'research/validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
