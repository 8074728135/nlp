def dfa(s):
    state = "q0"
    path = [state]

    for ch in s:

        if state == "q0":
            if ch == "a":
                state = "q1"
            else:
                state = "q0"

        elif state == "q1":
            if ch == "a":
                state = "q1"
            else:
                state = "q2"

        elif state == "q2":
            if ch == "a":
                state = "q1"
            else:
                state = "q0"

        path.append(state)

    print("Transition Path:")
    print(" -> ".join(path))

    if state == "q2":
        print("Accepted")
    else:
        print("Rejected")


s = input("Enter string: ")

dfa(s)
