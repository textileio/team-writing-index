"""Inventory the related Ceramic/3Box publication separately."""
import json
from research import ROOT,fetch,batch,metadata,article_urls,ET,BeautifulSoup
from email.utils import parsedate_to_datetime
u='https://blog.ceramic.network/sitemap-posts.xml'
urls=article_urls(fetch(u)['body'])
records=[metadata(r,'Ceramic / 3Box',u) for r in batch(urls)]
(ROOT/'data/ceramic-articles.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
print('Ceramic post records',len(records),flush=True)
u='https://medium.com/feed/3box';r=fetch(u);out=[]
for item in ET.fromstring(r['body']).findall('.//item'):
    body=item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded') or ''
    s=BeautifulSoup(body,'html.parser')
    out.append({'url':item.findtext('link').split('?')[0],'title':item.findtext('title'),'date':parsedate_to_datetime(item.findtext('pubDate')).date().isoformat(),'authors':[item.findtext('{http://purl.org/dc/elements/1.1/}creator')],'publication':'3Box on Medium','sources':[u],'http_status':None,'evidence':'public RSS feed','checked':'2026-10-15','links':[{'url':l['href'],'text':l.get_text(' ',strip=True)} for l in s.select('a[href]')]})
(ROOT/'data/3box-articles.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('3Box RSS records',len(out),flush=True)
