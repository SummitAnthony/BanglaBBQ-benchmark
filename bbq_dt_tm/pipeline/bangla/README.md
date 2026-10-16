# Bangla translation of the DT/TM files

`BanglaBBQ_BN/` holds the Bangla version of every file in `BanglaBBQ_ENG/`: same file names, same
rows in the same order, same fields. Only the context, question and answer strings are in Bangla:
`context`, `question`, `ans0`–`ans2` and their short forms in `answer_info` (`answer_info[ansN][0]`).
Everything else is copied unchanged from
the English row, including `label`, both ids, the `answer_info` group tags and
`additional_metadata`. The unknown option is `যথেষ্ট তথ্য নেই`, as in the NA Bangla file (`অজানা` suppressed Unknown answers; see `evaluation/unknown_wording/report.md`).

## How it was translated

The translation was done at the template level, as in KoBBQ and PakBBQ, not row by row:

1. `build_trace.py` reruns `build.sh`'s steps with a copy of the generator
   (`generate_bbq_trace.py`) that also records, for every block of four rows, which template it
   came from and what went into `{{NAME1}}`, `{{NAME2}}`, `{{WORD1}}` and `{{WORD2}}`. The rebuilt
   English files are identical to `BanglaBBQ_ENG/`.
2. `make_packets.py` collects the 224 distinct template rows (140 BBQ templates, with their a/b
   versions) and the ~450 slot fillers that the generator actually used → `packets/<Cat>.json`.
3. The templates and slot fillers were translated by an LLM, one category per pass, with the conventions that a
   native-Bangla-speaking author set for the Bangla of the newly authored categories (paper §3.5;
   `construction/README.md`, "Bangla"). That means direct sentence translation in formal, neutral,
   standard Bangladeshi Bangla, with no dictionary or small MT model. Slots are kept. The same register is
   used for both people in a template (both তিনি/তাঁর with -এন verbs, or both সে/তার). Nothing is
   in Latin script. The results are in `bn/<Cat>.json`. The 60 first names share one spelling
   list, `bn/first_names.json`.
4. `build_bangla.py` fills the Bangla templates with the Bangla fillers, following the trace, and
   writes `BanglaBBQ_BN/`. Answer order and labels come from the English rows. `{{SLOT:poss}}` in
   a Bangla template adds the genitive ending (র / ের / য়ের).

## Rebuilding

```
git clone https://github.com/nyu-mll/BBQ
python pipeline/bangla/build_trace.py BBQ/templates pipeline/bangla/build
python pipeline/bangla/build_bangla.py all --write          # -> BanglaBBQ_BN/
```

Run these commands from inside `bbq_dt_tm/`. They need Python 3 and pandas; `build_trace.py` calls the
pipeline scripts with the running Python, so no bash is needed (the English rebuild with `build.sh`,
`bbq_dt_tm/README.md`, needs bash: Linux or macOS, or on Windows WSL or Git Bash with `python3` on the
PATH). On Windows also set `PYTHONUTF8=1`. `build_bangla.py` stops if any hard check fails:
- a field changed
- an answer tag changed
- a slot was lost or left unfilled
- the two people's answers are the same string
- an ambiguous row's correct answer is not the Unknown option

It also reports soft flags: Latin text, `[NEEDS_REVIEW]`, and the register-symmetry heuristic from
`validate_bangla.py` of the development repository, which is not part of this release; it runs only
when the environment variable `BANGLABBQ_SCRIPTS` points at a folder that contains it.

## Checks on the delivered files (7 Oct 2026)

All 15,328 rows pass every hard check above, and the checks of the development repository's `validate_bangla.py`
for alignment with English, Latin leakage and placeholders: 0 flags each. The register heuristic
raises 390 soft flags, in Gender_identity (268), Physical_appearance (106) and Disability_status
(16). They were inspected during the translation run, and all are false positives: the heuristic counts substrings, so it
finds `ছিল` inside the honorific `ছিলেন`, `সে` inside `হিসেবে`, and `তিনি` inside `প্রতিনিধি`.

## Translation choices

Native Bangla speakers judged the translation acceptable (paper §5). The Bangla `bbq_dt_tm` results in
`evaluation/reports/dt_tm/` were obtained on this text. The main translation choices are:

- **Kinship terms are gendered in Bangla.** "grandparent" → নানা and "grandchild" → নাতি (both
  male). grandfather → দাদা, grandpa → দাদু, grandmother → দাদি, grandma → নানি. "elderly parent"
  → "বয়স্ক মা-বাবার একজন". "an uncle" → একজন মামা.
- **Register by age:** honorific for adults and plain for children and students, the same for both
  people in a template. In Age templates that pair an older adult with a child or teen, both get the
  plain register. This keeps the grammar symmetric, though the older person reads a little
  informally.
- **Transliterated loanwords:**
  - generation labels: বুমার, মিলেনিয়াল, জেন-জি
  - ট্রান্সজেন্ডার, পিটিএসডি
  - সেক্রেটারি rather than সচিব (in Bangladesh সচিব means a senior civil servant)
  - স্টেম, with a gloss
- **Word choices:** "teen" → কিশোর; "community center" → সামাজিক কেন্দ্র (in Bangladesh a
  "কমিউনিটি সেন্টার" is an event hall); "old geezer" → বুড়ো লোক.
- **Genitive suffixes on filled slots** come from a rule: র after a vowel sign, ের after a
  consonant, য়ের after a vowel letter. A few names may take a less common form
  (সুব্রতের/সুব্রতর).
