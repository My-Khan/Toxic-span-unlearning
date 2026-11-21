"""Rebuild the derived data used in the paper from the raw ToxicSpans files.

Steps (Appendix A and C of the Supplementary Material):
  1. majority-vote spans: a character is toxic if more than half of the comment's
     raters marked it; span ends beyond the text are clipped; the one comment with
     357 annotation rows is removed (16,099 comments remain);
  2. split: numpy.random.RandomState(0).permutation over the comments in file order,
     first 80% train, next int(0.1 N) dev, the rest test (12,879 / 1,609 / 1,611);
  3. the 200 development comments used for checks: the first 200 dev comments
     with at least one span, in split order;
  4. lexicon: lower-cased alphabetic words in training comments with spans that lie
     inside a majority span (at least half of their characters covered) at least
     five times, with precision >= 0.5 (120 words);
  5. optional (--detoxify): benign sets, i.e. comments without a span that the
     Detoxify "original" checkpoint scores below 0.05 (703 train, 95 test).

    python scripts/build_derived_data.py                 # steps 1-4, written to data/rebuilt/
    python scripts/build_derived_data.py --detoxify      # also step 5 (needs detoxify)
    python scripts/verify_derived_data.py                # compare with data/derived/
"""
import argparse
import json
import re
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

WORD = re.compile(r"\b[a-z]+\b")


def majority_spans(raw: str):
    comments = pd.read_csv(f"{raw}/comments.csv")
    ann = pd.read_csv(f"{raw}/annotations.csv")
    spans = pd.read_csv(f"{raw}/spans.csv")
    text = dict(zip(comments.comment_id, comments.comment_text.astype(str)))
    n_raters = ann.groupby("comment_id").size()
    removed = set(n_raters[n_raters == 357].index)
    ann2c = dict(zip(ann.annotation, ann.comment_id))
    rater_chars = defaultdict(set)
    for a, st, en in zip(spans.annotation, spans.start, spans.end):
        en = min(en, len(text[ann2c[a]]))
        rater_chars[a].update(range(st, en))
    votes = defaultdict(Counter)
    for a, cid in zip(ann.annotation, ann.comment_id):
        votes[cid].update(rater_chars.get(a, ()))
    kept = [cid for cid in comments.comment_id if cid not in removed]
    chars = {cid: sorted(ch for ch, v in votes[cid].items() if 2 * v > n_raters[cid]) for cid in kept}
    return kept, chars, text, n_raters


def to_ranges(chars):
    out = []
    for ch in chars:
        if out and ch == out[-1][1]:
            out[-1][1] = ch + 1
        else:
            out.append([ch, ch + 1])
    return out


def build_lexicon(train_ids, chars, text):
    inside, total = Counter(), Counter()
    for cid in train_ids:
        S = set(chars[cid])
        if not S:
            continue
        for m in WORD.finditer(text[cid].lower()):
            w, L = m.group(), m.end() - m.start()
            cov = sum(k in S for k in range(m.start(), m.end()))
            total[w] += 1
            inside[w] += 2 * cov >= L
    return sorted(w for w in inside if inside[w] >= 5 and inside[w] / total[w] >= 0.5)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--raw", default="data/raw")
    p.add_argument("--out", default="data/rebuilt", help="kept apart from the shipped data/derived")
    p.add_argument("--detoxify", action="store_true", help="also score benign candidates")
    args = p.parse_args()

    import os
    os.makedirs(args.out, exist_ok=True)
    kept, chars, text, n_raters = majority_spans(args.raw)
    ids = np.array(kept)
    n = len(ids)
    order = ids[np.random.RandomState(0).permutation(n)]
    n_tr, n_dv = int(0.8 * n), int(0.1 * n)
    split = {}
    for i, cid in enumerate(order):
        split[cid] = "train" if i < n_tr else ("dev" if i < n_tr + n_dv else "test")
    dev_eval = [c for c in order[n_tr:n_tr + n_dv] if chars[c]][:200]

    df = pd.DataFrame({
        "comment_id": order,
        "split": [split[c] for c in order],
        "n_raters": [int(n_raters[c]) for c in order],
        "has_span": [bool(chars[c]) for c in order],
        "majority_spans": [json.dumps(to_ranges(chars[c])) for c in order],
        "dev_eval_200": [c in set(dev_eval) for c in order],
    })

    if args.detoxify:
        from detoxify import Detoxify
        model = Detoxify("original")
        cand = df[~df.has_span].comment_id.tolist()
        scores = {}
        for b in range(0, len(cand), 64):
            batch = cand[b:b + 64]
            res = model.predict([text[c] for c in batch])["toxicity"]
            scores.update(zip(batch, res))
        df["detoxify_original_toxicity"] = df.comment_id.map(scores)
        benign = df.detoxify_original_toxicity < 0.05
        df["benign_anchor"] = benign & (df.split == "train")
        df["benign_test"] = benign & (df.split == "test")

    df.to_csv(f"{args.out}/comments_index.csv", index=False)
    lex = build_lexicon([c for c in order[:n_tr]], chars, text)
    with open(f"{args.out}/lexicon.txt", "w") as f:
        f.write("\n".join(lex) + "\n")
    print(f"comments {n}, with span {int(df.has_span.sum())}, lexicon {len(lex)} words")


if __name__ == "__main__":
    main()
