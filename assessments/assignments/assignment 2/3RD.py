# Q3: Morphology-based normalization for topic modeling

ROOTS = {"govern"}
SUFFIXES = {
    "ment": "Verb -> Noun (act/result of governing)",
    "ance": "Verb -> Noun (state/process of governing)",
}

def decompose(word):
    layers = []
    stem = word
    for s, effect in SUFFIXES.items():
        if stem.endswith(s) and stem[:-len(s)] in ROOTS:
            layers.append(("-" + s, effect))
            stem = stem[:-len(s)]
    return stem, layers

for w in ["govern", "government", "governance"]:
    root, layers = decompose(w)
    level = len(layers)
    affixes = ", ".join(a for a, _ in layers) if layers else "-"
    hierarchy = f"[{root}]" if level == 0 else f"[[{root}]V {layers[0][0]}]N"
    print(f"Original word           : {w}")
    print(f"Root form               : {root}")
    print(f"Affix(es)               : {affixes}")
    print(f"Derivational level      : {level}")
    print(f"Derivational hierarchy  : {hierarchy}")
    print(f"Normalized form         : {root}")
    print(f"Final output (topic)    : {root.upper()}")
    print("-" * 50)