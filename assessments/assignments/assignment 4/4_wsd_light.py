"""CO4 Part II Task 4 - Word sense disambiguation for 'light' (POS first, then context clues)."""
import re
from collections import Counter

WINDOW, MARGIN = 5, 1
SENSES = {  # label: (POS, clue stems)
    "LIGHT_DEVICE":    ("NOUN", ["turn", "switch", "lamp", "bulb", "off"]),
    "ILLUMINATION":    ("NOUN", ["room", "more", "dark", "bright", "plant", "sun", "enough"]),
    "LOW_WEIGHT":      ("ADJ",  ["bag", "carry", "heavy", "box", "suitcase", "weigh"]),
    "NOT_HEAVY_FOOD":  ("ADJ",  ["meal", "food", "lunch", "dinner", "served", "diet", "calorie"]),
    "BRIGHT":          ("ADJ",  ["sunrise", "dawn", "morning", "sky"]),
}
ADJ_BEFORE = {"is", "was", "are", "were", "became", "become", "feels", "seems", "very", "so", "quite"}
FOOD_NOUNS = {"meal", "lunch", "dinner", "breakfast", "snack", "bag", "suitcase", "box"}

def tokenize(s): return re.findall(r"[a-z']+", s.lower())

def pos_of(toks, i):
    prev = toks[i - 1] if i else ""
    nxt = toks[i + 1] if i + 1 < len(toks) else ""
    if prev in ADJ_BEFORE or nxt in FOOD_NOUNS: return "ADJ"
    return "NOUN"

def disambiguate(sentence):
    toks = tokenize(sentence)
    i = toks.index("light")
    pos = pos_of(toks, i)
    window = toks[max(0, i - WINDOW): i] + toks[i + 1: i + 1 + WINDOW]
    scores = {s: sum(any(w.startswith(c) for w in window) for c in clues)
              for s, (p, clues) in SENSES.items() if p == pos}
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    best, bs = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0
    if bs == 0 or bs - second < MARGIN: return pos, "AMBIGUOUS", scores
    return pos, best, scores

TEST = [
    ("Turn on the light.", "LIGHT_DEVICE"),
    ("Please switch off the light before leaving.", "LIGHT_DEVICE"),
    ("The room needs more light.", "ILLUMINATION"),
    ("Plants need light and water to grow.", "ILLUMINATION"),
    ("This bag is light.", "LOW_WEIGHT"),
    ("The suitcase was light enough to carry.", "LOW_WEIGHT"),
    ("The light meal was served early.", "NOT_HEAVY_FOOD"),
    ("She ate a light lunch.", "NOT_HEAVY_FOOD"),
    ("The room became light after sunrise.", "BRIGHT"),
]

if __name__ == "__main__":
    ok = 0
    per = Counter(); tot = Counter()
    for sent, gold in TEST:
        pos, pred, sc = disambiguate(sent)
        ok += pred == gold; tot[gold] += 1; per[gold] += pred == gold
        print(f"{pos:4} {pred:15} gold={gold:15} {sent}")
    print(f"\nAccuracy = {ok}/{len(TEST)} = {100*ok/len(TEST):.1f}%")
    for s in tot: print(f"  {s:15} {per[s]}/{tot[s]}")
    print("\nFailure case: 'The meal was light' ->", disambiguate("The meal was light.")[1],
          "(could mean low-calorie, small, or easy to digest - a 3-sense model cannot separate these)")
