import nltk

grammar = nltk.PCFG.fromstring("""
S -> NP VP [1.0]
NP -> 'the' N [0.6] | 'a' N [0.4]
N -> 'cat' [0.5] | 'dog' [0.5]
VP -> V [1.0]
V -> 'runs' [0.7] | 'sleeps' [0.3]
""")

parser = nltk.ViterbiParser(grammar)
sentence = "the cat runs".split()

for tree in parser.parse(sentence):
    print(tree)
    print("Probability:", tree.prob())
