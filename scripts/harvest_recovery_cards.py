"""Extract first-party publication cards from successfully read archive pages."""
import html
import json
import re
from urllib.parse import urljoin, urlsplit

from research import ROOT, DAY, BeautifulSoup, cleanurl


def original(url):
    return re.sub(r'^https?://web\.archive\.org(?::443)?/web/\d+(?:[a-z_]+)?/', '', url)


def main():
    records = {}
    observations = []
    for path in sorted((ROOT / '.cache/recovery-pass-2').glob('*.json')):
        result = json.loads(path.read_text())
        if result.get('status') != 200 or urlsplit(original(result['final_url'])).netloc != 'blog.textile.io':
            continue
        soup = BeautifulSoup(result['body'], 'html.parser')
        for card in soup.select('.m-article-card'):
            heading = card.select_one('.m-article-card__title')
            anchor = card.select_one('a.m-article-card__info-link[href]')
            if not heading or not anchor:
                continue
            title = heading.get_text(' ', strip=True)
            base = result['final_url'] if anchor['href'].startswith('/web/') else original(result['final_url'])
            url = cleanurl(original(urljoin(base, anchor['href'])))
            if urlsplit(url).netloc != 'blog.textile.io':
                continue
            byline = card.select_one('[data-tippy-content]')
            authors = []
            if byline:
                text = BeautifulSoup(byline['data-tippy-content'], 'html.parser').get_text(' ', strip=True)
                text = re.sub(r'^Posted by\s+', '', html.unescape(text)).strip()
                authors = [a.strip() for a in re.split(r'\s+Along with\s+|,\s*', text) if a.strip()]
            time = card.select_one('time[datetime]')
            date = time['datetime'][:10] if time and re.match(r'\d{4}-\d{2}-\d{2}', time['datetime']) else None
            record = records.setdefault(url, {'url': url, 'title': title, 'date': date,
                'authors': authors, 'publication': 'Textile historical blog',
                'sources': [], 'http_status': None, 'archive_url': None,
                'checked': DAY, 'links': [], 'evidence': 'archived publication listing'})
            if result['final_url'] not in record['sources']:
                record['sources'].append(result['final_url'])
            observations.append({'url': url, 'title': title, 'source': result['final_url']})
    (ROOT / 'data/recovery-card-articles.json').write_text(json.dumps(list(records.values()), indent=2, ensure_ascii=False) + '\n')
    (ROOT / 'research/recovery-pass-2/card-observations.json').write_text(json.dumps(observations, indent=2, ensure_ascii=False) + '\n')
    print(len(records), 'unique URLs supported by archived publication cards')


if __name__ == '__main__':
    main()
