import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from build_combined_v2 import build_combined

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "combined")


def test_build_combined_renumbers_sequentially(tmp_path):
    out_path = str(tmp_path / "out.jsonl")
    sources = [os.path.join(FIXTURE_DIR, "cat_a.jsonl"), os.path.join(FIXTURE_DIR, "cat_b.jsonl")]
    count = build_combined(sources, out_path)
    assert count == 3
    with open(out_path, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f]
    assert [r["id"] for r in rows] == [0, 1, 2]
    assert [r["example_id"] for r in rows] == [0, 1, 2]
    assert [r["category"] for r in rows] == ["A", "A", "B"]
    assert rows[2]["context"] == "b1"
