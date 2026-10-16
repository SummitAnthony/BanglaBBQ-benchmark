# BanglaBBQ — Educational_background: Validation Report

**Validator run:** 2026-07-07 · **Templates checked:** 100 (EDU-001..100, author_a/b/c.jsonl) · **Distinct source URLs:** 36 (all fetched once, all live)

**Verdicts: 95 PASS · 5 NEEDS-REVIEW · 0 FAIL**

Method: (1) all 36 distinct source URLs fetched live via workspace fetcher (Prothom Alo, Dhaka Tribune, TBS, Daily Star articles fetched directly; the two World Bank `documentdetail` pages render abstracts via JS, so quotes were verified against the World Bank Documents & Reports API `search.worldbank.org/api/v2/wds`, exactly as documented in author_a_notes.md — both landing pages also confirmed live). (2) Every `source_quote` compared against fetched page text after normalising whitespace/curly quotes/dashes. (3) Schema/logic checked mechanically in Python (18 fields, category, label pairs, answer construction, placeholders/empties). (4) Disambiguation direction, ambiguous-context leakage, and question polarity judged per template. (5) Dedup and cultural relevance judged across all 100.

Quote status legend: **QV** = QUOTE-VERIFIED (verbatim on fetched page); **QV-API** = QUOTE-VERIFIED via World Bank WDS API (landing page is a JS shell). No PAGE-UNFETCHABLE or QUOTE-NOT-FOUND cases.

## Summary table

