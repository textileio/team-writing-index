"""Try article bodies behind undated, listing-supported catalogue entries."""
import concurrent.futures as cf
import json
import re
from urllib.parse import urlsplit, urljoin

from research import ROOT, metadata, BeautifulSoup
from retry_unresolved import read, OUT


def recover(article):
    url = next((e['url'] for e in article['editions'] if urlsplit(e['url']).netloc == 'blog.textile.io'), None)
    if not url:
        return {'title': article['title'], 'url': None, 'attempts': [], 'article': None}
    attempts = []
    for prefix in ['http://web.archive.org/web/20220101/', 'https://web.archive.org/web/20220101id_/']:
        result = read(prefix + url.rstrip('/') + '/')
        a = metadata(result, 'Textile historical blog', result['final_url'] or result['url'])
        article_schema = bool(re.search(r'"@type"\s*:\s*"(?:Article|BlogPosting)"', result['body']))
        attempts.append({'url': result['url'], 'final_url': result['final_url'], 'status': result['status'], 'title': a['title'], 'date': a['date'], 'article_schema': article_schema})
        if result['status'] == 200 and article_schema and a['title']:
            a.update(url=url, http_status=None, archive_url=result['final_url'], archive_status=200, evidence='archived article')
            for link in a['links']:
                link['url'] = re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/', '', link['url'])
                if 'web.archive.org/' in link['url'] and '/web/' not in link['url']:
                    link['url'] = urljoin(url, urlsplit(link['url']).path)
            return {'title': article['title'], 'url': url, 'attempts': attempts, 'article': a}
    return {'title': article['title'], 'url': url, 'attempts': attempts, 'article': None}


if __name__ == '__main__':
    candidates = OUT / 'undated-candidates.json'
    if candidates.exists():
        articles = json.loads(candidates.read_text())
    else:
        articles = [{'title': a['title'], 'editions': [{'url': e['url']} for e in a['editions']]}
                    for a in json.loads((ROOT / 'data/catalogue.json').read_text()) if not a['date']]
        candidates.write_text(json.dumps(articles, indent=2, ensure_ascii=False) + '\n')
    with cf.ThreadPoolExecutor(max_workers=4) as pool:
        observations = list(pool.map(recover, articles))
    (OUT / 'undated-retry-observations.json').write_text(json.dumps(observations, indent=2, ensure_ascii=False) + '\n')
    records = [x['article'] for x in observations if x['article']]
    (ROOT / 'data/undated-recovery-articles.json').write_text(json.dumps(records, indent=2, ensure_ascii=False) + '\n')
    print(len(records), 'article reads;', sum(bool(a['date']) for a in records), 'with publication dates')
