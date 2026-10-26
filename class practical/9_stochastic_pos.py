import random

words = {
    "I": ["PRON"],
    "love": ["VERB"],
    "Python": ["NOUN"],
    "the": ["DET"],
    "cat": ["NOUN"],
    "runs": ["VERB"]
}

text = "I love Python"
tokens = text.split()

for word in tokens:
    tag = random.choice(words.get(word, ["NOUN"]))
    print(word, tag)
