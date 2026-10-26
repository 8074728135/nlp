import nltk

patterns = [
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*ly$', 'RB'),
    (r'.*ous$', 'JJ'),
    (r'.*', 'NN')
]

text = "The cat is running quickly"
words = nltk.word_tokenize(text)

tagger = nltk.RegexpTagger(patterns)
print(tagger.tag(words))
