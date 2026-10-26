import nltk
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("omw-1.4")

sentence = input("Enter a sentence: ")
word = input("Enter the word to disambiguate: ")

sense = lesk(word_tokenize(sentence), word)

if sense:
    print("Synset:", sense.name())
    print("Meaning:", sense.definition())
else:
    print("No sense found")
