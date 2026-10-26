import random

text = "I love Python I love programming Python is easy"
words = text.split()
bigrams = {}

for i in range(len(words) - 1):
    bigrams.setdefault(words[i], []).append(words[i + 1])

word = random.choice(words[:-1])
result = [word]

for i in range(10):
    if word not in bigrams:
        break
    word = random.choice(bigrams[word])
    result.append(word)

print(" ".join(result))
