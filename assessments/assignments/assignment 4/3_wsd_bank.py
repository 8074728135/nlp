"""CO4 Part I Task 4 - Rule/context-based word sense disambiguation for 'bank'."""
import re
from collections import Counter, defaultdict

WINDOW = 5
THRESHOLD = 1      # minimum evidence score
MARGIN = 1         # winner must beat runner-up by this much, else AMBIGUOUS

CLUES = {
    "BANK-N-FINANCIAL": ["deposit", "cash", "money", "loan", "account", "teller", "withdr", "branch", "approv"],
    "BANK-N-RIVER-SIDE": ["river", "water", "shore", "sat", "stream", "fish", "mud", "reed"],
    "BANK-V-AIRCRAFT-TILT": ["pilot", "aircraft", "plane", "wing", "turn", "left", "right"],
}

def tokenize(s): return re.findall(r"[a-z']+", s.lower())

def pos_of(tok):
    return "VERB" if tok.endswith(("ed", "ing")) else "NOUN"

def disambiguate(sentence):
    toks = tokenize(sentence)
    idx = next((i for i, t in enumerate(toks) if t.startswith("bank")), None)
    if idx is None: return {"sense": "NO-TARGET", "pos": None, "conf": 0.0, "scores": {}}
    pos = pos_of(toks[idx])
    cands = [s for s in CLUES if s.split("-")[1] == ("V" if pos == "VERB" else "N")]
    window = toks[max(0, idx - WINDOW): idx] + toks[idx + 1: idx + 1 + WINDOW]
    scores = {s: sum(any(w.startswith(c) for w in window) for c in CLUES[s]) for s in cands}
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    best, bs = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0
    if bs < THRESHOLD or bs - second < MARGIN:
        return {"sense": "AMBIGUOUS", "pos": pos, "conf": 0.0, "scores": scores}
    return {"sense": best, "pos": pos, "conf": round(bs / (bs + second + 1), 2), "scores": scores}

TEST = [
    ("Nila deposited cash at the bank.", "BANK-N-FINANCIAL"),
    ("They sat on the bank of the river.", "BANK-N-RIVER-SIDE"),
    ("The pilot banked the aircraft to the left.", "BANK-V-AIRCRAFT-TILT"),
    ("The hikers rested on the bank after crossing the stream.", "BANK-N-RIVER-SIDE"),
    ("She opened an account at the bank to get a loan.", "BANK-N-FINANCIAL"),
    ("The fisherman stood on the muddy bank near the water.", "BANK-N-RIVER-SIDE"),
    ("The plane banked sharply to avoid the storm.", "BANK-V-AIRCRAFT-TILT"),
    ("The bank approved my loan application.", "BANK-N-FINANCIAL"),
    ("He withdrew money from the bank before it closed.", "BANK-N-FINANCIAL"),
    ("The bank was crowded.", "AMBIGUOUS"),
]

def evaluate(test):
    tp, fp, fn = Counter(), Counter(), Counter()
    correct = answered = 0
    for sent, gold in test:
        out = disambiguate(sent)
        pred = out["sense"]
        print(f"{pred:22} (gold {gold:22}) conf={out['conf']}  {sent}")
        if pred != "AMBIGUOUS": answered += 1
        if pred == gold: correct += 1; tp[gold] += 1
        else: fp[pred] += 1; fn[gold] += 1
    print(f"\nAccuracy = {correct}/{len(test)} = {100*correct/len(test):.1f}%   "
          f"(answered {answered}, abstained {len(test)-answered})")
    for s in sorted(set(g for _, g in test)):
        p = tp[s] / (tp[s] + fp[s]) if tp[s] + fp[s] else 0.0
        r = tp[s] / (tp[s] + fn[s]) if tp[s] + fn[s] else 0.0
        print(f"  {s:22} precision={p:.2f} recall={r:.2f}")

if __name__ == "__main__":
    evaluate(TEST)
