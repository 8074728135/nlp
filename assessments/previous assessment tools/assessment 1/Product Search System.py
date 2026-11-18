import re

products = [
    "Apple iPhone 15",
    "Samsung Galaxy S24",
    "Apple MacBook Air",
    "Dell Laptop",
    "HP Pavilion",
    "Samsung Galaxy Book",
    "OnePlus Phone"
]

keyword = input("Enter search keyword: ")

# Exact search
exact = [
    p for p in products
    if re.search(r"\b" + re.escape(keyword) + r"\b", p, re.I)
]

# Prefix search
prefix = [
    p for p in products
    if re.search(r"\b" + re.escape(keyword), p, re.I)
]

# Suffix search
suffix = [
    p for p in products
    if re.search(re.escape(keyword) + r"\b", p, re.I)
]

# Partial search
partial = [
    p for p in products
    if re.search(re.escape(keyword), p, re.I)
]

print("\nExact Matches:", exact)
print("Total:", len(exact))

print("\nPrefix Matches:", prefix)
print("Total:", len(prefix))

print("\nSuffix Matches:", suffix)
print("Total:", len(suffix))

print("\nPartial Matches:", partial)
print("Total:", len(partial))
