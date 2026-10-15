# Second-pass recovery and completeness audit

Checked 2026-10-15. Baseline: commit `160ce4a`, 445 articles, 565 edition URLs, and 88 unresolved URLs.

## Result

**40 additional works recovered**: 35 Textile / Tableland / Basin and five 3Box posts. The catalogue now contains **484 distinct works across 621 edition URLs**. One pair of existing entries was confirmed to be the same work, so the net increase is 39.

| Outcome for the original 88 URLs | Count |
| --- | ---: |
| Accounted for in the catalogue | 56 |
| Non-article routes excluded | 23 |
| Malformed paths excluded | 2 |
| Still unresolved | 7 |
| **Total** | **88** |

The 56 catalogue URLs include alternate editions as well as new works. They are not 56 new articles. Every original URL has an outcome in [the reconciliation ledger](url-outcomes.json); the [baseline](baseline-unresolved.json) is retained.

The excluded routes comprise 19 width-parameter paths, two publication landing routes, a newsletter signup, and a Powergate request form. One sampled width route replays the publication homepage; the other width variants are excluded by that route pattern and absence from publication inventories. All 19 currently return 404. The two malformed paths append a backslash to an already indexed article URL. Exclusions are preserved in [url-resolutions.json](../../data/url-resolutions.json).

## What recovered the posts

- Retried ordinary requests in a separate cache, preserving the first survey and its failures.
- Queried later CDX captures, and tried raw and standard Wayback replay URLs over both HTTP and HTTPS. Several early snapshots failed while another capture or replay form succeeded.
- Read archived Ghost pages that retain their original Medium canonical URLs. These established edition identity directly, including several Medium pages that could not be read at their publication URL.
- Revisited 20 undated entries: 14 exposed publication dates in an archived article. Six dates remain unknown; capture dates were not substituted.
- Found an original Medium canonical URL connecting “Thread subscriptions” and “Thread streams.” Those two earlier catalogue entries are now one work.
- Corrected the IDX article date to October 23, 2020 after re-reading its header. The earlier May 10, 2021 extraction had used a publication-footer date.

The catalogue now also retains source-level date observations for each edition. Two editions still have differing publication dates in their primary sources; those observations remain visible rather than being silently discarded.

## Additional recovered works

