"""Inventory the two official Tableland Paragraph publications, including migrated Mirror posts."""
import json,re
from urllib.parse import urlsplit,urljoin
from research import ROOT,fetch,batch,metadata,article_urls,ET,BeautifulSoup,rsc,cleanurl
articles=[];coverage=[]
for handle in ['tableland','tableland-2']:
    base='https://paragraph.com/@'+handle;urls=set()
    for u in [base+'/sitemap.xml',base+'/news-sitemap.xml']:
        r=fetch(u)
        try:urls.update(cleanurl(x) for x in article_urls(r['body']) if urlsplit(x).path.count('/')==2 and not x.endswith('/'))
        except ET.ParseError:pass
    r=fetch('https://paragraph.com/api/blogs/rss/@'+handle)
    try:urls.update(cleanurl(x.findtext('link')) for x in ET.fromstring(r['body']).findall('.//item') if x.findtext('link'))
    except ET.ParseError:pass
    pages=batch([base]+[base+'/p/'+str(n) for n in range(2,5)])
    counts=[]
    for r in pages:
        s=BeautifulSoup(r['body'],'html.parser');counts+=re.findall(r'"postCount":(\d+)',rsc(s))
        for a in s.select('a[href]'):
            u=urljoin(base,a['href'])
            if urlsplit(u).path.startswith('/@'+handle+'/') and urlsplit(u).path.count('/')==2 and '/category/' not in u:urls.add(cleanurl(u))
    for r in batch(sorted(urls)):
        a=metadata(r,'Tableland Mirror / Paragraph',base)
        if a['date']:articles.append(a)
    coverage.append({'home':base,'reported_post_counts':list(set(counts)),'urls':len(urls),'metadata_records':sum(base in a['sources'] for a in articles)})
    print(coverage[-1],flush=True)
(ROOT/'data/mirror-articles.json').write_text(json.dumps(articles,indent=2,ensure_ascii=False)+'\n')
(ROOT/'research/mirror-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
