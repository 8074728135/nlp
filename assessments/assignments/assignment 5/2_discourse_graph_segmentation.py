"""CO5 A2 - Discourse unit segmentation, relation graph with right-frontier attachment, backward next-mention scan."""
import re

T = ["The department bought a new server for the lab last month.",
     "It replaced an old machine that had failed twice.",
     "Ravi configured the server with the lab's toolchain.",
     "He then installed the compiler suite on it.",
     "The suite crashed when the memory filled during a build.",
     "Ravi reported the fault to the vendor, and the vendor replaced a faulty module."]

def segment(text):
    """Sentence -> units; split coordinated clauses only when ', and ' is followed by a new subject."""
    units = []
    for s in text:
        parts = re.split(r",\s+and\s+(?=the |a |[A-Z])", s)
        for p in parts:
            p = p.strip().rstrip(".")
            units.append(p[0].upper() + p[1:] + ".")
    return units

def relation(unit, prev_unit, coordinated_split):
    low = unit.lower()
    if coordinated_split: return "Response", False
    if re.match(r"^(it|this|that)\b", low): return "Elaboration", False
    if " then " in f" {low} ": return "Sequence", False
    if re.search(r"\b(crashed|failed|broke)\b", low): return "Result", True      # inferred, no explicit cue
    return "Sequence", False

SATELLITE = {"Elaboration"}

def build_graph(units):
    edges, frontier = [], [1]
    for n in range(2, len(units) + 1):
        split = T_SPLIT.get(n, False)
        rel, inferred = relation(units[n - 1], units[n - 2], split)
        if rel in SATELLITE:                                   # subordinate: attach to last unit, keep parent open
            parent = frontier[-1]; frontier.append(n)
        else:                                                  # coordinating: attach to nearest nucleus, close satellites
            parent = next(u for u in reversed(frontier) if not SAT.get(u))
            frontier = frontier[:frontier.index(parent)] + [n]
        if rel in SATELLITE: SAT[n] = True
        edges.append((parent, n, rel + (" (inferred)" if inferred else "")))
    return edges

SAT, T_SPLIT = {}, {7: True}   # unit 7 was created by splitting sentence 6

UNIT_ENTITIES = [   # referents per unit (pronouns already resolved, see co5_1)
    {"department", "server", "lab"}, {"server", "old machine"}, {"Ravi", "server", "toolchain"},
    {"Ravi", "compiler suite", "server"}, {"compiler suite", "memory", "build"},
    {"Ravi", "fault", "vendor"}, {"vendor", "faulty module"}]

def next_mention_scan(unit_entities):
    """Backward scan: remember where each entity is mentioned next while moving from end to start."""
    nxt, table = {}, []
    for u in range(len(unit_entities), 0, -1):
        for e in sorted(unit_entities[u - 1]):
            table.append((u, e, nxt.get(e), (nxt[e] - u) if e in nxt else None))
        for e in unit_entities[u - 1]: nxt[e] = u
    return sorted(table)

if __name__ == "__main__":
    units = segment(T)
    for i, u in enumerate(units, 1): print(f"U{i}: {u}")
    print("\nDiscourse edges (parent -> child : relation):")
    for p, c, r in build_graph(units): print(f"  U{p} -> U{c} : {r}")
    print("\nNext-mention table (unit, entity, next unit, distance):")
    for u, e, nu, d in next_mention_scan(UNIT_ENTITIES):
        print(f"  U{u:<2} {e:15} next={'U'+str(nu) if nu else 'none':5} distance={d if d else '-'}  {'available' if nu else 'unavailable'}")
