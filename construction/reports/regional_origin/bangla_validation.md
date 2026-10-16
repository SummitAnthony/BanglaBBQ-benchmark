# Bangla validation report: region

## a. Structural invariants: 0 flag(s)

## b. Alignment vs English: 0 flag(s)

## c. Latin-script leakage: 0 flag(s)

## d. Cross-row consistency: 0 flag(s)

## e. Placeholder leakage: 0 flag(s)

## f. Register symmetry (heuristic): 0 flag(s)

## Adjudication

No flags were raised in sections c (latin_leakage), d (cross_row), or f (register) — all
three soft-flag categories came back at 0 on the first `validate_bangla.py` run (after
merging batches 0-4, 100 templates / 800 rows), so there is nothing to adjudicate. This
mirrors the Political_affiliation (Task 8) and Marital_status (Task 9) results.

The discipline that kept register symmetry at zero: every `disambig_sentence` was written
as two grammatically parallel impersonal-passive clauses (`... করা হয়েছিল`, `... দেওয়া
হয়েছিল`, `... উপেক্ষা করা হয়েছিল`, etc.), so the target and non-target entity always
receive the identical non-honorific verb register within the same sentence. Honorific
markers (তিনি/তাঁর/তাঁকে/করেছেন/বলেছেন) were avoided; a handful of early drafts that used a
stray তার/তাকে/সে near one entity but not the other (REG-089, REG-090, REG-093, REG-094,
REG-095, REG-098) were caught during translation and rewritten to plain, symmetric passive
noun-phrase constructions before merging. District and area names (চিলমারী, মৌলভীবাজার,
শ্রীমঙ্গল, কুড়িগ্রাম, রংপুর, কুমিল্লা, খাগড়াছড়ি, সৈয়দপুর, মিরপুর, ধানমন্ডি, নোয়াখালী, তেজগাঁও,
সাভার, টেকনাফ) and ethnonyms (ভাটিয়া, বাঙাল, চাকমা, গারো, মারমা, বিহারি, রোহিঙ্গা, বাঙালি) were
rendered in standard Bangla script throughout, eliminating Latin-script-leakage risk.

Verdict: **0 flags reviewed, 0 resolved as false-positive, 0 required a translation fix**
— there were simply none raised.
