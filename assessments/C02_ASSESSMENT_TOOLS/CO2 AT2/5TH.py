# Q5: Inflectional normalization for search optimization

ROOTS = {"create"}

RULES = [
    ("ing", "e", "Present participle (progressive aspect)"),
    ("s", "", "Third-person singular, present tense"),
]

def normalize(word):
    if word in ROOTS:
        return word, "-", "Base form (present tense)"
    for suffix, restore, category in RULES:
        if word.endswith(suffix):
            root = word[:-len(suffix)] + restore
            if root in ROOTS:
                return root, "-" + suffix, category
    return word, "-", "Unknown"

for w in ["create", "creates", "creating"]:
    root, suffix, category = normalize(w)
    print(f"Original word        : {w}")
    print(f"Suffix               : {suffix}")
    print(f"Grammatical category : {category}")
    print(f"Extracted root       : {root}")
    print(f"Normalized base form : {root}")
    print(f"Final representation : {root.upper()} (type: Inflectional)")
    print("-" * 50)