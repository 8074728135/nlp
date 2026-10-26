import nltk

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

text = "The cat is sitting on the mat"
words = nltk.word_tokenize(text)
tags = nltk.pos_tag(words)

print(tags)
