"""CO5 A5 - Forward GEN/KILL salience analysis to a fixed point; backward presupposition (must) analysis."""

UNITS = ["U1", "U2", "U3", "U4", "U5", "U6", "U7"]
PRED = {"U1": [], "U2": ["U1"], "U3": ["U2"], "U4": ["U3"], "U5": ["U4"], "U6": ["U5"], "U7": ["U6"]}
GEN = {"U1": {"server", "lab"}, "U2": {"old machine"}, "U3": {"Ravi", "toolchain"}, "U4": {"suite"},
       "U5": {"memory"}, "U6": {"vendor", "fault", "Ravi"}, "U7": {"module"}}
KILL = {"U1": set(), "U2": set(), "U3": {"lab", "old machine"}, "U4": {"toolchain"},
        "U5": {"server", "Ravi"}, "U6": {"suite", "memory"}, "U7": {"fault", "Ravi"}}   # topic-based pruning

def forward(units, pred, gen, kill, join=lambda sets: set().union(*sets) if sets else set()):
    IN = {u: set() for u in units}; OUT = {u: set() for u in units}
    passes, changed = 0, True
    while changed:
        changed = False; passes += 1
        for u in units:                                   # document order
            new_in = join([OUT[p] for p in pred[u]])
            new_out = gen[u] | (new_in - kill[u])         # OUT = GEN U (IN - KILL)
            if new_in != IN[u] or new_out != OUT[u]:
                IN[u], OUT[u], changed = new_in, new_out, True
    return IN, OUT, passes

def backward_presupposition(units, succ, req, defined):
    """Entities that must already be known on entry. Intersection join (must-analysis), initialised at end with {}."""
    IN = {u: set() for u in units}
    changed = True
    while changed:
        changed = False
        for u in reversed(units):
            outs = [IN[s] for s in succ[u]]
            out = set.intersection(*outs) if outs else set()
            new_in = req[u] | (out - defined[u])
            if new_in != IN[u]: IN[u], changed = new_in, True
    return IN

if __name__ == "__main__":
    IN, OUT, passes = forward(UNITS, PRED, GEN, KILL)
    for u in UNITS: print(f"{u}: OUT={sorted(OUT[u])}")
    print("Passes until fixed point:", passes, "(last pass only confirms no change)")

    print("\n-- Join demo: branch where one path introduces 'vendor' and the other 'fault' --")
    P2 = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]}
    G2 = {"A": {"server"}, "B": {"vendor"}, "C": {"fault"}, "D": set()}
    K2 = {u: set() for u in P2}
    for name, join in [("may (union)", lambda s: set().union(*s)), ("must (intersection)", lambda s: set.intersection(*s) if s else set())]:
        _, o, p = forward(list(P2), P2, G2, K2, join)
        print(f"  {name:20} OUT(D) = {sorted(o['D'])} after {p} passes")

    succ = {u: [UNITS[i + 1]] if i + 1 < len(UNITS) else [] for i, u in enumerate(UNITS)}
    REQ = {"U1": set(), "U2": {"server"}, "U3": {"server"}, "U4": {"Ravi", "server"}, "U5": {"suite"}, "U6": set(), "U7": {"vendor"}}
    print("\nBackward presupposition at document start:", sorted(backward_presupposition(UNITS, succ, REQ, GEN)["U1"]), "(everything is introduced in-text)")
    print("If the text started at U2:", sorted(backward_presupposition(UNITS[1:], succ, REQ, GEN)["U2"]))
