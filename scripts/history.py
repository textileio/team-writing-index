"""Recover historical public writing from Internet Archive CDX and snapshots."""
import concurrent.futures as cf
import json,re
from urllib.parse import urlsplit
from research import ROOT,fetch,batch,metadata,cleanurl,BeautifulSoup,ET

def cdx(host):
    u=f'https://web.archive.org/cdx/search/cdx?url={host}/*&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey'
    r=fetch(u);a=json.loads(r['body']);rows=[dict(zip(a[0],x)) for x in a[1:]]
    (ROOT/('research/'+host.replace('/','-')+'-cdx.json')).write_text(json.dumps(rows,indent=2)+'\n')
    return rows,u

def recover(row,publication,source,current_urls):
    original=cleanurl(row['original'])
    if original in current_urls:return None
    medium='medium.com' in original
    # Preserve live canonical links where possible; snapshot is fallback evidence.
    live=fetch(original)
    snapshot=f"https://web.archive.org/web/{row['timestamp']}id_/{row['original']}"
    result=live if live['status']==200 and urlsplit(live['final_url']).netloc==urlsplit(original).netloc else fetch(snapshot)
    if result['status'] != 200:
        result=fetch(snapshot.replace('id_/','/'))
    if result['status'] != 200:
        result=fetch('https://web.archive.org/web/20220101000000id_/'+row['original'])
    if result['status'] != 200:
        result=fetch(snapshot.replace('https://web.archive.org/','http://web.archive.org/'))
    if result['status']!=200:
        return {'url':original,'publication':publication,'title':None,'date':None,'authors':[],'sources':[source],'archive_url':snapshot,'http_status':live['status'],'archive_status':result['status'],'checked':'2026-10-15','links':[],'evidence':'CDX URL only; metadata unavailable'}
    a=metadata(result,publication,source)
    a.update(url=original,http_status=live['status'],final_url=live['final_url'],archive_url=result['final_url'] if 'web.archive.org/web/' in result['url'] else None,evidence='archived article' if 'web.archive.org/web/' in result['url'] else 'live article')
    a['archive_timestamp']=re.search(r'/web/(\d+)',result['final_url']).group(1) if '/web/' in result['final_url'] else None
    # Archived HTML's original relative links must resolve against original host.
    from urllib.parse import urljoin
    for l in a['links']:
        l['url']=re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/','',l['url'])
        if 'web.archive.org/' in l['url'] and '/web/' not in l['url']:l['url']=urljoin(original,urlsplit(l['url']).path)
    # Only bibliographic article pages, excluding author/landing pages.
    # Some genuine historical articles expose a heading and byline but no
    # publication date. Keep those unknown dates rather than dropping the post.
    if not a['date'] and not medium and not re.search(r'"@type"\s*:\s*"(?:Article|BlogPosting)"',result['body']):return None
    if a['title'] in ['Just a moment...','Medium','Textile','Textile Blog & Newsletter']:return None
    return a

def main():
    current={x['url'] for x in json.loads((ROOT/'data/paragraph-articles.json').read_text())}
    all_records=[];coverage=[]
    for host,group in [('blog.textile.io','Textile historical blog'),('medium.com/textileio','Textile on Medium')]:
        rows,source=cdx(host);candidates={}
        for row in rows:
            p=urlsplit(row['original'])
            if p.query:continue
            path=p.path.strip('/')
            if host.startswith('medium'):
                valid=re.fullmatch(r'textileio/[^/]+-[a-f0-9]{8,16}',path)
            else:
                valid=len(path.split('/'))==1 and path and '.' not in path and path not in ['new','explore','register','join-newsletter','hosted-powergate','andrew','carson'] and not path.endswith('\\') and not path.startswith(('width=','rss','sitemap','robots','favicon','subscribe','ghost','members','signup','assets','search','unsubscribe'))
            if valid:candidates.setdefault(cleanurl(row['original']),row)
        print(host,'candidate article URLs',len(candidates),flush=True)
        with cf.ThreadPoolExecutor(max_workers=5) as ex:
            fs=[ex.submit(recover,row,group,source,current) for row in candidates.values()]
            for n,f in enumerate(cf.as_completed(fs),1):
                try:
                    a=f.result()
                    if a:all_records.append(a)
                except Exception as e:print('ERROR',str(e),flush=True)
                if n%20==0:
                    print(host,n,'processed;',len(all_records),'historical records',flush=True)
                    (ROOT/'data/historical-articles.json').write_text(json.dumps(all_records,indent=2,ensure_ascii=False)+'\n')
        coverage.append({'publication':group,'cdx_rows':len(rows),'candidate_article_urls':len(candidates),'records':sum(a['publication']==group for a in all_records),'cdx_url':source})
        (ROOT/'data/historical-articles.json').write_text(json.dumps(all_records,indent=2,ensure_ascii=False)+'\n')
        (ROOT/'research/historical-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
if __name__=='__main__':main()
