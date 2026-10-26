import nltk

grammar = nltk.CFG.fromstring("""
S -> NP_SG VP_SG | NP_PL VP_PL
NP_SG -> 'the' 'cat' | 'the' 'dog'
NP_PL -> 'the' 'cats' | 'the' 'dogs'
VP_SG -> 'runs' | 'sleeps'
VP_PL -> 'run' | 'sleep'
""")

parser = nltk.ChartParser(grammar)
sentence = input("Enter a sentence: ").lower().split()

try:
    next(parser.parse(sentence))
    print("Sentence is grammatically valid")
except StopIteration:
    print("Sentence has incorrect agreement or grammar")
