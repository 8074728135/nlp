"""CO5 A1 - Conservative pronoun / definite-description resolver with scoring, trace and P/R/F1."""
import re

T = ["The department bought a new server for the lab last month.",
     "It replaced an old machine that had failed twice.",
     "Ravi configured the server with the lab's toolchain.",
     "He then installed the compiler suite on it.",
     "The suite crashed when the memory filled during a build.",
     "Ravi reported the fault to the vendor, and the vendor replaced a faulty module."]

LEX = {"compiler suite": "software", "old machine": "machine", "faulty module": "component",
       "department": "org", "server": "machine", "lab": "place", "ravi": "human",
       "toolchain": "software", "memory": "component", "vendor": "org", "fault": "event", "build": "event"}
DEFINITE = {"the suite": "compiler suite"}          # definite description -> earlier entity
PRON = {"it", "he"}
WEIGHTS = dict(role=0.35, recency=0.25, repetition=0.20, semantic=0.10, parallel=0.10)
TIE_MARGIN = 0.05

GOLD = {(2, "it"): "server", (4, "he"): "ravi", (4, "it"): "server", (5, "the suite"): "compiler suite"}

PAT = re.compile(r"\b(" + "|".join(sorted(list(LEX) + list(DEFINITE) + list(PRON), key=len, reverse=True)) + r")\b", re.I)

def allowed_types(pron, sentence):
    if pron == "he": return {"human"}
    if re.search(r"\b(replaced|installed)\b", sentence.lower()):
        return {"machine"}                                  # selectional restriction of the verb
    return {"machine", "software", "org", "component"}

def score(c, pron_role, pron, cur):
    last_sent, last_role = c["last"]
    s = {"role": 1.0 if last_role == "subject" else 0.5,
         "recency": 1.0 / (1 + cur - last_sent),
         "repetition": min(c["count"], 3) / 3,
         "semantic": 1.0 if (pron == "it" and c["type"] == "machine") or (pron == "he" and c["type"] == "human") else 0.4,
         "parallel": 1.0 if last_role == pron_role else 0.0}
    return sum(WEIGHTS[k] * v for k, v in s.items())

def resolve_all(verbose=True):
    ents, links = {}, {}
    for n, sent in enumerate(T, 1):
        for i, m in enumerate(PAT.finditer(sent)):
            surf = m.group(1).lower()
            role = "subject" if i == 0 else "object"
            if surf in PRON or surf in DEFINITE:
                if surf in DEFINITE:
                    status, ref, cands = "resolved", DEFINITE[surf], {DEFINITE[surf]: 1.0}
                else:
                    ok = allowed_types(surf, sent)
                    cands = {k: score(v, role, surf, n) for k, v in ents.items() if v["type"] in ok}
                    ranked = sorted(cands.items(), key=lambda kv: -kv[1])
                    if not ranked: status, ref = "unresolved", None
                    elif len(ranked) > 1 and ranked[0][1] - ranked[1][1] < TIE_MARGIN: status, ref = "ambiguous", None
                    else: status, ref = "resolved", ranked[0][0]
                links[(n, surf)] = ref
                if ref:
                    ents[ref]["count"] += 1; ents[ref]["last"] = (n, role)
                if verbose:
                    print(f"S{n} '{surf}' -> {ref} [{status}] candidates={ {k: round(v, 2) for k, v in cands.items()} }")
            else:
                e = ents.setdefault(surf, {"type": LEX[surf], "count": 0, "last": (n, role)})
                e["count"] += 1; e["last"] = (n, role)
    return links

def prf(tp, predicted, gold):
    p = tp / predicted if predicted else 0.0
    r = tp / gold if gold else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f

if __name__ == "__main__":
    links = resolve_all()
    pred = {k: v for k, v in links.items() if v}
    tp = sum(GOLD.get(k) == v for k, v in pred.items())
    print("\nOwn resolver: TP=%d predicted=%d gold=%d -> P=%.2f R=%.2f F1=%.3f" % ((tp, len(pred), len(GOLD)) + prf(tp, len(pred), len(GOLD))))
    print("System X (assignment): P=%.2f R=%.2f F1=%.3f" % prf(3, 5, 4))
    print("System Y (assignment): P=%.2f R=%.2f F1=%.3f" % prf(3, 3, 4))
    # Pleonastic 'it' check
    for s in ["It is raining.", "It is said that the lab is closed."]:
        print(f"{s!r}: non-referential 'it'? {bool(re.match(r'it is (raining|said|likely|clear)', s.lower()))}")
