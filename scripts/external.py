"""Discover public team bylines and cross-posts beyond the company publication."""
import json,re,datetime as dt
from urllib.parse import urlsplit
from research import ROOT,fetch,batch,metadata,BeautifulSoup,ET,cleanurl
from history import cdx,recover

def main():
    records=[];urls={}
    for handle in ['andrewxhill','carsonfarmer','sanderpick']:
        u='https://medium.com/feed/@'+handle
        r=fetch(u)
        if r['status']==200:
            try:
                for item in ET.fromstring(r['body']).findall('.//item'):
                    link=item.findtext('link')
                    if link:urls[cleanurl(link)]=u
            except ET.ParseError:pass
    for handle in ['andrewxhill','carsonfarmer','sanderpick']:
        u=f'http://web.archive.org/cdx/search/cdx?url=medium.com/@{handle}/*&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=urlkey'
        r=fetch(u)
        if r['status']!=200:continue
        try:
            rows=json.loads(r['body'])
            for row in rows[1:]:
                d=dict(zip(rows[0],row));path=urlsplit(d['original']).path
                if re.fullmatch(r'/@[^/]+/[^/]+-[a-f0-9]{8,16}/?',path):urls[cleanurl(d['original'])]=u
        except ValueError:pass
    for u in ['https://medium.com/textileio/about','https://medium.com/@carsonfarmer','https://medium.com/@andrewxhill']:
        s=BeautifulSoup(fetch(u)['body'],'html.parser')
        from urllib.parse import urljoin
        for a in s.select('a[href]'):
            link=urljoin(u,a['href'])
            if re.fullmatch(r'/textileio/[^/]+-[a-f0-9]{8,16}',urlsplit(link).path):urls[cleanurl(link)]=u
    u='https://hackernoon.com/u/carsonfarmer';s=BeautifulSoup(fetch(u)['body'],'html.parser');tag=s.find('script',id='__NEXT_DATA__')
    if tag:
        p=json.loads(tag.get_text())['props']['pageProps']['data']
        for item in p.get('profileStories',[]):urls['https://hackernoon.com/'+item['slug']]=u
    urls['https://www.freecodecamp.org/news/from-zero-to-interplanetary-hero-7e62f7d4427']='https://www.freecodecamp.org/news/from-zero-to-interplanetary-hero-7e62f7d4427'
    print('External / profile URL candidates',len(urls),flush=True)
    for u,r in zip(urls,batch(urls)):
        if r['status']==200:
            a=metadata(r,'Team writing on other sites',urls[u])
            a['evidence']='live article / author profile'
            if a['title'] and a['date']:records.append(a)
    (ROOT/'data/external-articles.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'research/external-discovery.json').write_text(json.dumps(urls,indent=2)+'\n')
    print('External records',len(records),flush=True)
if __name__=='__main__':main()
