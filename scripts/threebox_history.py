"""Recover the observed historical 3Box Medium CDX inventory."""
import json,re,concurrent.futures as cf
from urllib.parse import urlsplit
from research import ROOT,fetch,cleanurl
from history import recover
source='https://web.archive.org/cdx/search/cdx?url=medium.com/3box/*&output=json&filter=statuscode:200&collapse=urlkey'
a=json.loads(fetch(source)['body']);rows=[dict(zip(a[0],x)) for x in a[1:]]
(ROOT/'research/3box-cdx.json').write_text(json.dumps(rows,indent=2)+'\n')
candidates={}
for row in rows:
    p=urlsplit(row['original'])
    if not p.query and re.fullmatch(r'/3box/[^/]+-[a-f0-9]{8,16}/?',p.path):candidates.setdefault(cleanurl(row['original']),row)
records=[]
with cf.ThreadPoolExecutor(max_workers=5) as ex:
    for n,a in enumerate(ex.map(lambda r:recover(r,'3Box on Medium',source,set()),candidates.values()),1):
        if a:records.append(a)
        if n%20==0:print('3Box historical',n,'processed',sum(bool(x['date']) for x in records),'metadata records',flush=True)
(ROOT/'data/3box-historical-articles.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
(ROOT/'research/3box-coverage.json').write_text(json.dumps({'source':source,'cdx_rows':len(rows),'candidate_article_urls':len(candidates),'records':len(records),'article_metadata':sum(bool(x['date']) for x in records)},indent=2)+'\n')
print('3Box historical records',len(records),flush=True)
