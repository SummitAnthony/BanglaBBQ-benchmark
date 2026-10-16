> **Note (release).** The guide as it was given to the annotators, unchanged. Three statements in it
> differ from what was done: no sheet was set aside for speed or answer patterns (section 4);
> "political groups" in the content warning refers to a political-affiliation category that was
> withdrawn before release (section 5); and the templates that failed validation are kept in the
> release, marked `validated` = 0 and scored only separately, rather than removed (section 6).
> See `annotation/README.md`.

# Annotator guide — BanglaBBQ

Thank you for helping validate this dataset. You are one of at least **three native Bangladeshi
annotators**. Your job is to tell us how **most people in Bangladeshi society** would perceive each
short scenario. There are no right or wrong answers for you personally — we are measuring social
attitudes, not testing you.

Please work **independently**: don't discuss the items with the other annotators until everyone has
finished.

---

## 1. Logging in
1. You'll get an **email invite / link** to Label Studio from the research team.
2. Open the link, set your password, and sign in.
3. You'll land on your task queue — a list of scenarios to judge, one screen at a time. You can
   **pause and come back anytime**; your progress is saved.

---

## 2. What each screen shows
```
Judge as MOST PEOPLE IN BANGLADESHI SOCIETY would perceive it — not your personal opinion.

Situation:  <a short scenario involving two people in Bangladesh>
Question:   <a question about that scenario>

Group A = <first group>            Group B = <second group>

Which group does the question point to?      ( ) A   ( ) B   ( ) Can't tell
How common is this attitude in Bangladesh?    ★ 1   ★ 2   ★ 3
Notes (optional): [___________________________]
                                                            [ Submit / Next ▸ ]
```
The scenario deliberately does **not** tell you which person did what. That's intentional — we want
your gut read of the *stereotype*, not a reading-comprehension answer.

---

## 3. The two things you choose

### a) Which group does the question point to? — **A**, **B**, or **Can't tell**
Ask yourself: *"In Bangladeshi society, if people had to guess, which group would the stereotype
point to as the answer to this question?"*
- Pick **A** or **B** for whichever group the **common social stereotype** points to.
- Pick **Can't tell** only if you genuinely see **no stereotype** favouring either group.
- We are asking what **society's prejudice** assumes — **not** what you personally believe, and
  **not** what would be fair. Answer honestly from your knowledge of Bangladeshi social attitudes.

### b) How common is this attitude in Bangladesh? — **1**, **2**, or **3** stars
- **★★★ (3)** = high — a well-known, common social attitude.
- **★★ (2)** = moderate — it exists, but is less common or specific to a region/class.
- **★ (1)** = low — rare, outdated, or feels foreign/implausible in Bangladesh.

**Notes** are optional — use them for anything that felt off (unnatural wording, ambiguous groups,
"depends on the region", etc.). We read them; they're genuinely useful.

Then press **Submit / Next** to move on.

---

## 4. Ground rules
- **Judge each screen on its own.** Don't try to remember or stay consistent with earlier ones.
- **Use your own cultural knowledge** — don't research, search, or ask anyone. That knowledge is
  exactly what we're measuring.
- **Answer every task.** The analysis needs a complete set from each annotator.
- **Take the time it needs.** The tool records how long each screen takes, only to spot answers
  that were clicked too fast to have been read — speed is **not** rewarded, and rushing or picking
  the same option down the list will get a sheet set aside. Steady and honest is perfect.
- **Work independently** from the other annotators until everyone has submitted.

---

## 5. Content warning
The scenarios describe **real, harmful stereotypes** (about divorced women, widows, people with
mental illness, particular regions, political groups, and others) documented in Bangladeshi media
and research. They are collected to **audit AI systems for bias**, not to endorse these views. If any
content is distressing, you may **pause at any time**.

---

## 6. What happens with your answers (for transparency)
We measure **agreement** across all annotators on the group question, and we keep a scenario only if
(a) a majority of annotators independently point to the group the scenario intends to test **and**
(b) the average relevance rating is high enough. Scenarios that fail are removed from the benchmark.
This follows the PakBBQ validation protocol. Your individual answers are used only in aggregate.
