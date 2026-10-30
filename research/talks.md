# Technical talks and workshops

Research date: **2026-10-15**. The [table in README](../README.md#talks-and-workshops) contains **19 recorded sessions**, five with slide decks. Records and evidence are in [talks.json](../data/talks.json); sessions are counted separately from writing and X posts.

## Selection

Included technical conference presentations, developer workshops, research presentations, and substantial code walkthroughs associated with Set, Textile, Tableland, and Recall. Research primarily follows Andrew Hill, Carson Farmer, and Sander Pick; Joe Wagner's explicitly credited Tableland workshop is included too. Five clearly technical Tableland/Recall walkthroughs retain publisher attribution because the descriptions do not explicitly name the individual presenter.

Every row links directly to an individual recording or slide deck. Event listings, channel pages, schedules, and blog recaps are evidence sources, not the table's viewing destinations. Workshop code and notes are supplementary; they do not qualify a session without video or slides. Matching notes may also appear in the writing catalogue; one is the written resource and the other the recorded session.

Excluded token launches, airdrop instructions, promotional keynotes and teasers, marketing interviews, AMAs, town halls, community calls, short previews, unrelated speakers, and unattributed snippets. Technical content determines inclusion, rather than a channel's current name. For example, Sander's 2023 Tableland Functions experiment now appears on the Recall Network channel but explicitly describes a technical experiment and links its source code. Three 2025 MCP/Mastra coding sessions also meet the technical-content criterion. The HD and original upload of the MCP storage walkthrough are one session.

## Sources checked

| Discovery source | Confirmed resources |
| --- | --- |
| [O'Reilly's Strata 2017 session recording](https://www.oreilly.com/videos/strata-data-conference/9781491976326/9781491976326-video316462/) and [Carson's 2017 feature-extraction article](https://medium.com/textileio/on-device-feature-extraction-part-i-ee1b5902227) | *Learning location: Real-time feature extraction for mobile analytics*, 34:53, September 2017, New York. Andrew Hill confirmed that the opening slide credits him as the sole presenter. The recording is embedded on the individual session page; full viewing requires O'Reilly login. |
| [HackFS 2020 organizer archive](https://ethglobal.github.io/hackfs.com/) | Andrew's July 2 Filecoin/Powergate workshop and Carson/Andrew's July 7 Textile workshop. Exact recording URLs are corroborated by video descriptions and chapter credits. |
| [Andrew's Powergate notes](https://gist.github.com/andrewxhill/b0010d555ca4d79d9d1e78e380ad218e) | Matching July 2 slides and course notes. |
| [Carson's Buckets/Threads notes](https://gist.github.com/carsonfarmer/e7062ab30ddd4eb55812d64890db20d3) | Matching public *Getting started with Textile* slides. Followed the original short link into the public Google Slides presentation and checked its title and HTTP 200 response. |
| [IPFS Camp organizer source](https://github.com/ipfs/camp/blob/master/README.md) | The full *Building DApps with Textile* workshop, its PDF slides, and trainer credits for Ben Lupton, Carson Farmer, and Andrew Hill. The source links some short poster/deep-dive summaries too; those are not substituted for full talks. |
| [IPFS Web3 Weekend recap](https://blog.ipfs.tech/2021-06-08-web3-weekend/) | Andrew and Carson's recorded IPFS/Filecoin workshop. The recap embeds it under two subject headings; it is counted once. |
| [IPFS Pinning Summit recap](https://blog.ipfs.tech/2020-05-13-ipfs-pinning-summit-recap/) | Full recordings of *Into the Powergate* with Andrew Hill and Aaron Sutula, and Andrew's *Advanced Pinning Structures*. Matched the previously recovered Powergate and Threads/Buckets slide decks; video publication dates are distinct from the earlier deck publication dates. |
| [HackFS 2021 organizer schedule](https://ethglobal.com/events/hackfs2021) | Carson's Filecoin Bridge workshop, with the event date and exact recording ID. |
| [AltConf recording](https://www.youtube.com/watch?v=M6mUg-tMbk0) and [Textile's June 2019 update](https://medium.com/textileio/textile-update-june-2019-d596343ad67e) | Andrew's *Adding IPFS to your Apps* presentation. |
| [ETHDenver recording](https://www.youtube.com/watch?v=DpRaxjIiYew) | Carson's *Bring Your Own Data* talk. The video description explicitly gives the February 15, 2020 recording date. |
| [EASIER workshop site](https://workshop.easierdata.org/) | Carson's *From Maps, To Bits, And Beyond* recording. The organizer site's rendered application source supplies the direct YouTube link; the recording title/description confirms Carson and the research workshop. |
| [Andrew's Speaker Deck](https://speakerdeck.com/andrewxhill) | Three relevant technical decks: the matched HackFS Filecoin slides, *Into the Powergate*, and *Future of Pinning*. Read slide transcripts to confirm architecture, APIs, networking, encryption, configuration, and dynamic pinsets. Older map/cartography decks predate the requested period. *Space Race 2 — Slingshot* was excluded because its focus is support and project promotion. |
| [Textile's older YouTube channel](https://www.youtube.com/channel/UCQPmtkMrq8Owz9qWadZ7n1Q) | Six visible videos reviewed by metadata. The China summit recording mixes company mission and product promotion with a demo, so it was excluded under the requested filter. Short demonstrations and community calls are excluded too. |
| [Recall Network channel](https://www.youtube.com/channel/UCpFqp6DtxvXaP7LUjxT3KpA) | Enumerated 112 visible videos across the current channel and three continuation pages. Retained technical Tableland Functions, synthetic-data research, and three MCP/Mastra coding walkthroughs; rejected the marketing material. This is an inventory of currently visible videos, not a lifetime upload total. |
| Legacy Tableland workshop recordings on the same channel | Added the substantial Studio CLI and Data DAO coding workshops with channel attribution, plus Joe Wagner's explicitly credited Twitter-clone data workshop. Short demos remain excluded. |

The installed `yt-dlp` could not parse the channel's current video-card format and returned zero entries with warnings. That result was not treated as an empty channel. Channel enumeration instead read the public page data and its continuation responses directly. A request to the former `@tablelandxyz` handle returned 404; individual legacy recordings were still accessible on the current channel.

## Dates and access

- **Event dates** come from organizer schedules, explicit recording-date statements, or the recording's live broadcast timestamp. For example, ETHDenver's April upload is dated February 15 in the table because the description explicitly identifies the recording day.
- **Month-only dates** retain the verified precision. The Strata session is dated `2017-09`; its exact presentation day is unverified.
- **Video dates** are YouTube's publication timestamps; they do not establish when the talk occurred. IPFS Camp's June 2019 workshop was uploaded in September. EASIER's upload date is retained without inventing the workshop day.
- **Slide dates** come from the author's Speaker Deck publication page. They are not assumed to be stage dates.
- YouTube watch-page player metadata exposed the 18 YouTube recordings' titles, descriptions, durations, publication timestamps, channels, and `playabilityStatus: OK`. This is an access and metadata check, not a claim that each video was manually watched end to end. Speaker attribution uses explicit descriptions, organizer credits, or chapter labels. The five unnamed Tableland/Recall walkthroughs keep channel attribution rather than assigning them to the author of linked example code.
- **Strata presenter correction:** O'Reilly's catalogue combines credits for Sander Pick, Andrew Hill, and Carson Farmer at Set. Andrew Hill identified himself as the sole presenter from the opening slide, correcting that attribution. The table follows his correction. The researcher did not independently inspect the opening slide or full playback. Login-required recordings qualify and are labelled at their direct viewing link; free YouTube availability is not required.
- The IPFS Camp slides returned HTTP 200 and a PDF signature. Speaker Deck pages exposed readable slide transcripts; the public Google Slides deck returned HTTP 200 with the expected title. Raw video, captions, slide bodies, and page responses are not committed.

## Remaining leads and exclusions

| Candidate | Why it is not in the table |
| --- | --- |
| Carson's *Buckets of data: Easy APIs for off-chain data storage on IPFS + Filecoin*, ETHOnline, September 29, 2020 | The organizer's surviving schedule identifies Carson and the date but does not expose a recording link. A listing alone does not qualify. |
| Sander/Carson's NFT.NYC Rigs presentations | Draft programs expose talk listings, but no matching recording or slide deck was verified. Draft listings are insufficient to resolve the final presenter or delivery date. |
| September 2020 Powergate and Buckets masterclasses | Source notebooks and workshop notes survive in [textileio/workshops](https://github.com/textileio/workshops); no individual full recording or slide deck was verified for those exact sessions. |
| IPFS Camp *IPFS on Mobile*, poster sessions, and lightning introductions | Recovered video IDs include two-minute or shorter summaries/previews. They are not presented as full technical sessions. |
| Textile Build training-series link | A historical company post links the series, but its referenced video's oEmbed request returned 401. This does not prove the training series was deleted; a current readable recording still needs recovery. |
| Key-value-store walkthrough and brief Basin replication demos | Short technical demos, rather than substantial workshops or conference presentations. The longer Studio and Data DAO workshops are included with publisher-only attribution. |
| Recall launches, token/airdrop videos, highlights, and company-vision keynotes | Excluded by the requested non-marketing scope, even when a team member is on stage. |

The survey covers a recovered selection in 2017–2025, not a complete ten-year speaking history. Additional recordings on unindexed organizer channels, unavailable uploads, and privately shared slide decks remain possible gaps.
