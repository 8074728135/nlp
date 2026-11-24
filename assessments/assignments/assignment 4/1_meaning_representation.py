"""CO4 Task 1 - Meaning representation: event structure + frame/slot, validation, queries."""
import re

T = r"yesterday|after the meeting"
PATTERNS = [
    rf"^(?:(?P<tp>{T}),\s+)?(?P<ag>\w+) (?P<v>gave|sent) (?P<rc>\w+) (?:a|the) (?P<th>\w+)(?: (?P<t>{T}))?\.$",
    rf"^(?:(?P<tp>{T}),\s+)?(?P<ag>\w+) (?P<v>gave|sent) (?:a|the) (?P<th>\w+) to (?P<rc>\w+)(?: (?P<t>{T}))?\.$",
    rf"^(?:(?P<tp>{T}),\s+)?(?:a|the) (?P<th>\w+) was (?P<v>given|sent) to (?P<rc>\w+) by (?P<ag>\w+)(?: (?P<t>{T}))?\.$",
    rf"^(?P<rc>\w+) received (?:a|the) (?P<th>\w+) from (?P<ag>\w+)(?: (?P<t>{T}))?\.$",
]

def parse(sentence):
    """Return a role-labelled event dict, or None if no pattern matches."""
    for p in PATTERNS:
        m = re.match(p, sentence.strip(), re.I)
        if m:
            g = m.groupdict()
            verb = (g.get("v") or "gave").lower()
            time = g.get("tp") or g.get("t")
            return {"event": "SEND" if verb == "sent" else "GIVE",
                    "agent": g["ag"].title(), "theme": g["th"].lower(),
                    "recipient": g["rc"].title(),
                    "time": time.lower() if time else None}   # None = unspecified, never guessed
    return None

def validate(ev):
    """Every event needs exactly one agent and one theme; recipient optional."""
    errors = []
    if not ev.get("agent"): errors.append("missing AGENT")
    if not ev.get("theme"): errors.append("missing THEME")
    return errors

def as_relations(ev, eid="e1"):
    rel = [f"{ev['event']}({eid})", f"AGENT({eid},{ev['agent']})",
           f"THEME({eid},{ev['theme'].title()}1)", f"RECIPIENT({eid},{ev['recipient']})"]
    if ev["time"]: rel.append(f"TIME({eid},{ev['time']})")
    return rel

def as_frame(ev):
    return {"EVENT": ev["event"], "GIVER/SENDER": ev["agent"], "RECEIVER": ev["recipient"],
            "OBJECT": ev["theme"], "TIME": ev["time"] or "unspecified"}

def who_received(ev): return ev["recipient"]

def same_meaning(a, b): return a == b

if __name__ == "__main__":
    base = parse("Maya gave Ravi a book yesterday.")
    print("Relations:", as_relations(base))
    print("Frame    :", as_frame(base))
    print("Who received the book?", who_received(base))
    print("Validation errors:", validate(base) or "none")
    print("\n-- Meaning-preserving variants (Task 1.3 / Appendix A) --")
    for s in ["A book was given to Ravi by Maya yesterday.",
              "Yesterday, Maya gave a book to Ravi."]:
        print(f"{s!r:55} same as base? {same_meaning(parse(s), base)}")
    print("\n-- Meaning-changing variants --")
    for s in ["Ravi gave Maya a book yesterday.", "Maya received a book from Ravi."]:
        ev = parse(s)
        print(f"{s!r:55} same as base? {same_meaning(ev, base)}  roles={ev['agent']}->{ev['recipient']}")
    print("\n-- Part II Task 1: Leena sent the report to Arun after the meeting --")
    s1 = parse("Leena sent the report to Arun after the meeting.")
    s2 = parse("After the meeting, the report was sent to Arun by Leena.")
    s3 = parse("Arun sent the report to Leena after the meeting.")
    print("Frame:", as_frame(s1))
    print("Passive rewrite preserves meaning:", same_meaning(s1, s2))
    print("Swapped version preserves meaning:", same_meaning(s1, s3))
    # Graph form: (head, relation, dependent) triples
    print("Graph:", [("Leena", "AGENT", "e1"), ("report", "THEME", "e1"),
                     ("e1", "RECIPIENT", "Arun"), ("e1", "TIME", "after(meeting)")])
