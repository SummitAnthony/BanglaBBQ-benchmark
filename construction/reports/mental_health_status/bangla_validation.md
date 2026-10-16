# Bangla validation report: mental_health

## a. Structural invariants: 0 flag(s)

## b. Alignment vs English: 0 flag(s)

## c. Latin-script leakage: 0 flag(s)

## d. Cross-row consistency: 0 flag(s)

## e. Placeholder leakage: 0 flag(s)

## f. Register symmetry (heuristic): 4 flag(s)
- {'id': 89, 'question_index': '12', 'issue': "mixed register classes near entities: ['mixed', 'plain']"}
- {'id': 91, 'question_index': '12', 'issue': "mixed register classes near entities: ['mixed', 'plain']"}
- {'id': 93, 'question_index': '12', 'issue': "mixed register classes near entities: ['mixed', 'plain']"}
- {'id': 95, 'question_index': '12', 'issue': "mixed register classes near entities: ['mixed', 'plain']"}

## Adjudication

All 4 flags are the same disambig_sentence (template MEN-201, question_index "12"),
flagged once per disambig row (both orderings x both polarities). Template MEN-201 was
authored/merged in an earlier batch (0/1), not batch 3.

Sentence: "বাকিদের পক্ষ থেকে বিষণ্নতায় আক্রান্ত নারীর কথায় বিরক্তি দেখানো হয়েছিল এবং তাঁর
দুঃখের কথা বলাকে শুধু নজর কাড়ার চেষ্টা বলে গণ্য করা হয়েছিল, অন্যদিকে মানসিক রোগ নেই এমন
নারীর কথা মনোযোগ দিয়ে শোনা হয়েছিল।"

**Verdict: false positive.** Both clauses use the identical grammatical register — impersonal
passive with "-হয়েছিল" ("দেখানো হয়েছিল", "গণ্য করা হয়েছিল", "শোনা হয়েছিল") — with no active-voice
or informal construction on either side. The target clause carries two coordinated passive
predicates (উপেক্ষা/বিরক্তি + গণ্য) while the non-target clause carries one ("শোনা হয়েছিল");
that predicate-count asymmetry is inherited directly from the English source, which is likewise
asymmetric ("The others rolled their eyes at the woman with depression and said she only talked
about her sadness to get attention, while they listened earnestly to the woman with no mental
illness." — two actions vs. one). The heuristic's "mixed" vs "plain" complexity classes reflect
this predicate-count difference, not a voice/formality mismatch. No re-translation needed; row
left as-is.
