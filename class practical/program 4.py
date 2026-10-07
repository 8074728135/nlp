def plural(word):
    if word.endswith(("s", "sh", "ch", "x", "o")):
        return word + "es"
    else:
        return word + "s"

words = ["cat", "dog", "box", "bus"]

for word in words:
    print(word, "->", plural(word))
