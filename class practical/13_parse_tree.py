import nltk

grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> 'the' N
N -> 'cat' | 'dog'
VP -> V
V -> 'runs' | 'sleeps'
""")

parser = nltk.ChartParser(grammar)
sentence = "the cat runs".split()

for tree in parser.parse(sentence):
    print(tree)
    tree.pretty_print()
