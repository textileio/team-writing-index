"""Catalogue blog/article links and distinguish outside references from team bylines."""
import json,re,collections
from urllib.parse import urlsplit,urlunsplit
from research import ROOT,fetch,batch,metadata,cleanurl

def main():
    inputs=[]
    for p in (ROOT/'data').glob('*articles*.json'):
        if p.name=='linked-articles.json':continue
        for a in json.loads(p.read_text()):
            if a.get('title') and a.get('links'):inputs.append(a)
    outbound={}
    for a in inputs:
        for l in a.get('links',[]):
            u=l['url']
            if not u.startswith(('http://','https://')):continue
            p=urlsplit(u)
            if p.hostname in ['localhost','127.0.0.1'] or p.hostname is None:continue
            if 'web.archive.org/web/' in u:u=re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/','',u)
            u=cleanurl(u)
            if u==a['url']:continue
            entry=outbound.setdefault(u,{'url':u,'anchor_texts':[],'linked_from':[]})
            if l['text'] and l['text'] not in entry['anchor_texts']:entry['anchor_texts'].append(l['text'])
            if a['url'] not in entry['linked_from']:entry['linked_from'].append(a['url'])
    (ROOT/'data/outbound-links.json').write_text(json.dumps(sorted(outbound.values(),key=lambda x:x['url']),indent=2,ensure_ascii=False)+'\n')
    candidates=[]
    for u,v in outbound.items():
        p=urlsplit(u);host=p.netloc;path=p.path
        if host in ['blog.textile.io','blog.recall.network','blog.ceramic.network']:continue
        if path=='/' or re.search(r'/(@[^/]+|tag(?:ged)?/[^/]+|archive|about|all)/?$',path):continue
        if host.startswith(('docs.','developer.')):continue
        article=(host.startswith('blog.') or '/blog/' in path or '/news/' in path or re.search(r'/(?:19|20)\d{2}/',path) or host in ['medium.com','hackernoon.com','mirror.xyz'] or host.endswith('.substack.com') and path.startswith('/p/'))
        if article and not re.search(r'/(tag|category|author|u|m|membership|search|followers|following|subscribe|feed|api)/',path):candidates.append(u)
    print('Outbound URLs',len(outbound),'blog/article candidates',len(candidates),flush=True)
    records=[]
    for n,(u,r) in enumerate(zip(candidates,batch(candidates,6)),1):
        a=metadata(r,'Linked articles',outbound[u]['linked_from'][0])
        a.update(url=u,linked_from=outbound[u]['linked_from'],anchor_texts=outbound[u]['anchor_texts'])
        if not a['title'] or not a['date']:
            a['title']=None;a['date']=None;a['authors']=[];a['evidence']='linked URL; article metadata unavailable'
        else:a['evidence']='live linked article'
        records.append(a)
    (ROOT/'data/linked-articles.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    print('Linked records',len(records),'with metadata',sum(bool(a['date']) for a in records),flush=True)
if __name__=='__main__':main()
