"""Fetch public publication metadata and preserve link provenance (no credentials)."""
import concurrent.futures as cf
import datetime as dt
import hashlib
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit, unquote
import requests
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache'
CACHE.mkdir(exist_ok=True)
DAY='2026-10-15'

def fetch(url):
    key=hashlib.sha256(url.encode()).hexdigest()
    p=CACHE/(key+'.json')
    if p.exists(): return json.loads(p.read_text())
    try:
        r=requests.get(url,timeout=30,headers={'User-Agent':'TeamWritingIndex/1.0 (public bibliographic research)'})
        out={'url':url,'final_url':r.url,'status':r.status_code,'content_type':r.headers.get('content-type',''),'body':r.text,'checked':DAY}
    except requests.RequestException as e:
        out={'url':url,'final_url':None,'status':None,'error':str(e),'body':'','checked':DAY}
    p.write_text(json.dumps(out));return out

def batch(urls,workers=6):
    with cf.ThreadPoolExecutor(max_workers=workers) as ex: return list(ex.map(fetch,urls))

def cleanurl(u):
    p=urlsplit(u)
    return urlunsplit(('https',p.netloc.lower(),unquote(p.path).rstrip('/') or '/', '', ''))

def rsc(soup):
    chunks=[]
    for tag in soup.find_all('script'):
        t=tag.string or tag.get_text()
        m=re.fullmatch(r'self\.__next_f\.push\((.*)\)',t,re.S)
        if m:
            try:
                a=json.loads(m[1]);
                if len(a)>1 and isinstance(a[1],str): chunks.append(a[1])
            except (ValueError,IndexError): pass
    return ''.join(chunks)

def article_urls(body):
    root=ET.fromstring(body)
    return [x.text for x in root.findall('./{*}url/{*}loc') + root.findall('./{*}sitemap/{*}loc') if x.text]

def metadata(result,group,source):
    soup=BeautifulSoup(result['body'],'html.parser')
    def meta(name):
        t=soup.find('meta',property=name) or soup.find('meta',attrs={'name':name})
        return t.get('content','') if t else ''
    data=[]
    for tag in soup.find_all('script',type='application/ld+json'):
        try:
            v=json.loads(tag.string or tag.get_text()); data.extend(v if isinstance(v,list) else [v])
        except ValueError: pass
    def walk(v):
        if isinstance(v,dict):
            if v.get('@type') in ('Article','BlogPosting','NewsArticle','TechArticle'):return v
            for x in v.values():
                z=walk(x)
                if z:return z
        if isinstance(v,list):
            for x in v:
                z=walk(x)
                if z:return z
        return {}
    ld=walk(data)
    author=ld.get('author',[])
    if isinstance(author,(str,dict)):author=[author]
    authors=[x.get('name','') if isinstance(x,dict) else x for x in author]
    if not any(authors):authors=[meta('author')] if meta('author') else []
    canonical=soup.find('link',rel='canonical')
    title=ld.get('headline') or meta('og:title') or (soup.h1.get_text(' ',strip=True) if soup.h1 else '')
    date=ld.get('datePublished') or meta('article:published_time')
    text=rsc(soup)
    if not date:
        m=re.search(r'"publishedAt":(\d{13})',text)
        if m:date=dt.datetime.fromtimestamp(int(m[1])/1000,dt.timezone.utc).isoformat()
    article=soup.select_one('.post-content, .gh-content') or soup.find('article') or soup.find('main') or soup
    links=[{'url':urljoin(result['final_url'] or result['url'],a['href']),'text':a.get_text(' ',strip=True)} for a in article.select('a[href]')]
    return {'title':html.unescape(title),'url':cleanurl(result['url']),'canonical_url':canonical.get('href') if canonical else result['final_url'],'date':date[:10] if date else None,'authors':list(filter(None,authors)),'publication':group,'sources':[source],'http_status':result['status'],'final_url':result['final_url'],'checked':DAY,'links':links}

def paragraph():
    articles=[];coverage=[]
    for host,group in [('blog.textile.io','Textile / Tableland / Basin'),('blog.recall.network','Recall')]:
        base='https://'+host
        maps=batch([base+'/sitemap.xml',base+'/news-sitemap.xml'])
        urls=set()
        for m in maps:
            try:
                for u in article_urls(m['body']):
                    path=urlsplit(u).path
                    if path!='/' and not path.startswith(('/p/','/category/','/author/')):urls.add(cleanurl(u))
            except ET.ParseError:pass
        pages=batch([base+'/']+[base+'/p/'+str(n) for n in range(2,9 if 'textile' in host else 5)])
        counts=[]
        for p in pages:
            s=BeautifulSoup(p['body'],'html.parser')
            for a in s.select('a[href]'):
                u=urljoin(base,a['href']);path=urlsplit(u).path
                if urlsplit(u).netloc==host and path!='/' and not path.startswith(('/p/','/category/','/author/','/api/')):urls.add(cleanurl(u))
            m=re.search(r'"postCount":(\d+)',rsc(s))
            if m:counts.append(int(m[1]))
        feed=fetch(base+'/rss/')
        feeditems=[]
        try:
            for item in ET.fromstring(feed['body']).findall('.//item'):
                u=item.findtext('link')
                if u:urls.add(cleanurl(u));feeditems.append(u)
        except ET.ParseError:pass
        fetched=batch(sorted(urls))
        for result in fetched: articles.append(metadata(result,group,base+'/sitemap.xml + pagination + RSS'))
        coverage.append({'publication':group,'home':base,'reported_post_counts':sorted(set(counts)),'discovered_article_urls':len(urls),'rss_items':len(feeditems),'article_statuses':{str(s):sum(x['status']==s for x in fetched) for s in set(x['status'] for x in fetched)},'sitemap_urls':[x['url'] for x in maps]})
        print(coverage[-1],flush=True)
        (ROOT/'data/paragraph-articles.json').write_text(json.dumps(articles,indent=2,ensure_ascii=False)+'\n')
        (ROOT/'research/paragraph-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')

if __name__=='__main__':paragraph()
