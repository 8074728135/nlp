from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "Python is a programming language",
    "Natural language processing uses machine learning",
    "Python is useful for data science",
    "Machine learning can process text"
]

query = input("Enter search query: ")

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(documents + [query])
scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
ranking = scores.argsort()[::-1]

for index in ranking:
    print(f"Score: {scores[index]:.3f} - {documents[index]}")
