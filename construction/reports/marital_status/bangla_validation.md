# Bangla validation report: marital

## a. Structural invariants: 0 flag(s)

## b. Alignment vs English: 0 flag(s)

## c. Latin-script leakage: 0 flag(s)

## d. Cross-row consistency: 0 flag(s)

## e. Placeholder leakage: 0 flag(s)

## f. Register symmetry (heuristic): 0 flag(s)

## Adjudication

No flags were raised in sections c (latin_leakage), d (cross_row), or f (register) — all
three soft-flag categories came back at 0 on the first `validate_bangla.py` run, so there
is nothing to adjudicate. This mirrors the Political_affiliation (Task 8) result.

The translation discipline that kept register symmetry at zero: every `disambig_sentence`
was written as two grammatically parallel impersonal-passive clauses built on `-কে ...
করা হয়েছিল` / `-কে ... দেওয়া হয়েছিল` style constructions, so the target and non-target
entity always receive the identical non-honorific verb register within the same sentence.
Honorific markers (তিনি/তাঁর/তাঁকে/ছিলেন/হয়েছেন/করেছেন/বলেছেন) were deliberately avoided
throughout; several early drafts that used a stray তার/তাকে/তিনি/ছিলেন near one entity but
not the other (e.g. MAR-004, MAR-107, MAR-303, MAR-307, MAR-310, MAR-403, MAR-412, MAR-507,
MAR-511) were caught during translation and rewritten to plain, symmetric passive
constructions before merging. Party/relationship terms specific to this category (মোহরানা
for mahr/denmohor, ইদ্দত for iddat, একবিবাহে থাকা নারী for "woman in a monogamous
marriage", সতীন/দ্বিতীয় স্ত্রী for co-wife/second wife, পরিত্যক্তা নারী for "deserted
woman") were rendered in Bangla script throughout, eliminating Latin-script-leakage risk
since the check only flags Latin letters not on its allowlist.

Verdict: **0 flags reviewed, 0 resolved as false-positive, 0 required a translation fix**
— there were simply none raised.
