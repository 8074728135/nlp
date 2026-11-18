import re
import textwrap
from collections import defaultdict
from nltk.stem import PorterStemmer

ps = PorterStemmer()

reports = [
    "The infection spread quickly. Infected patients developed infectious symptoms.",
    "Doctors infect no one when infectious agents are contained; infections declined.",
    "General treatment of the disease needs careful generation of new antibiotics.",
    "The study of operations in generating vaccines was operative in the general hospital.",
]

STOP = {
    "the", "of", "in", "was", "are", "no", "one",
    "when", "new", "needs", "and", "were"
}

tokens = [
    w for r in reports
    for w in re.findall(r"[a-z]+", r.lower())
    if w not in STOP
]

vocab = sorted(set(tokens))
stems = {w: ps.stem(w) for w in vocab}

print("PORTER STEMS")
print(textwrap.fill(
    ", ".join(f"{w} -> {s}" for w, s in stems.items()), 88
))

ROOT = {
    "infect": "infect",
    "infection": "infect",
    "infections": "infect",
    "infected": "infect",
    "infectious": "infect",
    "general": "general",
    "generation": "generate",
    "generating": "generate",
    "operations": "operate",
    "operative": "operate"
}

by_root = defaultdict(set)
by_stem = defaultdict(set)

for w, r in ROOT.items():
    by_root[r].add(stems[w])
    by_stem[stems[w]].add(r)

print("\nERROR TYPE A - related words split into different stems")
for r, s in by_root.items():
    if len(s) > 1:
        print(f"root '{r}' -> stems {sorted(s)}")

print("\nERROR TYPE B - unrelated words merged into one stem")
for s, r in by_stem.items():
    if len(r) > 1:
        words = [w for w in ROOT if stems[w] == s]
        print(f"stem '{s}' <- {words} (roots {sorted(r)})")

BASE = {
    "infect", "infection", "infectious", "general", "generation",
    "generate", "operation", "operative", "operate", "patient", "symptom"
}

def inflectional_lemma(word):
    """Remove inflectional endings while keeping derivational forms."""
    if word in BASE:
        return word

    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            for cand in (stem, stem + "e"):
                if cand in BASE:
                    return cand

    return word

print("\nINFLECTION-ONLY NORMALIZATION")
for w in [
    "infect", "infection", "infections", "infected", "infectious",
    "general", "generation", "generating", "operations", "operative"
]:
    print(
        f"{w:<12} Porter: {stems[w]:<8} "
        f"Inflectional lemma: {inflectional_lemma(w):<11} "
        f"Root: {ROOT[w]}"
    )