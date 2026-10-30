"""Build Markdown indexes and a deduplicated bibliography from collected metadata."""
import collections,datetime as dt,html,json,re,unicodedata
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,quote,unquote
ROOT=Path(__file__).resolve().parents[1]
DAY='2026-10-15'

def normal(u):
    u=re.sub(r'^https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/','',u)
    p=urlsplit(u)
    return urlunsplit(('https',p.netloc.lower(),unquote(p.path).rstrip('/') or '/','',''))
def key(u):
    u=normal(u)
    if urlsplit(u).netloc=='medium.com':
        m=re.search(r'([a-f0-9]{8,16})$',urlsplit(u).path)
        if m:return 'medium:'+m[1]
    return u

def tkey(s):return re.sub(r'[^\w]+','',unicodedata.normalize('NFKC',html.unescape(s or '')).lower())
def esc(s):return html.unescape(str(s or '')).replace('|','\\|').replace('[','\\[').replace(']','\\]').replace('\n',' ').strip()
def link(label,u):return '['+esc(label)+']('+quote(u,safe=':/?=&%#@,;+$!~*-._')+')'

def valid(a):
    return bool(a.get('title')) and not a['title'].startswith(('500:','404:')) and bool(a.get('date') or 'listing' in a.get('evidence','') or a.get('evidence') in ['archived article','live article'])

