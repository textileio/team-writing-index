"""Supplement migrations with Substack and historical archive listing metadata."""
import json,re,concurrent.futures as cf
from urllib.parse import urlsplit,urljoin
from research import ROOT,fetch,batch,metadata,BeautifulSoup,cleanurl,ET

def substack():
    rows=[];offset=0
    while True:
        u=f'https://tableland.substack.com/api/v1/archive?sort=new&offset={offset}&limit=50'
        r=fetch(u)
        if r['status']!=200:break
        part=json.loads(r['body'])
        if not part:break
        rows+=part;offset+=len(part)
        if len(part)<50:break
    records=[]
    for row,r in zip(rows,batch([x['canonical_url'] for x in rows])):
        a=metadata(r,'Tableland Weeknotes on Substack','https://tableland.substack.com/api/v1/archive?sort=new&offset=0&limit=50')
        a.update(title=row['title'],date=row['post_date'][:10],authors=[x['name'] for x in row['publishedBylines']],evidence='public Substack archive API and article')
        records.append(a)
    (ROOT/'data/substack-articles.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n');print('Substack',len(records),flush=True)

def archive_listings():
    urls=['https://web.archive.org/web/20220101000000id_/https://blog.textile.io/']+['https://web.archive.org/web/20220101000000id_/https://blog.textile.io/page/'+str(n)+'/' for n in range(2,21)]
    records=[]
    for r in batch(urls,4):
        if r['status']!=200:continue
        s=BeautifulSoup(r['body'],'html.parser')
        for card in s.find_all('article'):
            h=card.find(['h1','h2','h3']);a=card.select_one('a[aria-label="Article"], a.m-article-card__info-link, a.m-featured-article__content')
            if h and a:
                author=card.select_one('a[data-tippy-content]')
                by=BeautifulSoup(author.get('data-tippy-content',''),'html.parser').get_text(' ',strip=True) if author else ''
                by=by.replace('Posted by ','').replace('Along with',',')
                authors=[x.strip() for x in by.split(',') if x.strip()]
                records.append({'url':cleanurl(urljoin('https://blog.textile.io/',a['href'])),'title':h.get('title') or h.get_text(' ',strip=True),'authors':authors,'date':None,'publication':'Textile historical blog','sources':[r['final_url']],'evidence':'archived publication listing','http_status':None,'archive_url':None,'links':[],'checked':'2026-10-15'})
    (ROOT/'data/archive-listing-articles.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n');print('Archive listing cards',len(records),flush=True)

def alternate_snapshots():
    records=[]
    old=json.loads((ROOT/'data/historical-articles.json').read_text())
    urls=[]
    for a in old:
        if a['date'] or 'blog.textile.io/' not in a['url']:continue
        urls.append((a,'https://web.archive.org/web/20210101000000id_/'+a['url']+'/'))
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for n,(old,r) in enumerate(zip([x[0] for x in urls],ex.map(fetch,[x[1] for x in urls])),1):
            if r['status']==200:
                a=metadata(r,old['publication'],r['final_url']);a.update(url=old['url'],http_status=old['http_status'],final_url=old.get('final_url'),archive_url=r['final_url'],evidence='archived article')
                if a['date']:records.append(a)
            if n%40==0:print('Alternate snapshots',n,'processed',len(records),'recovered',flush=True)
    (ROOT/'data/alternate-snapshot-articles.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n');print('Alternate snapshot metadata',len(records),flush=True)
if __name__=='__main__':
    substack();archive_listings();alternate_snapshots()
