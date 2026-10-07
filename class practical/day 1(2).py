def fsa(s):
    state = 0

    for ch in s:
        if state == 0 and ch == 'a':
            state = 1
        elif state == 1 and ch == 'b':
            state = 2
        elif ch == 'a':
            state = 1
        else:
            state = 0

    return state == 2


s = input("Enter a string: ")

if fsa(s):
    print("Accepted")
else:
    print("Rejected")
