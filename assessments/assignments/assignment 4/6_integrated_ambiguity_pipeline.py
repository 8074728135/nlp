"""CO4 Task 6 - Integrated ambiguity analysis: WSD + pronoun check + sense-aware retrieval + clarification."""
import re

SENSES = {   # word -> sense -> (context clues, retrieval tags)
    "bank":  {"FINANCIAL": (["deposit", "money", "loan", "account", "branch", "cash", "closed", "hours"], ["financial", "bank", "branch"]),
              "RIVER":     (["river", "water", "shore", "walking", "beside", "fishing", "reed"], ["river", "bank", "shore"])},
    "duck":  {"BIRD":  (["pond", "feather", "pet", "swim", "bird"], ["duck", "bird"]),
              "LOWER": (["ball", "avoid", "quickly", "hit", "low"], ["lower", "body"])},
    "crane": {"MACHINE": (["construction", "lift", "load", "operator", "truck", "building", "site", "steel"], ["construction", "crane", "machine"]),
              "BIRD":    (["wing", "nest", "migrat", "water", "reed", "feather"], ["crane", "bird", "river"])},
}
PROP_OK = {"closed": {"FINANCIAL"}, "moved": {"MACHINE", "BIRD"}}       # selectional restrictions
PROP_TERMS = {"closed": ["closed", "opening hours"], "moved": ["movement"]}
ARTICLES = {
    "A1 Why a bank branch may be closed": {"financial", "bank", "branch", "closed", "opening hours"},
    "A2 River-bank safety": {"river", "bank", "safety"},
    "A3 Duck care": {"duck", "bird", "care"},
    "A4 How to lower aircraft or equipment": {"lower", "aircraft", "equipment"},
    "C1 Construction crane movement near buildings": {"construction", "crane", "machine", "movement", "building"},
    "C2 Crane bird behaviour near rivers": {"crane", "bird", "river", "behaviour"},
}
CONF_MIN = 0.7

def words(s): return re.findall(r"[a-z']+", s.lower())

def pick_sense(word, toks, ctx_toks, prev_tok):
    scores = {}
    for sense, (clues, _) in SENSES[word].items():
        scores[sense] = sum(any(t.startswith(c) for t in toks + ctx_toks) for c in clues)
    if word == "duck" and prev_tok in {"her", "his", "my", "the", "a"}:
        scores["BIRD"] += 1                                  # noun reading: determiner + duck
    for prop, ok in PROP_OK.items():                          # 'closed'/'moved' are selectional clues
        if prop in toks:
            for s in scores:
                if s in ok and s in SENSES[word]: scores[s] += 1 if prop == "closed" else 0
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    (best, bs), second = ranked[0], (ranked[1][1] if len(ranked) > 1 else 0)
    conf = bs / (bs + second + 1) if bs > second else 0.0
    return best, round(conf, 2), scores

def analyze(message, context=""):
    toks, ctx = words(message), words(context)
    found = {}
    for w in SENSES:
        if w in toks:
            i = toks.index(w)
            found[w] = pick_sense(w, toks, ctx, toks[i - 1] if i else "")
    prop = next((p for p in PROP_OK if p in toks), None)
    print(f"\nMESSAGE: {message}" + (f"   CONTEXT: {context}" if context else ""))
    for w, (s, c, sc) in found.items():
        print(f"  {w:6} -> {s:9} confidence={c} scores={sc}")
    if "it" in toks and prop:
        cands = [w for w, (s, _, _) in found.items() if s in PROP_OK[prop]]
        print(f"  pronoun 'it' (needs a referent that can be '{prop}'): ->", cands or "UNRESOLVED (needs another referent)")
    # retrieval: only for the entity the property applies to
    target = next((w for w, (s, _, _) in found.items() if prop and s in PROP_OK[prop]), None)
    unsure = any(c < CONF_MIN for (_, c, _) in found.values() if True) if target is None else found[target][1] < CONF_MIN
    if target is None:
        print("  -> No sense-compatible target: ask a clarification question."); return
    sense = found[target][0]
    q = set(SENSES[target][sense][1]) | set(PROP_TERMS.get(prop, []))
    print("  query terms:", sorted(q))
    ranking = sorted(((len(q & tags), a) for a, tags in ARTICLES.items()), reverse=True)[:3]
    for sc, a in ranking: print(f"    {sc}  {a}")
    if unsure:
        label = "financial bank branch" if target == "bank" else f"{target} ({' or '.join(SENSES[target])})"
        print(f"  CLARIFY: low confidence. Ask: 'Do you mean {label}?'")

if __name__ == "__main__":
    analyze("I saw her duck near the bank, and it was closed.")
    analyze("I saw her duck near the bank, and it was closed.", "I went to deposit money.")
    analyze("I saw her duck near the bank, and it was closed.", "We were walking beside the river.")
    analyze("I watched the crane by the bank, then it moved.")
    analyze("I watched the crane by the bank, then it moved.", "The operator used it to lift steel at the construction site.")
