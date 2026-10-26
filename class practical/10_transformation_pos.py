import nltk

text = "The cat is running"
words = nltk.word_tokenize(text)

tags = [(word, 'NN') for word in words]

for i, (word, tag) in enumerate(tags):
    if word.lower() in ['the', 'a', 'an']:
        tags[i] = (word, 'DT')
    elif word.lower() in ['is', 'am', 'are']:
        tags[i] = (word, 'VBZ')
    elif word.endswith('ing'):
        tags[i] = (word, 'VBG')

print(tags)
