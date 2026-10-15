# Second research pass: Andrew Hill, Carson Farmer, and Sander Pick

Researched **2026-10-15**. The requested ten-year window is **2016-10-15–2026-10-15**. This pass adds **13 distinct articles, papers, workshops, and guides**, supplements bylines on **8 existing articles**, and adds **8 social entries covering 11 post URLs**. Social entries are counted separately from articles. Everything is linked directly from the [README](../README.md#writing-index).

## GitHub repositories and personal publishing

The public GitHub API returned **180 Textile repositories**, **62 Tableland repositories**, and **60 Recall repositories**. Repository names and descriptions were searched for publishing, documentation, papers, workshops, and website material. Selected source trees and Markdown were then read. These are public-repository inventories, not claims about private or deleted repositories.

| Source | Finding and disposition |
| --- | --- |
| [textileio/papers](https://github.com/textileio/papers/tree/master/whitepaper) | Recovered the Threads whitepaper draft. [Author metadata](https://github.com/textileio/papers/blob/master/whitepaper/metadata.yaml) names Sander Pick, Carson Farmer, Aaron Sutula, Irakli Gozalishvili, Ignacio Hagopian, and Andrew Hill. Draft 1.7 is labelled March 2020; the exact publication day remains unknown. The source includes the draft and a built PDF; these are one work. |
| [textileio/ipfs-camp-2019](https://github.com/textileio/ipfs-camp-2019) | Recovered *Building DApps with Textile, the iCloud for the DWeb*. Speaker notes explicitly identify Carson Farmer. The conference year is known; no publication day was inferred from Git history. |
| [textileio/community](https://github.com/textileio/community) | Read the documentation tree, including static-site, identity, authentication, Threads, and Buckets tutorials. These provide surviving technical context and article links. Generic documentation and a repository maintainer list do not establish individual article authorship, so they were not bulk-added as personal posts. |
| [textileio/workshops](https://github.com/textileio/workshops) | Contains the September 2020 Powergate and Buckets masterclasses. The READMEs do not expose individual bylines. Retained as discovery evidence rather than assigning them to a maintainer. |
| [gatsby-ipfs-blog](https://github.com/textileio/gatsby-ipfs-blog), [jekyll-ipfs-blog](https://github.com/textileio/jekyll-ipfs-blog), [hugo-ipfs-blog](https://github.com/textileio/hugo-ipfs-blog) | These are publishing templates. Sample posts are starter content, not a recovered Textile publication archive, and are excluded. |
| [textileio/go-libp2p-primer-article](https://github.com/textileio/go-libp2p-primer-article) | Companion example code, not another edition of the motivating article. Excluded as a separate article. |
| [textileio/textile.photos](https://github.com/textileio/textile.photos), [tablelandnetwork/site-tableland](https://github.com/tablelandnetwork/site-tableland) | Website source trees inspected; no additional individually attributed blog archive recovered. |
| [tablelandnetwork/weeknotes](https://github.com/tablelandnetwork/weeknotes) | The tree contains a README pointing to the already-enumerated Substack publication; no additional post files. |
| [recallnet/docs](https://github.com/recallnet/docs) | Documentation tree inspected. Generic API/product documentation is not treated as individually authored long-form writing. |
| [Andrew's Gists](https://gist.github.com/andrewxhill) | Enumerated 257 public Gists across three API pages. Added seven substantive Textile/Recall/Tableland/Basin guides or notes: Recall/Mastra, random-access formats for Basin, two workshops, Powergate Show & Tell, command-line tag, and composable Threads. Short link lists, unrelated material, code-only snippets, and identity proofs are excluded. |
| [Carson's Gists](https://gist.github.com/carsonfarmer) | Enumerated 58 public Gists. Added the Buckets/Threads workshop and an agent evaluation guide. The latter is broader team writing about AI evaluations, not a claimed Recall product publication. |
| [Sander's Gists](https://gist.github.com/sanderpick) | Enumerated 36 public Gists. No Markdown long-form article recovered; code and diagnostic logs are not counted as articles. |
| Personal websites | Andrew's [site](https://andrewxhill.com/) and [source](https://github.com/andrewxhill/andrewxhill.github.io) expose older posts ending in January 2016, outside this window. Carson's [current site](https://carsonfarmer.com/) is a link page; the [older blog source](https://github.com/carsonfarmer/blog) covers earlier geographic research rather than Textile/Recall publishing. |

Requests for `textileio/blog`, `textileio/website`, `textileio/textile.io`, and `textileio/blog.textile.io` returned GitHub API 404. That establishes only that these names were not publicly readable in this pass; it does not establish that they never existed.

Gist attribution uses the public owner and verified document contents. Gist dates are **creation timestamps**, not article masthead dates or last-edit dates. Filename titles are retained for `composable_threads.md` and `Random Access File Formats.md`. Metadata and provenance are in [github-articles.json](../data/github-articles.json); full source text remains outside the tracked repository.

## Other publications and recovered bylines

- Carson's [Techdirt essay on IPFS and long-term preservation](https://www.techdirt.com/2020/05/05/decentralized-web-could-help-preserve-internets-data-1000-years-heres-why-we-need-ipfs-to-build-it/) has a May 5, 2020 masthead and a closing Textile affiliation. It was missing from the catalogue. Ordinary HTTP returned 403; the public web reader exposed the article and byline.
- [*Decentralized identifiers for peer-to-peer service discovery*](https://dl.ifip.org/db/conf/networking/networking2021/1570714336.pdf) names Carson Farmer, Sander Pick, and Andrew Hill. The [conference program](https://networking.ifip.org/2021/program/workshops.html) corroborates the authors. [Crossref's record](https://api.crossref.org/works/10.23919/IFIPNetworking52078.2021.9472201) supplies the publication date **2021-06-21**, distinct from its July deposit date. The publisher PDF was readable through the web reader; ordinary HTTP timed out.
- Read the article-specific Paragraph author objects for all **96 current Textile and Recall posts**. Recovered Andrew's byline on *Introducing Basin*, *Unlocking the future of data*, *Model Arena: GPT-5 Predictions v. Reality*, and *Recall Model Arena*. Recovered Carson's byline on *Our Vision for Agent Discovery* and *Recall Rank*. *$RECALL: Skill Markets for AI* credits both Andrew and Carson, alongside Dataliquidity. Existing company metadata remains in the source records; publication-wide team lists were not used as post bylines.
- The [Threads architecture article](https://medium.com/textileio/wip-textile-threads-whitepaper-just-kidding-6ce3a6624338) explicitly credits **Carson Farmer and Sander Pick** in its body, even though Medium's account masthead shows only Carson. Added the missing coauthor. The encryption article's three-author credit was already represented.

These additions and byline supplements are in [second-pass-articles.json](../data/second-pass-articles.json). Interviews and podcasts about the team are discovery leads, not automatically team-authored essays.

## X and Twitter, 2016-2026

Searched all three handles with Textile, Tableland, Basin, and Recall terms; tried X/Twitter domain searches, Thread Reader author pages, public profile mirrors, and date-bounded searches for 2016–2019, 2020–2023, and 2024–2026. Search date operators returned out-of-period profile pages, so their results were **not** treated as proof of publication dates or complete historical coverage. Public X/Thread Reader search returned no usable historical inventory. Internet Archive CDX attempts timed out or returned 503.

The most productive routes were links embedded in earlier company posts, Andrew's Tableland workshop resources, and public profile mirrors. Exact post IDs were then checked against FxTwitter's public JSON for the original account, text, timestamp, and reply relationship. X may return a JavaScript shell with HTTP 200; that alone does not verify a post's contents.

| Account | Confirmed selection | Limits |
| --- | --- | --- |
| [@andrewxhill](https://x.com/andrewxhill) | Two 2026 threads about Recall's Codecontext and Mainline tools (three and two posts respectively); a 2022 Tableland/Solidity workshop post; two 2019 Textile/IPFS posts. | Descriptive titles are editorial. The IPFS Camp entry announces an already-catalogued article and is labelled accordingly. These are not a full timeline. |
| [@carsonfarmer](https://x.com/carsonfarmer) | Two 2019 Textile/IPFS posts and the 2026 X article [*My code is disposable now*](https://x.com/carsonfarmer/status/2107531595637010616). | The X article is broader team writing about AI development rather than a Recall product essay. Its title and original-post URL are corroborated by a [saved public copy](https://hraness.com/reading/my-code-is-disposable-now) and FxTwitter article metadata. October 6 is the sharing-post/public-copy date; an article ID was not converted into an invented publication date. |
| [@sanderpick](https://x.com/sanderpick) | Two original post URLs survive in Textile articles. | Both returned FxTwitter 404; one original X URL also returned 404. Without readable post contents, neither is counted as a confirmed writing entry. No claim that Sander never posted, or that the posts were deleted, follows from these errors. |

**Unrecovered leads:**

| Lead | Evidence | Next useful source |
| --- | --- | --- |
| [Sander post 1068279840946585600](https://x.com/sanderpick/status/1068279840946585600) | Linked from [Textile's November 2018 update](https://medium.com/textileio/textile-update-november-2018-a20282462af7) and the [IPFS framework article](https://medium.com/textileio/showing-how-textiles-framework-can-help-transmit-meaningful-data-over-ipfs-6795f255e079). | A readable archived embed or account export. The embedding article's date is not the tweet's date. |
| [Sander post 1068297685227061249](https://x.com/sanderpick/status/1068297685227061249) | Linked from the same IPFS framework article; FxTwitter 404. | A readable archived embed or account export. |
| Andrew's long-form “Day 1” post about Recall and verifiable AI | Search exposed a repost on [this public mirror profile](https://instalker.org/shinsaku6356), but opening the profile exposed a different snapshot. | Original status URL and a stable dated copy. Excluded from confirmed entries; relative “months ago” labels were not used as dates. |

[social-posts.json](../data/social-posts.json) retains metadata and evidence endpoints, not full tweet or article bodies. It includes one record per thread, with every verified continuation ID. Recovery is concentrated in **2019, 2022, and 2026**; **2016–2018, 2020–2021, and 2023–2025 remain substantial social-history gaps**. A public-web pass cannot establish a ten-year lifetime total without complete account exports or another reliable historical inventory.
