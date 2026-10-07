from nltk.stem import PorterStemmer

ps = PorterStemmer()

words = ["playing", "played", "player", "studies", "studying"]

for word in words:
    print(word, "->", ps.stem(word))
