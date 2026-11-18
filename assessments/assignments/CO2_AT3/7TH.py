import re
import time
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_predict, LeaveOneOut
from sklearn.metrics import accuracy_score

stemmer = PorterStemmer()

# ORIGINAL faulty program
documents = [
    "running runners runs",
    "studies studied studying",
    "organization organized organizer"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

features = [
    stemmer.stem(word)
    for word in vectorizer.get_feature_names_out()
]

print("ORIGINAL: matrix columns =", X.shape[1], "| features =", features)
print(
    "unique features =",
    len(set(features)),
    "(duplicates are still separate columns)"
)

# CORRECTED program
def stem_analyzer(doc):
    return [
        stemmer.stem(w)
        for w in re.findall(r"[a-z]+", doc.lower())
    ]

vec2 = CountVectorizer(analyzer=stem_analyzer)
X2 = vec2.fit_transform(documents)

print(
    "\nCORRECTED: matrix columns =",
    X2.shape[1],
    "| features =",
    list(vec2.get_feature_names_out())
)

# Comparison on a small labelled sample
docs = [
    "runners were running along the track while the coach runs drills",
    "she runs daily and the runner trained for racing",
    "running clubs organized races and the runners trained hard",
    "the coach trains runners and races are run on weekends",
    "training schedules help runners improve their running times",
    "he trained hard and ran the race with other runners",
    "students were studying for exams while the teacher studies lessons",
    "she studies nightly and the student studied for testing",
    "study groups organized lessons and the students learned quickly",
    "the teacher teaches students and lessons are studied on weekends",
    "learning schedules help students improve their studying habits",
    "he studied hard and learned the lesson with other students"
]

y = [0] * 6 + [1] * 6

def evaluate(vec, repeats=200):
    start = time.perf_counter()

    for _ in range(repeats):
        Xv = vec.fit_transform(docs)

    ms = (time.perf_counter() - start) / repeats * 1000

    pred = cross_val_predict(
        MultinomialNB(),
        Xv,
        y,
        cv=LeaveOneOut()
    )

    return Xv.shape[1], accuracy_score(y, pred), ms

print("\nCOMPARISON")

for name, vec in [
    (
        "Original (no stemming in matrix)",
        CountVectorizer(
            analyzer=lambda d: re.findall(r"[a-z]+", d.lower())
        )
    ),
    (
        "Corrected (stem inside analyzer)",
        CountVectorizer(analyzer=stem_analyzer)
    )
]:
    v, acc, ms = evaluate(vec)

    print(
        f"{name:<33} vocabulary = {v:<3} "
        f"accuracy = {acc:.3f} time = {ms:.2f} ms"
    )