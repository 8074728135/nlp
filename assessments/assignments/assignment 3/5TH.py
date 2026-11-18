import re
import pandas as pd
from nltk.stem import PorterStemmer

ps = PorterStemmer()

# data = pd.read_csv("bbc-text.csv")

data = pd.DataFrame({
    "text": [
        "The government announced new policies as companies and cities reported various economic problems",
        "News about the university studies showed that parties in many countries tried to tell stories about electricity",
        "Communication between communities is generally reliable and local organization carried the main work",
        "The business was operating happily while a new generation was studying economic reports",
        "Officials said the responsible leaders had visited the stories"
    ]
})

# ORIGINAL faulty code
data["Original_Result"] = data["text"].apply(ps.stem)

print("ORIGINAL CODE (first row):")
print(data["Original_Result"][0])

# CORRECTED code
def stem_text(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    return " ".join(ps.stem(t) for t in tokens)

data["Processed"] = data["text"].apply(stem_text)

print("\nCORRECTED CODE (first row):")
print(data["Processed"][0])

GOLD = {
    "policies": ("policy", "inflectional"),
    "companies": ("company", "inflectional"),
    "cities": ("city", "inflectional"),
    "countries": ("country", "inflectional"),
    "parties": ("party", "inflectional"),
    "stories": ("story", "inflectional"),
    "studies": ("study", "inflectional"),
    "studying": ("study", "inflectional"),
    "carried": ("carry", "inflectional"),
    "tried": ("try", "inflectional"),
    "operating": ("operate", "inflectional"),
    "communities": ("community", "inflectional"),
    "news": ("news", "inflectional rule misapplied"),
    "various": ("various", "inflectional rule misapplied"),
    "happily": ("happy", "derivational"),
    "economic": ("economy", "derivational"),
    "generally": ("general", "derivational"),
    "generation": ("generate", "derivational"),
    "organization": ("organize", "derivational"),
    "electricity": ("electric", "derivational"),
    "communication": ("communicate", "derivational"),
    "reliable": ("rely", "derivational"),
    "responsible": ("respond", "derivational"),
    "business": ("busy", "derivational"),
    "university": ("universe", "derivational")
}

words = sorted({
    w for t in data["text"]
    for w in re.findall(r"[a-z]+", t.lower())
})

bad = [
    (w, ps.stem(w), *GOLD[w])
    for w in words
    if w in GOLD and ps.stem(w) != GOLD[w][0]
]

print(f"\nINCORRECT STEMMING CASES ({len(bad)} found)")
print(f"{'No.':<4}{'Original':<15}{'Stem':<11}{'Correct root':<14}Type")

for i, (w, s, root, kind) in enumerate(bad, 1):
    print(f"{i:<4}{w:<15}{s:<11}{root:<14}{kind}")

for k in (
    "inflectional",
    "inflectional rule misapplied",
    "derivational"
):
    print(
        f"Count - {k}: "
        f"{sum(1 for b in bad if b[3] == k)}"
    )