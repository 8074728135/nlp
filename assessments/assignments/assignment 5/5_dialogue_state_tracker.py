"""CO5 B3 - Dialogue acts, status-based state tracking, safety tests, full-history vs windowed cost."""
import re

STATUSES = ["mentioned", "requested", "offered", "confirmed", "checked", "completed"]
CATALOGUE = {"NLP book": True}                     # simulated backend

def classify(utt, speaker):
    """Rule-based dialog acts; one utterance may hold several acts (split on sentences)."""
    acts = []
    for s in [x.strip() for x in re.split(r"(?<=[.?!])\s+", utt) if x.strip()]:
        low = s.lower()
        if re.search(r"\b(thanks|thank you)\b", low): acts.append(("thanks", s))
        elif speaker == "user" and re.match(r"^(yes|yeah|sure|ok)\b", low): acts.append(("accept", s))
        elif re.search(r"\bi meant\b", low): acts.append(("repair", s))
        elif speaker == "agent" and re.search(r"\bwould you like\b", low): acts.append(("offer", s))
        elif speaker == "agent" and re.search(r"\b(could you|can you|please)\b.*\?$", low): acts.append(("request_info", s))
        elif s.endswith("?"): acts.append(("question", s))
        elif speaker == "user" and re.search(r"\b(i need|book it|renew)\b", low): acts.append(("request", s))
        else: acts.append(("inform", s))
    return acts

class State:
    def __init__(self): self.items, self.pending_offer, self.history = {}, None, []
    def set(self, k, v): self.items[k] = v

    def update(self, speaker, utt):
        for act, s in classify(utt, speaker):
            low = s.lower()
            if act == "request" and "renew" in low: self.set("renewal", "requested")
            elif act == "request_info": self.set("library_id", "requested")
            elif act == "inform" and speaker == "user" and re.search(r"\b\d{4}[a-z]{2}\d+\b", low): self.set("library_id", "confirmed")
            elif act == "offer": self.pending_offer = "renewal"; self.set("renewal", "offered")
            elif act == "accept" and self.pending_offer:      # only the immediately preceding clear offer
                self.set(self.pending_offer, "confirmed"); self.pending_offer = None
            elif act == "question" and "nlp book" in low and "available" in low:
                self.set("nlp_availability", "requested")      # a question is NOT a fact
            elif act == "inform" and speaker == "agent" and "available" in low and "nlp book" in low:
                self.set("nlp_availability", "checked" if CATALOGUE.get("NLP book") else "mentioned")
            elif act == "inform" and speaker == "agent" and "reserved" in low and self.items.get("nlp_availability") == "checked":
                self.set("nlp_reservation", "completed")   # only after a verified check
            elif act == "repair":
                m = re.search(r"i meant (.+?),? not (.+?)\.?$", low)
                if m: self.history.append(("repair", m.group(2), m.group(1))); self.set("entity", m.group(1))
            self.history.append((speaker, act, s))
        return self

DIALOGUE_D = [("user", "I need to renew my books."), ("agent", "Could you give me your library ID?"),
              ("user", "It is 2024CS118."), ("agent", "Would you like a two-week renewal?"),
              ("user", "Yes please. Is the NLP book available?"),
              ("agent", "Yes, the NLP book is available. I reserved it until tomorrow."),
              ("user", "Thanks, that's all.")]

def cost_full(T, E):  # re-scan all turns for every tracked entity at every update
    ops = 0
    for t in range(1, T + 1):
        for _ in range(t):
            for _ in range(E): ops += 1
    return ops

def cost_window(T, E_active, W=4):
    ops = 0
    for t in range(1, T + 1):
        for _ in range(min(W, t)):
            for _ in range(E_active): ops += 1
    return ops

if __name__ == "__main__":
    st = State()
    for sp, u in DIALOGUE_D:
        st.update(sp, u)
        print(f"{sp:5}: {u}\n       acts={[a for a, _ in classify(u, sp)]} state={st.items}")
    print("\n-- Safety: question must not become a fact --")
    s2 = State().update("user", "Is the NLP book available?")
    print(s2.items, "-> correct reply: 'I will check the catalogue.'" if s2.items["nlp_availability"] == "requested" else "UNSAFE")
    print("\n-- Repair keeps history --")
    s3 = State().update("user", "I meant Tuesday, not Thursday.")
    print(s3.items, s3.history[0])
    print("\n-- Per-turn act accuracy on 3 mini dialogues --")
    gold = [("user", "When is the lab open?", ["question"]), ("user", "Book it for Friday.", ["request"]),
            ("user", "I meant Tuesday, not Thursday.", ["repair"])]
    ok = sum([a for a, _ in classify(u, sp)] == g for sp, u, g in gold)
    print(f"{ok}/{len(gold)} correct")
    print("\n-- Operation counts (measured by loops) --")
    print(f"{'turns/entities':16}{'full history':>14}{'window W=4':>12}")
    for T, E in [(10, 5), (50, 15), (100, 30)]:
        print(f"{T}/{E:<13}{cost_full(T, E):>14}{cost_window(T, E):>12}")
