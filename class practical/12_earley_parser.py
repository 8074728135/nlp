import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> 'the' N
N -> 'cat' | 'dog'
VP -> 'runs' | 'sleeps'
""")

parser = nltk.EarleyChartParser(grammar)
sentence = "the cat runs".split()

for tree in parser.parse(sentence):
    print(tree)
