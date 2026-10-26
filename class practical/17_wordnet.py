import nltk
from nltk.corpus import wordnet

nltk.download("wordnet")
nltk.download("omw-1.4")

word = input("Enter a word: ")
synsets = wordnet.synsets(word)

for synset in synsets:
    print("Synset:", synset.name())
    print("Meaning:", synset.definition())
    print("Examples:", synset.examples())
    print()