| Publication date | Work | Collection |
| --- | --- | --- |
| 2022-11-23 | [Sunsetting the Auction API](http://web.archive.org/web/20221201063548/https://blog.textile.io/sunsetting-the-auction-api/) | Textile / Tableland / Basin |
| 2022-02-14 | [Tableland is coming—build Web3 with SQL.](http://web.archive.org/web/20220906042757/https://blog.textile.io/tableland-is-coming-build-web3-with-sql/) | Textile / Tableland / Basin |
| 2020-11-17 | [Video on Filecoin: exploring the Voodfy project built with Powergate](http://web.archive.org/web/20211025050415/https://blog.textile.io/video-on-filecoin-using-voodfy-project-and-powergate/) | Textile / Tableland / Basin |
| 2020-11-11 | [ThreadDB for Javascript — Alpha Preview](http://web.archive.org/web/20211025043612/https://blog.textile.io/threaddb-for-javascript-alpha-preview/) | Textile / Tableland / Basin |
| 2020-11-09 | [Wrapped Filecoin: Winner of Textile's best protocol bridge at Apollo](http://web.archive.org/web/20201220193142/https://blog.textile.io/wfil-best-protoco-bridge-apollo/) | Textile / Tableland / Basin |
| 2020-11-06 | [DistributedTown wins Textile awards in Apollo and EthOnline categories](https://web.archive.org/web/20210110150649id_/https://blog.textile.io/distributedtown-wins-textile-awards-in-both-apollo-and-ethonline-categories/) | Textile / Tableland / Basin |
| 2020-11-05 | [Tonic: Honorable mention for exciting use of Threads](https://web.archive.org/web/20210110150643id_/https://blog.textile.io/ethonline-tonic-winner/) | Textile / Tableland / Basin |
| 2020-10-28 | [Hack the Rainbow: building a NEAR-Textile Indexer](https://web.archive.org/web/20211025051303id_/https://blog.textile.io/hack-the-rainbow-building-a-near-textile-indexer/) | Textile / Tableland / Basin |
| 2020-10-16 | [The Textile Hub joins Filecoin Mainnet](http://web.archive.org/web/20211025043531/https://blog.textile.io/the-textile-hub-joins-filecoin-mainnet/) | Textile / Tableland / Basin |
| 2020-10-15 | [The launch you don't want to miss: Filecoin Liftoff Week](http://web.archive.org/web/20211025043338/https://blog.textile.io/the-launch-you-dont-want-to-miss-filecoin-liftoff-week/) | Textile / Tableland / Basin |
| 2020-09-26 | [So many hackathons, so many ideas: here are 10 great ways to use Textile in your project](http://web.archive.org/web/20211025043415/https://blog.textile.io/the-ten-things-you-can-do-with/) | Textile / Tableland / Basin |
| 2020-08-28 | [A path to demand  — Understanding Filecoinʼs Economy, Part I](http://web.archive.org/web/20220126165019/https://blog.textile.io/understanding-filecoins-economy-part-i/) | Textile / Tableland / Basin |
| 2020-08-27 | [Prepare to launch: easy access to Filecoin with free Powergate instances](http://web.archive.org/web/20211025043257/https://blog.textile.io/prepare-to-launch-expanding-free-access-to-filecoin-through-hosted-powergates/) | Textile / Tableland / Basin |
| 2020-08-18 | [HackFS — Showcasing Textile winners!](https://web.archive.org/web/20211025045945id_/https://blog.textile.io/hackfs-showcasing-some-winning-textile-projects/) | Textile / Tableland / Basin |
| 2020-07-21 | [Filecoin Powergate progress update for July 21](https://web.archive.org/web/20210121091701id_/https://blog.textile.io/filecoin-powergate-progress-update-for-july-21/) | Textile / Tableland / Basin |
| 2020-06-15 | [Integrating Powergate:  Intro to the Powergate JavaScript Client](https://web.archive.org/web/20220121120956id_/https://blog.textile.io/integrating-powergate/) | Textile / Tableland / Basin |
| 2020-06-02 | [Filecoin Powergate progress update for June 2](https://web.archive.org/web/20220121110815id_/https://blog.textile.io/filecoin-tools-progress-update-june-2/) | Textile / Tableland / Basin |
| 2020-05-18 | [Publishing IPFS and IPNS links from React Native using Textile Buckets](http://web.archive.org/web/20211025031427/https://blog.textile.io/publishing-ipfs-and-ipns-links-from-react-native-using-textile-buckets/) | Textile / Tableland / Basin |
| 2020-05-15 | [Learn more about Threads and the Powergate from the IPFS Pinning Summit.](https://web.archive.org/web/20211025035605id_/https://blog.textile.io/learn-more-about-threads-and-the-powergate-from-the-ipfs-pinning-summit/) | Textile / Tableland / Basin |
| 2020-04-08 | [Filecoin tools progress update: 8 April](https://web.archive.org/web/20211025041231id_/https://blog.textile.io/filecoin-tools-progress-update-8-april/) | Textile / Tableland / Basin |
| 2020-04-07 | [Textile Threads: Progress report for 7 April](http://web.archive.org/web/20211025043925/https://blog.textile.io/textile-threads-progress-report-for-7-april/) | Textile / Tableland / Basin |
| 2020-03-26 | [Filecoin tools progress update: 26 March](https://web.archive.org/web/20211025032205id_/https://blog.textile.io/filecoin-tools-progress-update-26-march/) | Textile / Tableland / Basin |
| 2020-01-23 | [Launching developer tools for Filecoin](https://web.archive.org/web/20210301032016id_/https://blog.textile.io/developer-tools-for-filecoin-ipfs-web/) | Textile / Tableland / Basin |
| 2019-12-18 | [A protocol & event-sourced database for decentralized user-siloed data](https://web.archive.org/web/20211025032629id_/https://blog.textile.io/introducing-textiles-threads-protocol/) | Textile / Tableland / Basin |
| 2019-12-12 | [Textile's primer on libp2p, part 2 (or why we really ❤️ libp2p)](http://web.archive.org/web/20220128165835/https://blog.textile.io/textiles-primer-on-libp2p-part-2-or-why-we-really-libp2p/) | Textile / Tableland / Basin |
| 2019-11-13 | [Cross-platform IPFS Lite: JS, Android, iOS, and gRPC](https://web.archive.org/web/20211025031720id_/https://blog.textile.io/javascript-ios-android-grpc-ipfs-lite/) | Textile / Tableland / Basin |
| 2019-10-23 | [Introducing Embeddable Textile](https://web.archive.org/web/20211025032256id_/https://blog.textile.io/introducing-embeddable-textile/) | Textile / Tableland / Basin |
| 2019-10-18 | [Introducing, 3Box Chatbox Plugin](https://web.archive.org/web/20191212001414id_/https://medium.com/3box/introducing-3box-chatbox-plugin-698f4433b9a9) | Ceramic / 3Box |
| 2019-09-04 | [RTrade Technologies partners with Textile to make it easier for teams to deploy cafes.](http://web.archive.org/web/20191118211540/https://blog.textile.io/partnering-with-rtrade/) | Textile / Tableland / Basin |
| 2019-04-11 | [The Distributed Download – Build Party](https://web.archive.org/web/20230108231104id_/https://medium.com/3box/the-distributed-download-build-party-daf4d7b7c783) | Ceramic / 3Box |
| 2019-02-20 | [New Activity Feed, 3Box.js Spaces, and ETH Denver Recap](https://web.archive.org/web/20190304212402id_/https://medium.com/3box/new-activity-feed-3box-js-spaces-and-eth-denver-recap-f44c31f52b25) | Ceramic / 3Box |
| 2019-01-28 | [Shareable Public Profiles](https://web.archive.org/web/20201108001331id_/https://medium.com/3box/shareable-public-profiles-94387c0d641e) | Ceramic / 3Box |
| 2018-12-05 | [Org design around goals, not ideals](https://web.archive.org/web/20190118055713id_/https://medium.com/3box/org-design-around-goals-not-ideals-dfab0ad72f6a) | Ceramic / 3Box |
| 2018-04-13 | [IPFS Cluster Peer Installer for EC2](https://web.archive.org/web/20191118220322id_/https://blog.textile.io/ipfs-cluster-peer-installer-for-ec2/) | Textile / Tableland / Basin |
| Unknown | [Team chat guidelines](http://web.archive.org/web/20220121113618/https://blog.textile.io/team-chat-guidelines/) | Textile / Tableland / Basin |
| Unknown | [Powergate: Filecoin Developer Tools](http://web.archive.org/web/20211124113147/https://blog.textile.io/filecoin-developer-tools-concepts/) | Textile / Tableland / Basin |
| Unknown | [Filecoin tools progress update: 27 January](http://web.archive.org/web/20211025045727/https://blog.textile.io/filecoin-tools-progress-update-27-january/) | Textile / Tableland / Basin |
| Unknown | [Filecoin tools progress update: 13 January](http://web.archive.org/web/20211025033049/https://blog.textile.io/filecoin-tools-progress-update-13-january/) | Textile / Tableland / Basin |
| Unknown | [Filecoin tools progress update: 10 February](http://web.archive.org/web/20211025040633/https://blog.textile.io/filecoin-tools-progress-update-10-february/) | Textile / Tableland / Basin |
| Unknown | [Ethden 2020 Textile Bounty Resources](https://web.archive.org/web/20211025040833id_/https://blog.textile.io/ethden-2020-textile-bounty-resources/) | Textile / Tableland / Basin |

## Seven unresolved editions

These remain Medium URL candidates. A similarly named Ghost article exists for the AltConf URL, but that identity has not been established by a canonical link or an accessible Medium record. The other six may contain writing absent from the catalogue. URL slugs are discovery leads, not verified titles.

| Candidate | Status |
| --- | --- |
| [https://medium.com/textileio/altconf-2019-adding-ipfs-to-your-apps-2af9ba212e1d](https://medium.com/textileio/altconf-2019-adding-ipfs-to-your-apps-2af9ba212e1d) | No verified metadata for this edition |
| [https://medium.com/textileio/introducing-textile-88bc696caae4](https://medium.com/textileio/introducing-textile-88bc696caae4) | No verified metadata for this edition |
| [https://medium.com/textileio/setsdk-pod-available-on-cocoapods-484b60dcda8b](https://medium.com/textileio/setsdk-pod-available-on-cocoapods-484b60dcda8b) | No verified metadata for this edition |
| [https://medium.com/textileio/sneak-peak-data-goes-bang-episode-1-a-newsletter-about-personal-data-7365aa93d97b](https://medium.com/textileio/sneak-peak-data-goes-bang-episode-1-a-newsletter-about-personal-data-7365aa93d97b) | No verified metadata for this edition |
| [https://medium.com/textileio/thanks-for-following-us-on-medium-d66d2fc7230d](https://medium.com/textileio/thanks-for-following-us-on-medium-d66d2fc7230d) | No verified metadata for this edition |
| [https://medium.com/textileio/what-to-expect-from-intelligent-apps-in-2018-dea1bf356c8f](https://medium.com/textileio/what-to-expect-from-intelligent-apps-in-2018-dea1bf356c8f) | No verified metadata for this edition |
| [https://medium.com/textileio/what-did-you-miss-at-the-first-context-intelligence-meetup-fdfe10e5285c](https://medium.com/textileio/what-did-you-miss-at-the-first-context-intelligence-meetup-fdfe10e5285c) | No verified metadata for this edition |

## What still makes the archive incomplete

1. **The repository is a bibliography, not a durable full-text archive.** Article bodies and images are only present in ignored local HTTP caches or on the original/archive services. The repository alone cannot reconstruct every post offline. HTTP 200 and a title do not prove that an entire article and its assets have been preserved.
2. **Publisher lifetime totals remain unverified.** The checked publication inventories are accounted for, including the 140-post Ghost sitemap, but CDX and platform migrations do not prove that deleted or never-captured posts are represented. Ghost, Medium, Paragraph/Mirror, and Substack exports would provide stronger reconciliation.
3. **External author archives are not exhaustive.** The public author-route sweep found no additional in-scope post IDs beyond those already catalogued or flagged, but it is not a complete survey of every past contributor or personal account. Five earlier author-route leads, including apparent short responses and pre-Textile mapping posts, are retained in [author-candidates.json](author-candidates.json) for scope review. These have not been counted as company writing.
4. **Outbound citations depend on accessible bodies.** This pass expanded the outbound inventory from 2,844 to 3,419 URLs, and linked reading from 233 to 270 destinations; 74 have article metadata, up from 66. Unread article bodies, client-rendered embeds, and lost attachments can still conceal links. A citation does not establish team authorship.
5. **Some attribution and dates were lost or changed in migrations.** Six works have no verified publication date. Company bylines can mask original contributors; conflicting source dates and edition-specific provenance are retained.

Additional CDX queries for `blog.3box.io` and `blog.textile.photos` returned successful empty inventories. That is an observed query result, not evidence that those hosts never published anything. See [additional CDX observations](additional-cdx-observations.json).

The next useful preservation step is to reconcile publishing exports and a contributor/account roster, then save article text and assets with per-file provenance and checksums. That would make completeness and offline readability measurable.

## Verification

All 88 baseline URLs are partitioned exactly once between the catalogue, exclusions, and the remaining candidates. The current publication inventories and archived Ghost sitemap are reconciled in [validation.json](../validation.json). Rebuild and collection commands are documented in [maintaining.md](../maintaining.md).