| template_id | verdict | quote status | relevance | cultural (1-3) | notes |
|---|---|---|---|---|---|
| EDU-001 | PASS | QV | strong | 3 | near-dup of EDU-003 (same facet, Dhaka office hiring, both male) — keep one eye on pair at compile |
| EDU-002 | PASS | QV | strong | 3 | |
| EDU-003 | PASS | QV | strong | 3 | near-dup of EDU-001 |
| EDU-004 | PASS | QV | strong | 3 | |
| EDU-005 | PASS | QV | strong | 3 | Re-grounded away from World Bank during post-review re-grounding |
| EDU-006 | PASS | QV | strong | 3 | |
| EDU-007 | PASS | QV | strong | 2 | generic office scenario, BD-localised |
| EDU-008 | PASS | QV | strong | 3 | |
| EDU-009 | PASS | QV | strong | 2 | |
| EDU-010 | PASS | QV-API | strong | 2 | WB abstract verified via WDS API |
| EDU-011 | PASS | QV | partial | 2 | quote is adviser's call for tech-driven system, implies gap; not a direct tech-incompetence claim |
| EDU-012 | PASS | QV | partial | 3 | "time-befitting education" quote documents modern-skills-gap discourse |
| EDU-013 | PASS | QV | partial | 3 | remedial tech/English training for Qawmi teachers implies documented gap |
| EDU-014 | PASS | QV-API | strong | 3 | |
| EDU-015 | PASS | QV | strong | 3 | Re-grounded away from World Bank during post-review re-grounding |
| EDU-016 | PASS | QV | partial | 3 | minister's "remove inequality" remark documents acknowledged stream gap |
| EDU-017 | PASS | QV | strong | 3 | |
| EDU-018 | PASS | QV | strong | 3 | |
| EDU-019 | PASS | QV | strong | 3 | |
| EDU-020 | PASS | QV | strong | 3 | |
| EDU-021 | PASS | QV | strong | 3 | official denial attests live militancy trope (attestation-style grounding) |
| EDU-022 | PASS | QV | strong | 3 | |
| EDU-023 | PASS | QV | strong | 3 | source documents "breaking the misinterpretation" — attests cultural-exclusion trope |
| EDU-024 | PASS | QV | strong | 3 | |
| EDU-025 | PASS | QV | partial | 3 | "brought to mainstream" quote documents exclusion indirectly |
| EDU-026 | PASS | QV | partial | 3 | same quote as EDU-025 |
| EDU-027 | PASS | QV | strong | 3 | |
| EDU-028 | PASS | QV | strong | 3 | |
| EDU-029 | PASS | QV | strong | 3 | |
| EDU-030 | PASS | QV | strong | 3 | |
| EDU-031 | PASS | QV | strong | 2 | madrasa-board math fail-rate stat; generic till setting |
| EDU-032 | PASS | QV | strong | 2 | |
| EDU-033 | PASS | QV | partial | 2 | "failed to produce skilled human resources" → leadership unfitness is an inference |
| EDU-034 | PASS | QV | partial | 2 | |
| EDU-035 | PASS | QV | partial | 3 | mainstream-exclusion quote reused |
| EDU-036 | PASS | QV | strong | 3 | source explicitly says disconnected-from-roots idea "is still prevalent in society" (article itself rebuts it — attestation grounding) |
| EDU-037 | PASS | QV | strong | 3 | |
| EDU-038 | PASS | QV | partial | 3 | "protect national interests" regulation quote only indirectly supports weak-national-values stereotype |
| EDU-039 | PASS | QV | strong | 3 | source is PA admission-fair series (advertorial tone) — see credibility notes; near-dup of EDU-059 |
| EDU-040 | PASS | QV | strong | 3 | |
| EDU-041 | PASS | QV | partial | 3 | "privileged families" quote documents affluence, not fragility; near-dup of EDU-050 |
| EDU-042 | PASS | QV | strong | 3 | near-dup of EDU-052 (EM vs Bangla exam-language facet; genders differ) |
| EDU-043 | PASS | QV | partial | 3 | "colonial mindset" is about general perception, not Boishakh disdain specifically |
| EDU-044 | PASS | QV | strong | 3 | quote attests "concerns about the practice of Bangla" in EM schools |
| EDU-045 | PASS | QV | strong | 3 | |
| EDU-046 | PASS | QV | partial | 3 | "viewed as superior" documents perception; template makes target act superior |
| EDU-047 | PASS | QV | strong | 3 | |
| EDU-048 | PASS | QV | strong | 3 | |
| EDU-049 | PASS | QV | strong | 3 | |
| EDU-050 | PASS | QV | partial | 3 | "parents spent a fortune" = affluence assumption only; student-written TBS Thoughts op-ed; near-dup of EDU-041 |
| EDU-051 | PASS | QV | strong | 3 | |
| EDU-052 | PASS | QV | strong | 3 | curly quotes/em dash in quote match source exactly; near-dup of EDU-042 |
| EDU-053 | PASS | QV | partial | 3 | quote (EM schools → inequality) supports class-disconnect reading indirectly; "(Hamid, 2016)" renders as citation link on page but text is verbatim |
| EDU-054 | PASS | QV | strong | 3 | |
| EDU-055 | PASS | QV | partial | 3 | same caveat as EDU-038 |
| EDU-056 | PASS | QV | strong | 3 | |
| EDU-057 | PASS | QV | strong | 3 | |
| EDU-058 | PASS | QV | strong | 3 | |
| EDU-059 | PASS | QV | strong | 3 | near-dup of EDU-039 (residents'-association elitism; genders differ) |
| EDU-060 | PASS | QV | strong | 3 | |
| EDU-061 | PASS | QV | strong | 3 | |
| EDU-062 | PASS | QV | strong | 2 | near-dup of EDU-075 (BM freezes speaking English at work; settings differ) |
| EDU-063 | PASS | QV | strong | 3 | |
| EDU-064 | PASS | QV | partial | 2 | rote-learning quote is about the exam system, not individuals' creativity |
| EDU-065 | PASS | QV | partial | 2 | British-curriculum promo piece (admission-fair series) credits EM with presentation skills — implies BM deficit |
| EDU-066 | PASS | QV | strong | 3 | |
| EDU-067 | PASS | QV | strong | 3 | |
| EDU-068 | PASS | QV | strong | 2 | examiner op-ed on national-curriculum HSC scripts |
| EDU-069 | PASS | QV | strong | 2 | |
| EDU-070 | PASS | QV | strong | 2 | |
| EDU-071 | PASS | QV | partial | 3 | "viewed as superior" quote; representational-unfitness is an inference |
| EDU-072 | PASS | QV | partial | 3 | "presentable" quote is about a debater's skill, not BM unpresentability |
| EDU-073 | PASS | QV | strong | 3 | |
| EDU-074 | PASS | QV | partial | 3 | creativity-vs-textbook quote from advertorial-style curriculum piece |
| EDU-075 | PASS | QV | strong | 3 | near-dup of EDU-062 |
| EDU-076 | PASS | QV | partial | 3 | PM quote critiques certificate-centric culture; documents credentialism domain, not the paperwork-incompetence claim |
| EDU-077 | PASS | QV | partial | 3 | quote (experience as competence proxy) is about IT graduates, not never-schooled workers — mechanism matches, group does not |
| EDU-078 | PASS | QV | partial | 3 | TVET-reform quote documents status/standards gap domain, not "diploma isn't real" stigma |
| EDU-079 | PASS | QV | partial | 3 | 4IR-curriculum quote is weakly tied to family vocational stigma; near-dup of EDU-100 |
| EDU-080 | PASS | QV | partial | 3 | course-duration quote weakly tied to "mistri can't supervise" stigma; "mistri" slur is authentic BD usage |
| EDU-081 | NEEDS-REVIEW | QV | off-topic | 3 | quote documents measles-driven debt/savings exhaustion among informal-worker families — not education-based financial distrust; author-flagged; re-ground with a sharper quote |
| EDU-082 | PASS | QV | partial | 3 | BRAC "documents they cannot read" quote grounds the non-reader/documents domain |
| EDU-083 | PASS | QV | partial | 3 | same quote; bKash mis-typing scenario is adjacent but in-domain |
| EDU-084 | PASS | QV | partial | 3 | quote links out-of-school poor communities to crime *vulnerability*; template asserts theft — direction of the association differs, keep flagged in notes |
| EDU-085 | PASS | QV | partial | 3 | same caveat as EDU-084 |
| EDU-086 | PASS | QV | partial | 3 | same caveat as EDU-084 |
| EDU-087 | PASS | QV | strong | 3 | op-ed directly ties education level to leadership/lawmaking ability |
| EDU-088 | PASS | QV | partial | 3 | "better educated don't want to enter politics" is adjacent to the unfit-president stigma |
| EDU-089 | PASS | QV | strong | 3 | |
| EDU-090 | PASS | QV | strong | 3 | low-literacy-household vulnerability quote fits parenting-blame scenario |
| EDU-091 | PASS | QV | strong | 3 | "hoes before pencils" article documents labour-vs-schooling directly |
| EDU-092 | NEEDS-REVIEW | QV | off-topic | 2 | quote documents outcome inequity for marginalized women, not the "low-education patients don't follow medical advice" stereotype; author-flagged |
| EDU-093 | NEEDS-REVIEW | QV | off-topic | 3 | same caveat as EDU-092; author-flagged |
| EDU-094 | NEEDS-REVIEW | QV | off-topic | 3 | quote ("education to delay child marriage") documents a different phenomenon than marriage-market rejection of low-educated grooms; validator-flagged (not author-flagged) |
| EDU-095 | PASS | QV | partial | 3 | low-literacy-household vulnerability quote loosely supports "can't raise educated children" trope |
| EDU-096 | PASS | QV | partial | 3 | education-as-privilege quote; testimony-dismissal is an extension |
| EDU-097 | PASS | QV | partial | 3 | counter-stereotype quote ("they can dream, too") attests the "only labour" trope |
| EDU-098 | NEEDS-REVIEW | QV | off-topic | 3 | quote documents the "One Teacher, One Tab" policy initiative, not a stereotype about low-educated adults and technology; author-flagged |
| EDU-099 | PASS | QV | partial | 3 | "documents they cannot read" deception quote grounds scam-vulnerability domain; mobile-banking scam is distinctly BD |
| EDU-100 | PASS | QV | partial | 3 | near-dup of EDU-079 (vocational stigma at family gathering; genders/settings differ) |

## Issues found

### 1. NEEDS-REVIEW — quotes document adjacent facts, not the encoded stereotype (5 templates)
All five quotes are verbatim-verified on live, credible pages; the problem is **relevance**, not fabrication. Excluded from `validated.jsonl` pending re-grounding:
- **EDU-081** (financial trust / cooperative treasurer): quote is about measles-induced household debt — no education/financial-trust link.
- **EDU-092, EDU-093** (healthcare interactions): quote documents that maternal-health harms fall hardest on marginalized women — outcome inequity, not the non-adherence/condescension stereotype. (Flagged in author_c_notes.md.)
- **EDU-094** (marriage proposals, low-educated groom): quote is about integrating education programmes to delay child marriage — different phenomenon from marriage-market stigma. Validator addition beyond the author's flags.
- **EDU-098** (technology use): quote documents a government literacy/tablet initiative, not a stereotype statement. (Flagged in author_c_notes.md.)

Recommendation: re-ground these five with sharper quotes once a search tool is available (author_c_notes.md documents that search engines were blocked during authoring); the scenarios themselves are well-formed and schema-clean.

### 2. Source liveness and credibility (36 distinct URLs)
- **All 36 URLs resolved live** on 2026-07-07. Outlets: Prothom Alo English (14), Dhaka Tribune (10), The Business Standard (6), The Daily Star (2), World Bank Documents & Reports (2), SpringerOpen peer-reviewed journals (2: *Language Testing in Asia* x2 papers on one domain + *Multilingual Education*). All are on the approved outlet list; **no blogs/forums/SEO pages**.
- **World Bank JS-rendering caveat (EDU-005/010/014/015):** the two `documentdetail` landing pages render "Loading…" shells; abstracts (containing the quotes verbatim, whitespace-normalized) were confirmed via the World Bank WDS API exactly as the author notes describe. Both landing pages themselves resolve with correct titles/metadata.
- **Advertorial caveat:** five Prothom Alo English pieces (EDU-036/039/042/044/045/047/051/052/056/057/058/059/065/074 sources: `dhyeorr39f`, `3s62co6hfr`, `vhjc3u5sxz`, `t50xz46qt6`, `3ggzw01ubj`) belong to an "English Medium School Admission Fair" content series with promotional framing (British Council spokespeople). They are published under Prothom Alo's masthead and are adequate for *documenting perceptions/stereotypes*, but they are weaker than reportage; several explicitly rebut the stereotype while attesting it "is still prevalent in society" (acceptable attestation-style grounding, same pattern as the home-minister militancy denial used by author A).
- **Opinion-piece grounding:** EDU-050 (TBS *Thoughts*, written by affected A-level candidates), EDU-062/049 (PA opinion by a British Council invigilator), EDU-068 (PA op-ed by an HSC examiner), EDU-087–089 (DT op-ed). Fine for stereotype attestation; noted for transparency.
- Minor: the TBS URL for EDU-038/055 contains a typo ("schoola") but is the canonical URL and resolves.

### 3. Schema & logic — clean
- 100/100 templates parse; IDs EDU-001..100 complete, no duplicates.
- 18 fields exactly, `category` correct, all four label pairs correct (madrasa/nonMadrasa ×35, englishMedium/nonEnglishMedium ×25, banglaMedium/nonBanglaMedium ×15, lowEducation/nonLowEducation ×25), `target_answer`/`nontarget_answer` = "The "+short in all rows, no `{{...}}`/TODO/empty strings.
- Disambiguation direction: in all 100, the disambig sentence assigns the negative outcome to the target (biased direction) and the positive to the nontarget — verified by reading each.
- Ambiguous contexts do not leak the disambiguating outcome. (In the criminal-suspicion items EDU-084–086 the *incident* appears in the ambiguous context but attribution — the actual disambiguator — does not; standard BBQ construction.)
- Negative/nonnegative questions are proper opposite-polarity pairs in all 100.
- Note (not an error): a few templates (EDU-001/003/004/005/006) introduce the pair as "one madrasa-educated and one university-educated" rather than repeating the full `target_short` string in the ambiguous context; referents remain unambiguous.

### 4. Near-duplicate pairs (flagged, none are true duplicates — all remain PASS)
Same subcategory + same stereotype facet + similar setting; most differ by gender per BBQ family design, so they are flagged for compile-time awareness rather than failed:
- EDU-001 / EDU-003 (madrasa man rejected at Dhaka office hiring for lack of skill)
- EDU-039 / EDU-059 (EM resident acts elitist at a Dhaka residents'-association)
- EDU-041 / EDU-050 (EM "pampered rich kid" quits hardship volunteering/fieldwork)
- EDU-042 / EDU-052 (EM student defeated by Bangla-language admission exam)
- EDU-062 / EDU-075 (BM man freezes in spoken-English work situation)
- EDU-079 / EDU-100 (vocational-track relative shamed at family gathering)

### 5. Cultural relevance
No template scored below 2. 82 templates rated 3 (distinctly Bangladeshi settings/stereotypes: Qawmi/Alia madrasas, EM-vs-BM medium divide, Ekushey, Pohela Boishakh, Lalon/Baul, ghotok, gaye holud, salish, bKash, char villages, RMG factories, union parishad, DU/BUET admission). 18 rated 2 (generic office/tech scenarios that are BD-localised only by venue; the education-stream axis itself is still Bangladesh-specific).

## Final tally

| Verdict | Count | Template IDs |
|---|---|---|
| PASS | 95 | all except below |
| NEEDS-REVIEW | 5 | EDU-081, EDU-092, EDU-093, EDU-094, EDU-098 |
| FAIL | 0 | — |

- Quote verification: 100/100 QUOTE-VERIFIED (96 directly on page, 4 via World Bank WDS API per author-notes route). 0 QUOTE-NOT-FOUND, 0 PAGE-UNFETCHABLE.
- `templates/validated.jsonl` written with the 95 PASS templates, verbatim lines from the author files, in EDU-001..100 order (verbatim identity mechanically re-verified).

---

## Post-review re-grounding (2026-07-11)

External review found 5 quotes not verbatim-fetchable (EDU-005/010/014/015: World Bank JS-shell landing pages; EDU-053: inline citation link). Fixes applied and re-verified against live fetches:

- **EDU-005, EDU-014, EDU-015** → re-grounded on Prothom Alo English, "'75pc madrasa students jobless'" (Barkat book-launch report); three distinct verbatim sentences copied from the fetched page.
- **EDU-010** → source repointed to the World Bank plain-text rendition (`.../text/380120BD0Schoo1chievement001PUBLIC1.txt`); quote replaced with the document's own wording ("However, we document significant learning deficit…") — the previous quote was the WDS API's third-person abstract rewrite.
- **EDU-053** → quote trimmed to end before the "(Hamid, 2016)" citation, which renders as a hyperlink and broke plain-text matching. Same source, same sentence.

Final file recompiled; all §9 invariants re-verified.
