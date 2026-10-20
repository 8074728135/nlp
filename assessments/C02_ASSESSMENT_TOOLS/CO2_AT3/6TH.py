def parser_original(word):
    if word.endswith("s"):
        return word[:-2], "Plural Noun"
    else:
        return word, "Singular"

print("ORIGINAL PARSER")

for w in ["cars", "boxes", "cities", "children"]:
    print(" ", w, "->", parser_original(w))

LEXICON = {
    "car", "box", "city", "child", "bus", "class", "glass",
    "wolf", "knife", "man", "woman", "mouse", "foot", "dog",
    "church", "wish", "boy", "lady", "person"
}

IRREGULAR = {
    "children": "child",
    "men": "man",
    "women": "woman",
    "mice": "mouse",
    "feet": "foot",
    "people": "person"
}

RULES = [
    ("ies", "y", "-ies -> -y"),
    ("ves", "f", "-ves -> -f"),
    ("ves", "fe", "-ves -> -fe"),
    ("es", "", "-es"),
    ("s", "", "regular -s")
]

def parser(word):
    if word in IRREGULAR:
        return IRREGULAR[word], "Plural Noun (irregular)"

    if word in LEXICON:
        return word, "Singular"

    for ending, repl, name in RULES:
        if word.endswith(ending):
            root = word[:-len(ending)] + repl

            if root in LEXICON:
                return root, f"Plural Noun ({name})"

    return word, "Singular (unknown word)"

print("\nCORRECTED PARSER")

for w in [
    "cars", "boxes", "cities", "children", "buses",
    "wolves", "knives", "glasses", "class", "mice",
    "men", "churches"
]:
    print(f"{w:<9} -> {parser(w)}")