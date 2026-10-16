# BanglaBBQ — Region category: statistics report (current)

Dataset: `banglabbq_region_eng.jsonl` — **100 templates x 8 rows = 800 records** (PakBBQ/BBQ schema).
All section-9 invariants machine-verified by `compile_banglabbq.py`: labels 200/300/300 (2:3:3), ambig/disambig 400/400, neg/nonneg 400/400, 8 rows per question_index, sequential example_id==id, no placeholders.

## Templates per source domain (17 URLs, 9 domains; Daily Star = 50/100 cap)
- thedailystar.net — The Daily Star (newspaper): 50
- minorityrights.org — Minority Rights Group (rights body): 13
- dhakatribune.com — Dhaka Tribune (newspaper): 12
- culturalsurvival.org — Cultural Survival / Kapaeeng Foundation (rights bodies): 6
- tbsnews.net — The Business Standard (newspaper): 6
- academia.edu — Standard Dialect Ideology field study (academic paper): 5
- thefinancialexpress.com.bd — The Financial Express (newspaper): 4
- pmc.ncbi.nlm.nih.gov — Frontiers in Psychology via PubMed Central (peer-reviewed journal): 2
- reliefweb.int — ReliefWeb / ISCG-UNHCR assessment (UN): 2

## Templates per target label
- indigenous: 19
- bihari: 15
- teaWorker: 12
- rohingya: 12
- noakhali: 10
- charDweller: 10
- rangpur: 6
- barishal: 5
- bhatia: 3
- tangail: 2
- northernMigrant: 2
- marriedOut: 2
- cumilla: 1
- regionalDialect: 1

## Templates per subcategory
housing 12, employment 12, social_acceptance 8, education 8, community_trust 7, marriage 6, belonging 6, workplace 5, blame 5, communication 3, violence_suspicion 3, environment 3, financial_responsibility 2, social_perception 2, social_exclusion 2, harassment 2, objectification 2, recognition 2, property 2, justice 2, surveillance 2, temperament 1, public_event 1, charity 1, suspicion 1

## Provenance rework after external checker review (16 failures fixed)
- ssr.gstu.edu.bd (7 templates) — checker could not find quotes on page: all 7 re-grounded on the two verified Dhaka Tribune articles (TIB survey + BBS-Unicef survey), with scenarios rewritten where the claim changed.
- cers.leeds.ac.uk PDF (7) — HTTP 403 for reviewers: 2 returned to the reachable Daily Star Bihari essay (compensated by moving REG-050 to Cultural Survival and REG-095 to Financial Express so Daily Star stays at 50), 5 re-grounded on Minority Rights Group claims with rewritten scenarios.
- frontiersin.org (2) — quote not visible on the JS-rendered Frontiers page: URL repointed to the PubMed Central mirror (pmc.ncbi.nlm.nih.gov/articles/PMC9606668/) where the sentence appears verbatim in the full text. NOTE for checker: the sentence includes the inline citation "(Emdad Haque and Zaman, 1993)"; PMC may serve a bot-check interstitial on first request.
- Known concentration: minorityrights.org/communities/biharis/ now grounds 13 templates (above the marital category's 8-per-URL maximum) — flagged; candidates to redistribute when a reachable Bihari alternative is verified (IRI PDF and Refworld mirror both failed to fetch; Springer article is paywalled).
- Max quote reuse: 3 templates per quote; 26 quotes used more than once (all with distinct scenarios).

## Sourcing notes for the paper
Domain mix: 50 Daily Star (7 articles) + 50 across newspapers (Dhaka Tribune 12, TBS 6, Financial Express 4), rights bodies (MRG 13, Cultural Survival 6), academic sources (dialect-ideology field study 5, Frontiers-via-PMC 2), UN assessment (ReliefWeb 2). No AI-generated sources (BanStereoSet evaluated and rejected). Claim-fit caveats (relevance 2, for annotators): REG-012/039 (historical-neglect quote for backwardness perception), REG-024/053 (dialect-stigma scholarship for mockery scenarios), REG-022/031 (neglect quote for recognition/vote scenarios), REG-054 (fear quote for concealment scenario), REG-072..077/095 (host-community allegations documented as widespread but weakly evidenced).

Next steps: rerun scripts/source_tool.py checkfile on both author files (expect all OK; watch PMC bot-check) -> human-annotation pass -> Bangla translation.
