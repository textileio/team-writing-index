"""Recover bibliographic fields from public Paragraph cards and feeds."""
import json,re,datetime as dt
from urllib.parse import urljoin,urlsplit
from research import ROOT,fetch,batch,BeautifulSoup,rsc,ET,cleanurl
out=[]
for base,group,count in [('https://blog.textile.io','Textile / Tableland / Basin',8),('https://blog.recall.network','Recall',2),('https://paragraph.com/@tableland','Tableland Mirror / Paragraph',1),('https://paragraph.com/@tableland-2','Tableland Mirror / Paragraph',3)]:
    def walk(v):
        if isinstance(v,dict):
            yield v
            for x in v.values():yield from walk(x)
        elif isinstance(v,list):
            for x in v:yield from walk(x)
    for r in batch([base+'/']+[base+'/p/'+str(n) for n in range(2,count+1)]):
        text=rsc(BeautifulSoup(r['body'],'html.parser'))
        for line in text.splitlines():
            try:v=json.loads(line.split(':',1)[1])
            except (ValueError,IndexError):continue
            for node in walk(v):
                href=node.get('href','')
                if not isinstance(href,str) or href=='/' or any(x in href for x in ['/p/','/category/','/author/']):continue
                u=urljoin(base,href)
                if urlsplit(u).netloc!=urlsplit(base).netloc or u.rstrip('/')==base.rstrip('/'):continue
                sub=list(walk(node));image=next((x for x in sub if x.get('publishedAt') and (x.get('text') or x.get('alt'))),None)
                if image:
                    out.append({'url':cleanurl(u),'title':image.get('text') or image.get('alt'),'date':dt.datetime.fromtimestamp(image['publishedAt']/1000,dt.timezone.utc).date().isoformat(),'authors':[],'publication':group,'sources':[r['url']],'evidence':'public publication listing','http_status':None,'checked':'2026-10-15','links':[]})
(ROOT/'data/paragraph-listing-articles.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Paragraph card records',len(out),'unique',len({a['url'] for a in out}))