def main():
    raw=[]
    resolutions_path=ROOT/'data/url-resolutions.json'
    resolutions=json.loads(resolutions_path.read_text()) if resolutions_path.exists() else []
    excluded={key(a['url']) for a in resolutions if a['classification'] in ['non-article','malformed-route']}
    for p in sorted((ROOT/'data').glob('*articles*.json')):
        if p.name in ['linked-articles.json','catalogue-articles.json']:continue
        for a in json.loads(p.read_text()):
            a['_file']=p.name
            if a.get('url') and key(a['url']) not in excluded:raw.append(a)
    linked=json.loads((ROOT/'data/linked-articles.json').read_text()) if (ROOT/'data/linked-articles.json').exists() else []
    staff={'Carson Farmer','Andrew Hill','Sander Pick','Aaron Sutula','Ignacio Hagopian','Merlin Ran','Michael Sena','Danny Zuckerman','Daniel Zuckerman','Mark Krasner','Timothy Lim','Joel Torstensson','Christian Lundkvist','3Box Labs'}
    for a in linked:
        official = '3Box on Medium' if 'medium.com/3box/' in a['url'] else 'Textile on Medium' if 'medium.com/textileio/' in a['url'] else 'Tableland Mirror / Paragraph' if 'mirror.xyz/tableland.eth/' in a['url'] else None
        if (official or set(a.get('authors',[]))&staff) and valid(a):
            a=dict(a);a['publication']=official or 'Team writing on other sites';a['_file']='linked-articles.json';raw.append(a)
    # Merge identical URL / Medium post IDs before merging matching titles.
    buckets={}
    for a in raw:buckets.setdefault(key(a['url']),[]).append(a)
    parent={k:k for k in buckets}
    def find(k):
        while parent[k]!=k:parent[k]=parent[parent[k]];k=parent[k]
        return k
    def union(a,b):
        if find(a)!=find(b):parent[find(b)]=find(a)
    for k,items in buckets.items():
        for a in items:
            c=a.get('canonical_url')
            if c and key(c) in buckets:union(k,key(c))
    titles={}
    for k,items in buckets.items():
        for a in items:
            if not valid(a):continue
            t=tkey(a['title']);date=a.get('date')
            for prior,pdate in titles.get(t,[]):
                if not date or not pdate or abs((dt.date.fromisoformat(date)-dt.date.fromisoformat(pdate)).days)<=45:union(k,prior)
            titles.setdefault(t,[]).append((k,date))
    groups={}
    for k,items in buckets.items():groups.setdefault(find(k),[]).extend(items)
    catalogue=[];unresolved=[]
    for items in groups.values():
        good=[a for a in items if valid(a)]
        if not good:
            # Retain corroborated CDX article-shaped URLs; never invent a title from a slug.
            for a in items:
                if a.get('evidence','').startswith('CDX URL only'):
                    unresolved.append({k:v for k,v in a.items() if k not in ['links','_file']})
            continue
        def score(a):
            return (bool(a.get('date')),a.get('http_status')==200,'web reader' not in a.get('evidence',''),len(a.get('authors',[])),len(a.get('links',[])))
        best=max(good,key=score)
        editions={}
        for a in items:
            u=normal(a['url']);entry=editions.setdefault(u,{'url':u,'publication':a.get('publication'),'date':None,'date_observations':[],'http_status':None,'archive_url':None,'sources':[],'evidence':[]})
            if valid(a) and a.get('date'):
                entry['date']=a['date']
                observation={'date':a['date'],'sources':a.get('sources',[]),'evidence':a.get('evidence'),'record_file':a['_file']}
                if observation not in entry['date_observations']:entry['date_observations'].append(observation)
            if a.get('http_status') is not None:entry['http_status']=a['http_status']
            if a.get('archive_url') and (valid(a) or a.get('archive_status')==200):entry['archive_url']=a['archive_url']
            for source in a.get('sources',[]):
                if source not in entry['sources']:entry['sources'].append(source)
            if a.get('evidence') and a['evidence'] not in entry['evidence']:entry['evidence'].append(a['evidence'])
        pubs={a.get('publication','') for a in items}
        if 'GitHub papers and workshops' in pubs:collection='Papers and workshops'
        elif 'Recall' in pubs:collection='Recall'
        elif any('Ceramic' in p or '3Box' in p for p in pubs):collection='Ceramic / 3Box'
        elif all(p=='Team writing on other sites' for p in pubs):collection='Other team bylines'
        else:collection='Textile / Tableland / Basin'
        authors=sorted({y for a in good for y in a.get('authors',[]) if y})
        record={'title':html.unescape(best['title']),'date':best.get('date'),'authors':authors,'collection':collection,'editions':list(editions.values()),'checked':DAY}
        catalogue.append(record)
    catalogue.sort(key=lambda x:(x['date'] or '',x['title']),reverse=True)
    # A URL-only alias is no longer unresolved if another record supplied its metadata.
    known={key(e['url']) for a in catalogue for e in a['editions']}
    unresolved=list({key(a['url']):a for a in unresolved if key(a['url']) not in known}.values())
    (ROOT/'data/catalogue.json').write_text(json.dumps(catalogue,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'data/unresolved-urls.json').write_text(json.dumps(unresolved,indent=2,ensure_ascii=False)+'\n')
    def table(records):
        lines=['| Date | Article | Byline | Editions / access |','| --- | --- | --- | --- |']
        for a in records:
            editions=sorted(a['editions'],key=lambda e:(0 if e['http_status']==200 else 1 if e.get('archive_url') else 2 if any('reader' in ev or 'RSS' in ev for ev in e.get('evidence',[])) else 3,'medium.com' in e['url']))
            main=editions[0];alts=[]
            for e in editions:
                host=urlsplit(e['url']).netloc
                name=('Medium' if host=='medium.com' else 'Paragraph' if host=='paragraph.com' else 'Substack' if host.endswith('substack.com') else host)
                status='' if e['http_status']==200 else (' (HTTP '+str(e['http_status'])+')' if e['http_status'] else '')
                alts.append(link(name,e['url'])+status)
                if e.get('archive_url'):alts.append(link('archive',e['archive_url']))
            lines.append('| '+(a['date'] or 'Unknown')+' | '+link(a['title'],main['archive_url'] if main.get('archive_url') and main['http_status']!=200 else main['url'])+' | '+esc(', '.join(a['authors']) or 'Not exposed by source')+' | '+'; '.join(alts)+' |')
        return lines
    social=json.loads((ROOT/'data/social-posts.json').read_text())
    talks=json.loads((ROOT/'data/talks.json').read_text())
    company_order=['Set','Textile','Tableland','Basin','Recall']
    assignments=json.loads((ROOT/'data/readme-sections.json').read_text())
    section_keys={}
    for section,assignment in assignments.items():
        assert section in company_order, ('Unknown README section',section)
        for url in assignment['urls']:
            k=key(url)
            assert k in known and k not in section_keys, ('Unknown or repeated README assignment',url)
            section_keys[k]=section
    sections=collections.defaultdict(list)
    for a in catalogue:
        section=a['collection']
        if section=='Textile / Tableland / Basin':
            assigned={section_keys[key(e['url'])] for e in a['editions'] if key(e['url']) in section_keys}
            assert len(assigned)<=1, ('Conflicting README sections',a['title'])
            section=assigned.pop() if assigned else 'Textile'
        sections[section].append(a)
    company_links=' · '.join(link(section,'#'+section.lower()) for section in company_order)
    mainlines=['## Writing index','',f'Researched {DAY}. **{len(catalogue)} distinct articles, papers, and guides across {sum(len(a["editions"]) for a in catalogue)} publication URLs**, plus **{len(social)} X posts, threads, and articles** listed separately below. Another {len(unresolved)} historical article URLs await metadata.','', '**Jump to:** '+company_links+' · [Papers and workshops](#papers-and-workshops) · [Other team bylines](#other-team-bylines) · [X posts and long-form writing](#x-posts-and-long-form-writing).','', 'Company publications include guest contributors. A company byline is retained when a migration no longer exposes the original individual author. Dates come from article metadata, feeds, publication cards, or explicitly documented source records. Gist dates are public creation dates; unknown publication days remain unknown. Article bodies are not republished.','', 'See [coverage and gaps](research/coverage.md), [the second research pass](research/second-pass.md), [URL-only historical candidates](indexes/unresolved.md), [linked reading](indexes/linked-reading.md), and [machine-readable catalogue](data/catalogue.json).','']
    for collection in company_order+['Papers and workshops','Other team bylines']:
        rows=sections[collection]
        mainlines += ['### '+collection,'',str(len(rows))+' distinct articles, papers, or guides.','']+table(rows)+['']
    mainlines += ['### X posts and long-form writing','', 'Public-web research covered 2016-10-15 through 2026-10-15 for @andrewxhill, @carsonfarmer, and @sanderpick. This is a recovered selection, not a complete timeline. Descriptive post titles are editorial; thread continuations count as one entry. Article announcements are labelled separately. The long-form Carson article is broader team writing about AI development. [Evidence and missing posts](research/second-pass.md#x-and-twitter-2016-2026) · [structured social records](data/social-posts.json).','', '| Date | Post / thread | Byline | Format / topic | Evidence / reading |','| --- | --- | --- | --- | --- |']
    for a in sorted(social,key=lambda x:(x['date'],x['title']),reverse=True):
        access=[link('metadata',a['sources'][0])]
        access += [link('part '+str(i+2),'https://x.com/'+a['handle']+'/status/'+post_id) for i,post_id in enumerate(a['post_ids'][1:])]
        if a.get('reading_url'):access.append(link('saved public copy',a['reading_url']))
        mainlines.append('| '+a['date']+' | '+link(a['title'],a['url'])+' | '+esc(', '.join(a['authors']))+' | '+esc(a['kind']+'; '+a['scope'])+' | '+'; '.join(access)+' |')
    mainlines += ['']
    related=[a for a in catalogue if a['collection']=='Ceramic / 3Box']
    mainlines += ['### Ceramic / 3Box','',str(len(related))+' distinct articles in the separate [Ceramic / 3Box historical index](indexes/ceramic-3box.md).','']
    recordings=sum(bool(a['video_url']) for a in talks)
    slides_only=len(talks)-recordings
    talk_summary=f'**{len(talks)} technical sessions**: {recordings} recordings'
    if slides_only:
        talk_summary+=f' and {slides_only} presentations with slides only'
    talk_summary+=f'; {sum(bool(a["slides_url"]) for a in talks)} sessions include slides.'
    mainlines += ['## Talks and workshops','',talk_summary+' Direct recordings and slide decks are linked below. Dates marked **video** or **slides** are publication dates; unmarked dates are verified event dates.','', 'Conference presentations, developer workshops, and substantial code walkthroughs. Marketing, token announcements, highlights, community calls, and short previews are excluded. A few code walkthroughs are published on Recall Network; the source does not name their individual presenters, so they retain channel attribution. [Research and selection notes](research/talks.md) · [structured session records](data/talks.json).','', '| Date | Presentation / workshop | Speakers | Event / subject | Video | Slides / materials |','| --- | --- | --- | --- | --- | --- |']
    for a in sorted(talks,key=lambda x:(x['date'],x['title']),reverse=True):
        date=a['date']+({'video publication':' (video)','slides publication':' (slides)'}.get(a['date_basis'],''))
        speakers=', '.join(a['speakers']) or 'Not individually credited ('+a['publisher']+')'
        watch='—'
        if a['video_url']:
            minutes,seconds=divmod(a['duration_seconds'],60)
            watch=link('Watch · '+str(minutes)+':'+str(seconds).zfill(2)+(' · '+a['video_access'] if a.get('video_access') else ''),a['video_url'])
        materials=([link('Slides',a['slides_url'])] if a['slides_url'] else [])+[link(m['label'],m['url']) for m in a['materials']]
        mainlines.append('| '+date+' | '+esc(a['title'])+' | '+esc(speakers)+' | '+esc(a['event']+' — '+a['topic'])+' | '+watch+' | '+('; '.join(materials) or '—')+' |')
    mainlines += ['']
    start='<!-- BEGIN GENERATED WRITING INDEX -->'
    end='<!-- END GENERATED WRITING INDEX -->'
    readme=ROOT/'README.md'
    introduction=readme.read_text().split(start,1)[0].rstrip()
    readme.write_text(introduction+'\n\n'+start+'\n\n'+'\n'.join(mainlines).rstrip()+'\n\n'+end+'\n')
    (ROOT/'indexes/ceramic-3box.md').write_text('\n'.join(['# Ceramic / 3Box historical writing','', 'Related team history, kept separate from Textile / Tableland / Basin / Recall. This collection includes official publication contributors; inclusion does not by itself establish employment.','',str(len(related))+' distinct articles.','']+table(related))+'\n')
    # Every recognized blog-shaped outbound URL retains the referring company article.
    lines=['# Linked reading','', 'Blog/article-shaped links extracted from accessible company posts. Inclusion establishes a citation, not team authorship. Some are site sections or unavailable historical links; these are explicitly labelled. The complete, unfiltered outbound URL inventory is in [outbound-links.json](../data/outbound-links.json).','', '| Article / linked label | Destination | Byline | Metadata | Linked from |','| --- | --- | --- | --- | --- |']
    for a in sorted(linked,key=lambda x:x['url']):
        label=a.get('title') or next((x for x in a.get('anchor_texts',[]) if len(x)>4),a['url'])
        label=label[:180]
        lines.append('| '+esc(label)+' | '+link(urlsplit(a['url']).netloc,a['url'])+' | '+esc(', '.join(a.get('authors',[])) or 'Unknown')+' | '+(a.get('date') or 'Unverified')+'; HTTP '+str(a.get('http_status') or 'unavailable')+' | '+'; '.join(link('source '+str(i+1),u) for i,u in enumerate(a.get('linked_from',[])))+' |')
    (ROOT/'indexes/linked-reading.md').write_text('\n'.join(lines)+'\n')
    lines=['# Historical URLs awaiting article metadata','', 'These article-shaped URLs were captured in Internet Archive CDX, but article metadata could not yet be confirmed from accessible article or listing content. They remain candidates and are excluded from confirmed article counts. Capture dates below are not publication dates. Some may be editions of articles already indexed.','', 'See the [second-pass recovery report](../research/recovery-pass-2/report.md) for the outcome of all 88 original candidates, including routes excluded as non-articles.','', '| Original URL | Archive capture | Reading link |','| --- | --- | --- |']
    cdx={normal(x['original']):x for x in json.loads((ROOT/'research/textile-wayback-cdx.json').read_text())}
    for a in sorted(unresolved,key=lambda x:x['url']):
        cap=cdx.get(normal(a['url']),{}).get('timestamp') or (re.search(r'/web/(\d{14})',a.get('archive_url') or '').group(1) if re.search(r'/web/(\d{14})',a.get('archive_url') or '') else 'Unknown')
        lines.append('| '+link(a['url'],a['url'])+' | '+cap+' | '+(link('Wayback',a['archive_url']) if a.get('archive_url') else 'Unavailable')+' |')
    (ROOT/'indexes/unresolved.md').write_text('\n'.join(lines)+'\n')
    counts=collections.Counter(a['collection'] for a in catalogue)
    stats={'checked':DAY,'distinct_articles':len(catalogue),'edition_urls':sum(len(a['editions']) for a in catalogue),'collections':dict(counts),'url_only_candidates':len(unresolved),'linked_blog_candidates':len(linked),'linked_articles_with_metadata':sum(bool(a['date']) for a in linked),'articles_without_publication_date':sum(not a['date'] for a in catalogue),'outbound_urls':len(json.loads((ROOT/'data/outbound-links.json').read_text()))}
    stats['social_entries']=len(social)
    stats['social_post_urls']=sum(len(a['post_ids']) for a in social)
    stats['talk_sessions']=len(talks)
    stats['talk_recordings']=sum(bool(a['video_url']) for a in talks)
    stats['talks_with_slides']=sum(bool(a['slides_url']) for a in talks)
    (ROOT/'research/counts.json').write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
