import re
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_predict, LeaveOneOut
from sklearn.metrics import accuracy_score, confusion_matrix

ps = PorterStemmer()

TECH = [
    "the organization released a new software update for developers",
    "organizers of the technology conference announced new chip designs",
    "engineers organized the data into a faster database system",
    "organizing large datasets requires scalable computing and clever algorithms",
    "the organization's cloud platform runs machine learning models",
    "developers are organizing open source code repositories",
    "new processors improve computing speed for mobile devices",
    "researchers trained neural networks on massive image datasets",
    "the company released a secure operating system for servers",
    "programmers organized the software modules into libraries",
    "wireless networks connect devices using faster protocols",
    "the organizer of the hackathon demonstrated robotics and automation"
]

BUSINESS = [
    "the organization reported higher quarterly profits and revenue",
    "organizers of the trade summit discussed market regulations",
    "executives organized the merger of two large banks",
    "organizing corporate finances requires careful budgeting and auditing",
    "the organization's shareholders approved the annual dividend",
    "investors are organizing a new venture capital fund",
    "stock markets rose as inflation and interest rates fell",
    "retailers increased prices after higher costs hit profits",
    "the company announced layoffs to cut operating expenses",
    "managers organized the quarterly sales targets by region",
    "banks lend money to businesses at lower interest rates",
    "the organizer of the investment forum praised economic growth"
]

docs = TECH + BUSINESS
labels = [0] * len(TECH) + [1] * len(BUSINESS)

LEMMA = {
    "organizing": "organize",
    "organized": "organize",
    "organizers": "organizer",
    "developers": "developer",
    "designs": "design",
    "engineers": "engineer",
    "datasets": "dataset",
    "algorithms": "algorithm",
    "models": "model",
    "repositories": "repository",
    "processors": "processor",
    "devices": "device",
    "researchers": "researcher",
    "networks": "network",
    "servers": "server",
    "programmers": "programmer",
    "modules": "module",
    "libraries": "library",
    "protocols": "protocol",
    "profits": "profit",
    "regulations": "regulation",
    "executives": "executive",
    "finances": "finance",
    "shareholders": "shareholder",
    "investors": "investor",
    "markets": "market",
    "rates": "rate",
    "retailers": "retailer",
    "prices": "price",
    "costs": "cost",
    "layoffs": "layoff",
    "expenses": "expense",
    "managers": "manager",
    "targets": "target",
    "businesses": "business",
    "announced": "announce",
    "released": "release",
    "trained": "train",
    "increased": "increase",
    "approved": "approve",
    "rose": "rise",
    "fell": "fall",
    "discussed": "discuss",
    "reported": "report",
    "requires": "require",
    "runs": "run",
    "praised": "praise",
    "demonstrated": "demonstrate",
    "using": "use",
    "banks": "bank"
}

def tokens(text):
    return re.findall(r"[a-z']+", text.lower())

def none(text):
    return tokens(text)

def porter(text):
    return [ps.stem(t) for t in tokens(text)]

def lemma(text):
    return [
        LEMMA.get(re.sub(r"'s$", "", t), re.sub(r"'s$", "", t))
        for t in tokens(text)
    ]

print("Task 2 - Porter stems of the problem words")

for w in [
    "organization", "organizer", "organizing", "organized",
    "organization's", "organ", "organic", "organism"
]:
    print(f"{w:<16} -> {ps.stem(w)}")

print("\nTask 4 - Classifier comparison")

for name, f in [
    ("Without stemming", none),
    ("Porter stemming", porter),
    ("Lemmatization", lemma)
]:
    vec = CountVectorizer(analyzer=f)
    X = vec.fit_transform(docs)

    pred = cross_val_predict(
        MultinomialNB(),
        X,
        labels,
        cv=LeaveOneOut()
    )

    cm = confusion_matrix(labels, pred)

    print(
        f"{name:<17} vocabulary = {X.shape[1]:<3} "
        f"accuracy = {accuracy_score(labels, pred):.3f} "
        f"confusion matrix = {cm.tolist()}"
    )