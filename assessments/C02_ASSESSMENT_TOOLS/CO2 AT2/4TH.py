# Q4: Morphological parsing of activate / activation / reactivation

KNOWN = {"act", "active", "activate"}
PREFIXES = {"re": ("re-", "Verb -> Verb", "again / repetition")}

SUFFIXES = [
    ("ation", "ate", "-ion", "Verb -> Noun", "act or result of the action"),
    ("ate", "e", "-ate", "Adjective -> Verb", "to make / cause to be"),
    ("ive", "", "-ive", "Verb -> Adjective", "having the quality of"),
]

def parse(word):
    steps = []
    while word != "act":
        for p, (label, change, meaning) in PREFIXES.items():
            if word.startswith(p) and word[len(p):] in KNOWN:
                steps.append((word[len(p):], word, label, change, meaning))
                word = word[len(p):]
                break
        else:
            for s, restore, affix, change, meaning in SUFFIXES:
                if word.endswith(s):
                    base = word[:-len(s)] + restore
                    steps.append((base, word, affix, change, meaning))
                    word = base
                    break
            else:
                break
    return word, steps[::-1]

for w in ["activate", "activation", "reactivation"]:
    root, steps = parse(w)
    prefix = next((s[2] for s in steps if s[2] == "re-"), "-")
    suffix = [s[2] for s in steps if s[2] != "re-"]
    chain = " -> ".join([root] + [s[1] for s in steps])
    parsed = " + ".join(([prefix] if prefix != "-" else []) + [root] + suffix)

    print(f"Original word          : {w}")
    print(f"Prefix                 : {prefix}")
    print(f"Root word              : {root}")
    print(f"Suffix                 : {', '.join(suffix)}")
    print(f"Derivational sequence  : {chain}")
    for base, result, affix, change, meaning in steps:
        print(f" {base:<10} + {affix:<5} = {result:<13} [{change}; {meaning}]")
    print("Normalized base form  : activate")
    print(f"Final parsed form      : {parsed}")
    print("-" * 60)