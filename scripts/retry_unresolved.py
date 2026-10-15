"""Second-pass public reads, preserving the first survey and every retry result.

Raw responses remain ignored. The checked-in observations contain metadata only.
Run with --refresh to retry this pass's cached failures deliberately.
"""
import concurrent.futures as cf
import hashlib
import json
import re
import sys
from urllib.parse import urljoin, urlsplit

import requests
from research import ROOT, DAY, metadata, BeautifulSoup

OUT = ROOT / 'research/recovery-pass-2'
CACHE = ROOT / '.cache/recovery-pass-2'
CACHE.mkdir(exist_ok=True)
REFRESH = '--refresh' in sys.argv


def read(url):
    path = CACHE / (hashlib.sha256(url.encode()).hexdigest() + '.json')
    if path.exists() and not REFRESH:
        return json.loads(path.read_text())
    try:
        r = requests.get(url, timeout=25, headers={'User-Agent': 'TeamWritingIndex/1.0 (public bibliographic research)'})
        result = {'url': url, 'final_url': r.url, 'status': r.status_code,
                  'content_type': r.headers.get('content-type'), 'body': r.text, 'checked': DAY}
    except requests.RequestException as e:
        result = {'url': url, 'final_url': None, 'status': None, 'error': str(e), 'body': '', 'checked': DAY}
    path.write_text(json.dumps(result))
    return result


def recover(candidate):
    original = candidate['url']
    pub = candidate['publication']
    live = read(original)
    attempts = []
    record = None
    snapshots = [candidate.get('archive_url')]
    # The first survey's collapsed CDX inventory selected early captures. A new
    # 2021+ inventory supplies later snapshots without discarding that evidence.
    for row in later:
        if row['original'].replace('http://', 'https://').rstrip('/') == original.rstrip('/'):
            snapshots.insert(0, f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}")
    snapshots = [s for s in snapshots if s]
    normal_snapshots = [s.replace('id_/', '/') for s in snapshots]
    if not re.search(r'/width=\d+$', original):
        path = original + '/' if urlsplit(original).netloc == 'blog.textile.io' else original
        snapshots.append('https://web.archive.org:443/web/20220101000000id_/' + path)
        snapshots.append('http://web.archive.org/web/20220101/' + path)
        if urlsplit(original).netloc == 'medium.com':
            snapshots.append('http://web.archive.org/web/20190101/' + path)
            snapshots.append('http://web.archive.org/web/20250101/' + path)
            snapshots.append('http://web.archive.org/web/20190101id_/' + path)
            snapshots.append('https://web.archive.org/web/20220101id_/' + path)
    urls = list(dict.fromkeys([original] + snapshots +
                             [s.replace('https://web.archive.org/', 'http://web.archive.org/') for s in snapshots] +
                             [s.replace('id_/', '/').replace('https://web.archive.org/', 'http://web.archive.org/') for s in snapshots] + normal_snapshots))
    for url in urls:
        result = live if url == original else read(url)
        soup = BeautifulSoup(result['body'], 'html.parser')
        a = metadata(result, pub, url)
        article_type = bool(soup.select('script[type="application/ld+json"]') and re.search(r'"@type"\s*:\s*"(?:Article|BlogPosting|NewsArticle|TechArticle)"', result['body']))
        attempts.append({'url': url, 'final_url': result['final_url'], 'status': result['status'],
                         'title': a['title'], 'date': a['date'], 'authors': a['authors'],
                         'article_schema': article_type, 'error': result.get('error')})
        if result['status'] != 200 or not a['title'] or not article_type:
            continue
        if a['title'] in ['Textile', 'Medium', 'Textile Blog & Newsletter', 'Just a moment...']:
            continue
        archived = urlsplit(result['final_url'] or url).hostname == 'web.archive.org'
        a.update(url=original, http_status=live['status'], final_url=live['final_url'],
                 archive_url=result['final_url'] if archived else None,
                 archive_status=result['status'] if archived else None,
                 evidence='archived article' if archived else 'live article',
                 sources=[original, result['final_url']])
        for link in a['links']:
            link['url'] = re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/', '', link['url'])
            if 'web.archive.org/' in link['url'] and '/web/' not in link['url']:
                link['url'] = urljoin(original, urlsplit(link['url']).path)
        record = a
        break
    return {'url': original, 'checked': DAY, 'attempts': attempts, 'article': record}


if __name__ == '__main__':
    baseline = json.loads((OUT / 'baseline-unresolved.json').read_text())
    cdx_url = 'https://web.archive.org/cdx/search/cdx?url=blog.textile.io/*&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey&from=2021'
    result = read(cdx_url)
    try:
        rows = json.loads(result['body'])
        later = [dict(zip(rows[0], r)) for r in rows[1:]]
    except (ValueError, KeyError):
        later = []
    (OUT / 'textile-cdx-from-2021.json').write_text(json.dumps(later, indent=2) + '\n')
    observations = []
    with cf.ThreadPoolExecutor(max_workers=5) as pool:
        jobs = [pool.submit(recover, c) for c in baseline]
        for job in cf.as_completed(jobs):
            observations.append(job.result())
            if len(observations) % 10 == 0:
                print(len(observations), 'checked;', sum(bool(x['article']) for x in observations), 'article reads', flush=True)
            (OUT / 'retry-observations.json').write_text(json.dumps(sorted(observations, key=lambda x: x['url']), indent=2, ensure_ascii=False) + '\n')
    articles = [x['article'] for x in sorted(observations, key=lambda x: x['url']) if x['article']]
    (ROOT / 'data/recovery-pass-2-articles.json').write_text(json.dumps(articles, indent=2, ensure_ascii=False) + '\n')
    print('Recovered metadata from', len(articles), 'URLs')
