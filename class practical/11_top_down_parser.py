import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> 'the' 'cat' | 'the' 'dog'
VP -> 'runs' | 'sleeps'
""")

parser = nltk.ChartParser(grammar)
sentence = "the cat runs".split()

for tree in parser.parse(sentence):
    print(tree)
