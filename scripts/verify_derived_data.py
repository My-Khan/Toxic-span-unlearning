"""Print the dataset statistics of Table 1 from the shipped derived data, and compare
the shipped files with a rebuild in data/rebuilt/ if one exists.

    python scripts/verify_derived_data.py
"""
import json
import os

import numpy as np
import pandas as pd

RAW, SHIP, REBUILT = "data/raw", "data/derived", "data/rebuilt"

idx = pd.read_csv(f"{SHIP}/comments_index.csv")
text = dict(pd.read_csv(f"{RAW}/comments.csv")[["comment_id", "comment_text"]].astype({"comment_text": str}).values)

print(f"{'':28s}{'train':>8s}{'dev':>8s}{'test':>8s}")
rows = {"Comments": [], "With at least one span": [], "Median length (words)": [],
        "Toxic share of characters (%)": [], "Benign comments": []}
for s in ["train", "dev", "test"]:
    d = idx[idx.split == s]
    sp = d[d.has_span]
    rows["Comments"].append(len(d))
    rows["With at least one span"].append(len(sp))
    rows["Median length (words)"].append(np.median([len(text[c].split()) for c in d.comment_id]))
    share = [sum(e - b for b, e in json.loads(r)) / len(text[c]) for c, r in zip(sp.comment_id, sp.majority_spans)]
    rows["Toxic share of characters (%)"].append(round(100 * np.mean(share), 1))
    col = {"train": "benign_anchor", "test": "benign_test"}.get(s)
    rows["Benign comments"].append(int(d[col].sum()) if col and col in d else "-")
for k, v in rows.items():
    print(f"{k:28s}" + "".join(f"{x:>8}" for x in v))

expected = {"Comments": [12879, 1609, 1611], "With at least one span": [7754, 971, 935]}
for k, v in expected.items():
    assert rows[k] == v, f"{k}: {rows[k]} != {v}"
print("Table 1 counts reproduced.")

if os.path.exists(f"{REBUILT}/comments_index.csv"):
    re_ = pd.read_csv(f"{REBUILT}/comments_index.csv")
    cols = ["comment_id", "split", "has_span", "majority_spans", "dev_eval_200"]
    same = idx[cols].reset_index(drop=True).equals(re_[cols].reset_index(drop=True))
    print("rebuilt spans, split and dev set identical to shipped:", same)
    lex_a = open(f"{SHIP}/lexicon.txt").read().split()
    lex_b = open(f"{REBUILT}/lexicon.txt").read().split()
    print("rebuilt lexicon identical to shipped:", lex_a == lex_b, f"({len(lex_a)} words)")
