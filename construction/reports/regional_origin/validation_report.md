# BanglaBBQ — Region category: validation report (current, single version)

Dataset state: 100 templates -> 800 records in `banglabbq_region_eng.jsonl`. Supersedes all earlier drafts. Incorporates the external checker review that found 16 provenance failures (GSTU quotes-not-on-page x7, Leeds PDF 403 x7, Frontiers quote-not-visible x2) — all 16 re-grounded or repointed; no template cites those hosts any more.

## Method
- Every source URL fetched live during construction; every source_quote verified verbatim against the fetched page text (ASCII-normalised quotes).
- Unverifiable-to-reviewers hosts removed even where my own fetch succeeded (Leeds CERS PDF, GSTU journal page, Frontiers-hosted page).
- Section 9 assertions machine-verified by `compile_banglabbq.py`.

## Source inventory (17 URLs, 9 domains)

| Source URL | Templates | IDs |
|---|---|---|
| thedailystar.net/ds/big-picture/news/stereotypes-struggle-and-survival-recl | 17 | 010, 011, 013, 014, 015, 038, 041, 042, 043, 044, 055, 081, 084, 085, 086, 087, 088 |
| minorityrights.org/communities/biharis/ | 13 | 019, 028, 030, 035, 040, 046, 047, 048, 054, 057, 092, 099, 100 |
| thedailystar.net/news/how-dhakas-rental-housing-market-marginalises-indigen | 12 | 056, 059, 062, 063, 064, 065, 066, 067, 068, 069, 070, 071 |
| thedailystar.net/shout/news/what-your-ancestral-home-really-says-about-you- | 8 | 001, 002, 003, 004, 005, 027, 032, 033 |
| dhakatribune.com/bangladesh/nation/163790/tib-tea-workers-still-denied-fund | 7 | 023, 025, 026, 051, 082, 096, 098 |
| culturalsurvival.org/news/alarming-trend-violence-against-indigenous-women- | 6 | 020, 049, 050, 058, 060, 091 |
| tbsnews.net/bangladesh/rohingya-influx-creates-jobs-locals-resentment-linge | 6 | 061, 072, 073, 074, 075, 076 |
| academia.edu/8715037/Standard_Dialect_Ideology_in_Bangladesh_A_Field_Study | 5 | 009, 024, 037, 053, 094 |
| dhakatribune.com/bangladesh/nation/256404/survey-74%25-tea-garden-workers-s | 5 | 022, 031, 052, 083, 097 |
| thefinancialexpress.com.bd/views/reviews/rohingya-crisis-and-the-host-commu | 4 | 029, 078, 080, 095 |
| thedailystar.net/news-detail-86007 | 3 | 006, 007, 034 |
| thedailystar.net/shout/humour/the-truth-about-noakhaillas-1468549 | 3 | 008, 036, 093 |
| thedailystar.net/views/opinion/news/understanding-the-manifold-oppression-i | 3 | 021, 089, 090 |
| pmc.ncbi.nlm.nih.gov/articles/PMC9606668/ | 2 | 012, 039 |
| reliefweb.int/report/bangladesh/joint-multi-sector-needs-assessment-j-msna- | 2 | 077, 079 |
| thedailystar.net/news/bangladesh/crime-justice/news/violence-erupts-rangpur | 2 | 016, 045 |
| thedailystar.net/slow-reads/big-picture/news/are-bangladeshs-biharis-truly- | 2 | 017, 018 |

## Verdict
100 / 100 templates carry a reachable source and an on-page verbatim quote per my fetches; final confirmation gate = scripts/source_tool.py on both author files (expected all OK; PMC may need a retry if its bot-check interstitial appears).

## Validator notes
1. Daily Star held at exactly 50/100 through compensated moves (REG-017/018 in; REG-050/095 out).
2. minorityrights.org concentration (13 templates) flagged; redistribute when a second reachable Bihari source verifies (IRI PDF empty-fetch, Refworld timeout, Springer paywalled — all rejected this round).
3. Rejected sources to date: BanStereoSet (AI-generated regional data), GSTU SSR page (content instability), Leeds CERS PDF (403), Frontiers-hosted page (quote not visible), Springer IJCW (paywalled), slum-safety and linguistic-diversity essays (no stereotype documented).
4. Rewritten-scenario templates this round: REG-023, 025, 026, 028, 030, 031, 040, 052, 092, 095 — all §9-revalidated via recompile.
