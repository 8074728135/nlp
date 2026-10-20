LEX = {
    "happy", "believe", "run", "order", "smart", "phone",
    "read", "play", "agree", "city", "walk", "car"
}

PREFIXES = ["un", "re", "dis"]

SUFFIXES = {
    "ness": "ness",
    "ment": "ment",
    "able": "able",
    "ing": "ing",
    "est": "est",
    "ies": "s",
    "ed": "ed",
    "er": "er",
    "es": "s",
    "s": "s"
}

def fmt(prefixes, root, suffixes):
    return " + ".join(
        [p + "-" for p in prefixes] +
        [root] +
        ["-" + s for s in suffixes]
    )

def naive_parse(word):
    if word in LEX:
        return word

    for suf, label in SUFFIXES.items():
        if word.endswith(suf) and word[:-len(suf)] in LEX:
            return fmt([], word[:-len(suf)], [label])

    for p in PREFIXES:
        if word.startswith(p) and word[len(p):] in LEX:
            return fmt([p], word[len(p):], [])

    return "FAIL"

def candidates(base, suf):
    out = [base, base + "e"]

    if len(base) > 2 and base[-1] == base[-2]:
        out.append(base[:-1])

    if base.endswith("i"):
        out.append(base[:-1] + "y")

    if suf == "ies":
        out.append(base + "y")

    return out

def root_with_prefixes(w):
    if w in LEX:
        return [], w

    for i in range(2, len(w) - 1):
        if w[:i] in LEX and w[i:] in LEX:
            return [], w[:i] + " + " + w[i:]

    for p in PREFIXES:
        if w.startswith(p):
            r = root_with_prefixes(w[len(p):])
            if r:
                return [p] + r[0], r[1]

    return None

def fst_parse(word, suffixes=()):
    r = root_with_prefixes(word)

    if r:
        return fmt(r[0], r[1], suffixes)

    for suf in sorted(SUFFIXES, key=len, reverse=True):
        if word.endswith(suf):
            for c in candidates(word[:-len(suf)], suf):
                if len(c) > 1:
                    res = fst_parse(
                        c,
                        (SUFFIXES[suf],) + suffixes
                    )
                    if res:
                        return res

    return None

GOLD = {
    "happiest": "happy + -est",
    "unbelievable": "un- + believe + -able",
    "running": "run + -ing",
    "reordering": "re- + order + -ing",
    "smartphones": "smart + phone + -s",
    "unreadable": "un- + read + -able",
    "replayed": "re- + play + -ed",
    "players": "play + -er + -s",
    "happier": "happy + -er",
    "unhappiness": "un- + happy + -ness",
    "disagreement": "dis- + agree + -ment",
    "cities": "city + -s",
    "walked": "walk + -ed",
    "cars": "car + -s"
}

ok_before = 0
ok_after = 0

for w, gold in GOLD.items():
    b = naive_parse(w)
    a = fst_parse(w) or "FAIL"

    ok_before += b == gold
    ok_after += a == gold

    print(f"{w:<13} before: {b:<26} after: {a}")

n = len(GOLD)

print(
    f"\nAccuracy before correction: "
    f"{ok_before}/{n} = {100 * ok_before / n:.1f}%"
)
print(
    f"Accuracy after correction: "
    f"{ok_after}/{n} = {100 * ok_after / n:.1f}%"
)