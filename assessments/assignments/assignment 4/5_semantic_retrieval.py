"""CO4 Task 5 - Lexical vs semantic retrieval, combined ranking, precision/recall."""
import math, re

QUERY = "methods for finding the meaning of ambiguous words"

# concept id -> surface terms (substring match; a tiny hand-built concept lexicon)
CONCEPTS = {
    "METHOD":  ["method", "algorithm", "technique", "classifier", "model", "lesk"],
    "MEANING": ["meaning", "interpretation", "intended"],
    "AMBIG":   ["ambigu", "polysem", "homonym", "lexical", "multiple senses", "disambiguation", "word sense"],
    "CONTEXT": ["context", "surrounding"],
}
QUERY_CONCEPTS = ["METHOD", "MEANING", "AMBIG"]
STOP = {"for", "the", "of", "a", "an", "and", "to", "in", "using"}

DOCS = {
    "D1": ("Word Sense Disambiguation using Context", "Methods that select the intended sense of an ambiguous word from its context."),
    "D2": ("Lesk Algorithm for Dictionary-Based Sense Selection", "A dictionary overlap algorithm to select the meaning of polysemous words."),
    "D3": ("Part-of-Speech Tagging for NLP", "Tagging words with grammatical categories using statistical models."),
    "D4": ("Banking Services and Loan Products", "Explains the meaning of banking terms such as loan and account."),
    "D5": ("Contextual Language Models for Meaning Selection", "Neural models use context to choose the intended meaning of words."),
    "D6": ("Resolving Lexical Polysemy with Surrounding Text", "Contextual interpretation of lexical polysemy using the Lesk method."),
}
GOLD_RELEVANT = {"D1", "D2", "D5", "D6"}

def stem(w): return w[:5]

def lexical(query, text):
    q = [stem(w) for w in re.findall(r"[a-z]+", query.lower()) if w not in STOP]
    t = {stem(w) for w in re.findall(r"[a-z]+", text.lower())}
    return sum(w in t for w in q) / len(q)

def concept_vec(text):
    text = text.lower()
    return {c: sum(text.count(t) for t in terms) for c, terms in CONCEPTS.items()}

def cosine(a, b):
    dot = sum(a[k] * b[k] for k in a)
    na, nb = math.sqrt(sum(v * v for v in a.values())), math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0

def concept_features(query_concepts, title, abstract):
    full = concept_vec(title + " " + abstract)
    tit = concept_vec(title)
    qv = {c: 1 if c in query_concepts else 0 for c in CONCEPTS}
    S = cosine(qv, {c: min(v, 3) for c, v in full.items()})        # semantic similarity
    C = sum(full[c] > 0 for c in query_concepts) / len(query_concepts)   # concept coverage
    F = sum(tit[c] > 0 for c in query_concepts) / len(query_concepts)    # field (title) importance
    return S, C, F

def rank(weights):
    wL, wS, wC, wF = weights
    rows = []
    for d, (title, abstract) in DOCS.items():
        L = lexical(QUERY, title + " " + abstract)
        S, C, F = concept_features(QUERY_CONCEPTS, title, abstract)
        rows.append((d, L, S, C, F, wL * L + wS * S + wC * C + wF * F))
    # tie-break: higher concept coverage first
    return sorted(rows, key=lambda r: (-r[5], -r[3]))

def precision_recall_at_k(ranked_ids, relevant, k):
    top = ranked_ids[:k]
    hit = sum(d in relevant for d in top)
    return hit / k, hit / len(relevant)

def show(name, weights, k=4):
    print(f"\n== {name}: weights L,S,C,F = {weights} ==")
    rows = rank(weights)
    print(f"{'doc':4} {'L':>5} {'S':>5} {'C':>5} {'F':>5} {'final':>6}")
    for d, L, S, C, F, fs in rows:
        print(f"{d:4} {L:5.2f} {S:5.2f} {C:5.2f} {F:5.2f} {fs:6.2f}  {'REL' if d in GOLD_RELEVANT else '-'}  {DOCS[d][0]}")
    ids = [r[0] for r in rows]
    p, r = precision_recall_at_k(ids, GOLD_RELEVANT, k)
    print(f"Precision@{k} = {p:.2f}   Recall@{k} = {r:.2f}")
    fp = [d for d in ids[:k] if d not in GOLD_RELEVANT]
    fn = [d for d in GOLD_RELEVANT if d not in ids[:k]]
    print("False positives in top-k:", fp or "none", "| False negatives:", fn or "none")

if __name__ == "__main__":
    print("Query:", QUERY)
    show("Keyword only", (1, 0, 0, 0))
    show("Part I combined (0.20L+0.45S+0.25C+0.10F)", (0.20, 0.45, 0.25, 0.10))
    show("Part II combined (0.2 lexical, 0.4 semantic, 0.3 coverage, 0.1 title)", (0.2, 0.4, 0.3, 0.1))
    # Generic metric demos from the assignment text
    print("\nExample: 3 relevant of 5 retrieved, 4 relevant in collection -> P=%.2f R=%.2f" % (3/5, 3/4))
