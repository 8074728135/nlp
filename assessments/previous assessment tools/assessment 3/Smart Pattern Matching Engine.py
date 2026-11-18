import re

text = """
Meeting on 12/09/2026
Call 9876543210
#NLP
@OpenAI
natural language processing
"""

print("1. Search Date")
print("2. Search Phone Number")
print("3. Search Hashtag")
print("4. Search Mention")
print("5. Search Prefix")
print("6. Search Suffix")

choice = input("Enter choice: ")

if choice == "1":
    result = re.findall(
        r"\b\d{2}/\d{2}/\d{4}\b",
        text
    )

elif choice == "2":
    result = re.findall(
        r"\b[6-9]\d{9}\b",
        text
    )

elif choice == "3":
    result = re.findall(
        r"#\w+",
        text
    )

elif choice == "4":
    result = re.findall(
        r"@\w+",
        text
    )

elif choice == "5":
    word = input("Enter prefix: ")

    result = re.findall(
        r"\b" + re.escape(word) + r"\w*",
        text,
        re.I
    )

elif choice == "6":
    word = input("Enter suffix: ")

    result = re.findall(
        r"\w*" + re.escape(word) + r"\b",
        text,
        re.I
    )

else:
    result = []

print("\nMatching Patterns:")

for x in result:
    print(x)
