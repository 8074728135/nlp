"""CO5 A3 - Generator with focus list (k=2), given/new flags, referring-expression choice, aggregation."""

class Ent:
    def __init__(self, eid, noun, agr, proper=False, focusable=True, short=None):
        self.id, self.noun, self.agr, self.proper, self.focusable = eid, noun, agr, proper, focusable
        self.short = short or noun            # shorter noun for later definite mentions

SERVER = Ent("server_1", "server", "it")
RAVI = Ent("Ravi", "Ravi", "masc", proper=True)
SUITE = Ent("suite_1", "compiler suite", "it", short="suite")
BUILD = Ent("build_1", "build", "it", focusable=False)
ARUN = Ent("Arun", "Arun", "masc", proper=True)

PLAN = [  # (template with {0},{1}.., entities in order of mention)
    ("{0} has 32 GB of memory", [SERVER]),
    ("{0} configured {1}", [RAVI, SERVER]),
    ("{0} installed {1} on {2}", [RAVI, SUITE, SERVER]),
    ("{0} crashed during {1}", [SUITE, BUILD]),
]

class Realiser:
    def __init__(self, k=2, given=()):
        self.k, self.focus, self.mentioned = k, [], set(given)
        self.role = {}                                   # last role weight per entity (subject=2, object=1)

    def choose_form(self, e, props, first):
        """CHOOSE_FORM: new -> indefinite/name; focused & no agreement competitor -> pronoun; else definite/name."""
        if e.id not in self.mentioned:
            np = e.noun if e.proper else "a " + e.noun
        elif e.proper:
            competitor = any(o is not e and o.agr == e.agr for o in props)
            np = e.noun if (e.id not in self.focus or competitor) else ("He" if first else "he")
        else:
            competitor = any(o is not e and o.agr == e.agr for o in props)
            if e.id in self.focus and not competitor: np = "It" if first else "it"
            else: np = "the " + e.short
        return np[0].upper() + np[1:] if first else np

    def realise(self, template, ents, future):
        forms = [self.choose_form(e, ents, i == 0) for i, e in enumerate(ents)]
        # the sentence-initial slot is capitalised; others are left as chosen
        text = template.format(*forms) + "."
        self.update(ents, future)
        return text

    def update(self, ents, future):
        for i, e in enumerate(ents):
            self.mentioned.add(e.id)
            self.role[e.id] = 2 if i == 0 else 1
        pool = set(self.focus) | {e.id for e in ents if e.focusable}
        need = {x.id for f in future for x in f}
        order = {e.id: n for n, e in enumerate(ents)}
        self.focus = sorted(pool, key=lambda i: (i not in need, -self.role.get(i, 0), order.get(i, 99)))[: self.k]

def aggregate(subj1, pred1, subj2, pred2):
    return f"{subj1} {pred1} and {pred2}." if subj1 == subj2 else None

def wc(s): return len(s.split())

if __name__ == "__main__":
    naive = ["The server has 32 GB of memory.", "Ravi configured the server.",
             "Ravi installed a compiler suite on the server.", "The compiler suite crashed during a build."]  # naive: full noun phrase every time
    r = Realiser(k=2, given={"server_1"})
    smart = []
    for n, (tpl, ents) in enumerate(PLAN):
        future = [p[1] for p in PLAN[n + 1:]]
        out = r.realise(tpl, ents, future)
        smart.append(out)
        print(f"F{n+1}: {out:50} focus={r.focus}")
    print(f"\nNaive words: {sum(map(wc, naive))}  | Focus-list words: {sum(map(wc, smart))}")
    print("Aggregated F2+F3:", aggregate("Ravi", "configured it", "Ravi", "installed a compiler suite on the server"))
    print("\n-- Failure / safety case: two masculine entities --")
    r2 = Realiser(k=2, given={"Ravi", "Arun"}); r2.focus = ["Ravi", "Arun"]
    print("Ravi told Arun that", r2.choose_form(RAVI, [RAVI, ARUN], False), "had completed the build  <- name repeated, pronoun blocked")
