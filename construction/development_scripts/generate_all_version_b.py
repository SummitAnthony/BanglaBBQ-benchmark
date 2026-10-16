# NOTE (release): kept for provenance. Written for the development repository; paths in it refer to
# that layout (output/, templates/, scripts/), which is not part of this release.
"""
Generate version b (counter-stereotypical) compiled records for all 5 NA categories
using disambig_counterbiased sentences from templates_with_counter.jsonl.

For each category:
  - Loads version a compiled JSONL
  - Replaces disambig sentence with counter sentence
  - Flips labels on disambig rows (neg -> nontarget_idx, nonneg -> target_idx)
  - Keeps ambig rows identical (label=Unknown unchanged)
  - Resets example_id sequentially within each file

Output files (in output/):
  banglabbq_marital_eng_vb.jsonl          (800 records)
  banglabbq_age_politics_eng_vb.jsonl     (800 records)
  banglabbq_educational_eng_vb.jsonl      (760 records)
  banglabbq_region_eng_vb.jsonl           (800 records)
  banglabbq_mental_health_eng_vb.jsonl    (568 records)
"""
import json, copy, sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

# ── Load templates ────────────────────────────────────────────────────────────
with open('kaggle_eval/dataset_upload/templates_with_counter.jsonl', encoding='utf-8') as f:
    all_templates = [json.loads(l) for l in f]

# ── Category config ───────────────────────────────────────────────────────────
CATEGORIES = {
    'Marital_status': {
        'va_file': 'output/banglabbq_marital_eng.jsonl',
        'vb_file': 'output/banglabbq_marital_eng_vb.jsonl',
    },
    'Age_political_perception': {
        'va_file': 'output/banglabbq_age_politics_eng.jsonl',
        'vb_file': 'output/banglabbq_age_politics_eng_vb.jsonl',
    },
    'Educational_background': {
        'va_file': 'educational_background/output/banglabbq_educational_eng.jsonl',
        'vb_file': 'output/banglabbq_educational_eng_vb.jsonl',
    },
    'Regional_origin': {
        'va_file': 'regional bias outputs/banglabbq_region_eng.jsonl',
        'vb_file': 'output/banglabbq_region_eng_vb.jsonl',
    },
    'Mental_health_status': {
        'va_file': 'output/banglabbq_mental_health_eng.jsonl',
        'vb_file': 'output/banglabbq_mental_health_eng_vb.jsonl',
    },
}

def load_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(l) for l in f]

# ── Process each category ─────────────────────────────────────────────────────
for category, cfg in CATEGORIES.items():
    print(f'\n{"="*60}')
    print(f'Processing: {category}')

    # Templates for this category (in order = question_index 1, 2, 3, ...)
    cat_templates = [t for t in all_templates if t['category'] == category]
    # Build question_index -> template mapping
    idx_to_tmpl = {str(i + 1): t for i, t in enumerate(cat_templates)}

    # Load version a records
    va_records = load_jsonl(cfg['va_file'])
    print(f'  Loaded {len(va_records)} version a records')

    vb_records = []
    skipped = 0
    new_id = 0

    for row in va_records:
        rec = copy.deepcopy(row)
        q_idx = rec['question_index']
        tmpl = idx_to_tmpl.get(q_idx)

        if tmpl is None:
            print(f'  WARNING: no template for question_index {q_idx}')
            skipped += 1
            continue

        counter_sent = tmpl['en'].get('disambig_counterbiased', '')
        if not counter_sent:
            print(f'  WARNING: no counter sentence for {tmpl["template_id"]}')
            skipped += 1
            continue

        rec['additional_metadata']['version'] = 'b'

        if rec['context_condition'] == 'ambig':
            pass  # identical to version a — label stays Unknown

        else:
            # Replace disambig sentence
            ambig_ctx = tmpl['en']['ambiguous_context']
            rec['context'] = ambig_ctx + ' ' + counter_sent

            # Find target and nontarget answer indices
            target_ans    = tmpl['en']['target_answer']
            nontarget_ans = tmpl['en']['nontarget_answer']

            target_idx    = None
            nontarget_idx = None
            for idx in [0, 1, 2]:
                val = rec[f'ans{idx}']
                if val == target_ans:
                    target_idx = idx
                elif val == nontarget_ans:
                    nontarget_idx = idx

            if target_idx is None or nontarget_idx is None:
                print(f'  WARNING: cannot find ans indices for {tmpl["template_id"]} eid={rec["example_id"]}')
                skipped += 1
                continue

            # Flip label: nontarget gets bad outcome in version b
            if rec['question_polarity'] == 'neg':
                rec['label'] = nontarget_idx
            else:
                rec['label'] = target_idx

        rec['id'] = new_id
        rec['example_id'] = new_id
        new_id += 1
        vb_records.append(rec)

    # Write output
    with open(cfg['vb_file'], 'w', encoding='utf-8') as f:
        for rec in vb_records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')

    print(f'  Written: {len(vb_records)} records -> {cfg["vb_file"]}')
    if skipped:
        print(f'  Skipped: {skipped}')

    # Quick sanity
    disambig = [r for r in vb_records if r['context_condition'] == 'disambig']
    ambig    = [r for r in vb_records if r['context_condition'] == 'ambig']
    from collections import Counter
    lc = Counter(r['label'] for r in vb_records)
    print(f'  ambig={len(ambig)}, disambig={len(disambig)}, labels={dict(lc)}')

    # Show 2 sample disambig+neg
    for r in [x for x in disambig if x['question_polarity'] == 'neg'][:2]:
        lbl = r['label']
        q = r['question_index']
        t = idx_to_tmpl[q]
        print(f'    {t["template_id"]} label={lbl} -> {r[f"ans{lbl}"]}  (nontarget={t["en"]["nontarget_answer"]})')

print('\nDone. All 5 version b files written.')
