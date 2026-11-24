"""CO5 B4 - Translation service: level selection policy + post-translation validation of facts."""
import re

NOTICE = ("The lab server will be down on 25 November from 9 AM to 11 AM. "
          "It must not be used during this time. Ravi will restore it by 12 PM.")

PRONOUNS = r"\b(it|he|she|they)\b"
NEGATION_MARKERS = {"hi": ["नहीं", "मत"], "ta": ["கூடாது", "வேண்டாம்"]}
DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
TAMIL_DIGITS = str.maketrans("௦௧௨௩௪௫௬௭௮௯", "0123456789")

def count_pronouns(text): return len(re.findall(PRONOUNS, text, re.I))

def resolve_simple(text):
    """Level-1 style: replace sentence-initial 'It' by the previous sentence's subject (high-confidence case only)."""
    sents = re.split(r"(?<=\.)\s+", text)
    subj = None
    out = []
    for s in sents:
        m = re.match(r"^(The [\w ]+?) (will|must|has|is)\b", s)
        if m and not s.startswith("It"): subj = m.group(1)
        if s.startswith("It ") and subj: s = subj + s[2:]
        out.append(s)
    return " ".join(out)

def choose_level(n_sentences, n_pronouns, high_impact, latency_critical=False):
    """Lowest-cost level that meets the need; escalate with ambiguity/risk."""
    if latency_critical and not high_impact and n_pronouns == 0: return 0
    if high_impact or n_sentences > 8 or n_pronouns > 3: return 2
    return 1

def facts(text):
    t = text.translate(DEVANAGARI_DIGITS).translate(TAMIL_DIGITS)
    return {"numbers": sorted(re.findall(r"\d+", t))}

def validate(source, translation, lang):
    """Check numbers preserved and negation/obligation kept; returns list of problems."""
    problems = []
    if facts(source)["numbers"] != facts(translation)["numbers"]:
        problems.append(f"numbers differ: {facts(source)['numbers']} vs {facts(translation)['numbers']}")
    if re.search(r"\bmust not\b|\bmay not\b|\bdo not\b", source, re.I) and not any(m in translation for m in NEGATION_MARKERS[lang]):
        problems.append("negation/prohibition missing")
    return problems

HI_GOOD = "लैब सर्वर 25 नवंबर को सुबह 9 बजे से 11 बजे तक बंद रहेगा। इस दौरान इसका उपयोग नहीं करना है। रवि इसे दोपहर 12 बजे तक चालू कर देंगे।"
HI_BAD = "लैब सर्वर 25 नवंबर को सुबह 9 बजे से 11 बजे तक बंद रहेगा। इस दौरान इसका उपयोग किया जा सकता है। रवि इसे दोपहर 2 बजे तक चालू कर देंगे।"

if __name__ == "__main__":
    print("Source pronouns:", count_pronouns(NOTICE))
    resolved = resolve_simple(NOTICE)
    print("After reference resolution:", resolved)
    print("Pronouns left:", count_pronouns(resolved), "(remaining 'it' in sentence 3 needs full resolver / human review)")
    print("\nLevel policy:")
    for desc, args in [("short preview", (1, 0, False, True)), ("routine notice", (3, 2, False)),
                       ("safety notice", (3, 2, True)), ("long ambiguous report", (12, 6, False))]:
        print(f"  {desc:22} -> Level {choose_level(*args)}")
    print("\nValidation of candidate Hindi translations:")
    print("  good:", validate(NOTICE, HI_GOOD, "hi") or "OK")
    print("  bad :", validate(NOTICE, HI_BAD, "hi"))
    print("\nNote: plug a real MT system (e.g. an NMT API) into the translate step; this file covers the pipeline control and fact-checking around it.")
