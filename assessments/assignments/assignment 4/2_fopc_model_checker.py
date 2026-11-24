"""CO4 Task 2 - First-order logic over a finite model: evaluate formulas, countermodels, tiny KB."""

class Model:
    def __init__(self, domain, **preds):
        self.D = set(domain)
        self.P = {k: set(v) for k, v in preds.items()}   # unary: {x}, binary: {(x,y)}
    def holds(self, name, *args):
        return (args[0] if len(args) == 1 else args) in self.P.get(name, set())

# ---------- University vocabulary (Part I Task 2) ----------
def stmt_i(m):    # forall x [Student(x) -> exists c (Course(c) & Enrolled(x,c))]
    return all((not m.holds("Student", x)) or any(m.holds("Course", c) and m.holds("Enrolled", x, c) for c in m.D) for x in m.D)

def stmt_i_reversed(m):   # exists c forall x [Student(x) -> Enrolled(x,c)]
    return any(all((not m.holds("Student", x)) or m.holds("Enrolled", x, c) for x in m.D) for c in m.D)

def stmt_ii(m):   # exists x [Student(x) & forall c ((Course(c) & Teaches(drRao,c)) -> Passed(x,c))]
    return any(m.holds("Student", x) and all(not (m.holds("Course", c) and m.holds("Teaches", "drRao", c)) or m.holds("Passed", x, c) for c in m.D) for x in m.D)

def stmt_iii(m):  # forall i [Instructor(i) -> exists c (Course(c) & ~Teaches(i,c))]
    return all((not m.holds("Instructor", i)) or any(m.holds("Course", c) and not m.holds("Teaches", i, c) for c in m.D) for i in m.D)

def every_student_passed_nlp(m):  return all((not m.holds("Student", x)) or m.holds("Passed", x, "NLP") for x in m.D)
def some_student_not_passed_nlp(m): return any(m.holds("Student", x) and not m.holds("Passed", x, "NLP") for x in m.D)

# ---------- Course-platform vocabulary (Part II Task 2) ----------
def p_stmt_i(m):   # enrolled in NLP -> completed at least one prerequisite of NLP
    return all(not (m.holds("Learner", x) and m.holds("Enrolled", x, "NLP")) or
               any(m.holds("Course", p) and m.holds("Prerequisite", p, "NLP") and m.holds("Completed", x, p) for p in m.D) for x in m.D)

def p_stmt_ii(m):  # some learner completed every course offered by the department
    return any(m.holds("Learner", x) and all(not (m.holds("Course", c) and m.holds("OfferedBy", c, "Department")) or m.holds("Completed", x, c) for c in m.D) for x in m.D)

def p_stmt_iii(m): # no learner completed a course they were not enrolled in
    return all(not (m.holds("Learner", x) and m.holds("Course", c) and m.holds("Completed", x, c)) or m.holds("Enrolled", x, c) for x in m.D for c in m.D)

# ---------- Tiny knowledge base with forward chaining ----------
def forward_chain(facts):
    """Rule: Completed(x,c) -> Enrolled(x,c). Returns closure of facts."""
    facts = set(facts)
    changed = True
    while changed:
        changed = False
        for f in list(facts):
            if f[0] == "Completed":
                new = ("Enrolled", f[1], f[2])
                if new not in facts:
                    facts.add(new); changed = True
    return facts

if __name__ == "__main__":
    # Countermodel from the assignment: S1 only in C1, S2 only in C2
    m = Model({"S1", "S2", "C1", "C2"},
              Student={"S1", "S2"}, Course={"C1", "C2"},
              Enrolled={("S1", "C1"), ("S2", "C2")})
    print("forall x exists c Enrolled        :", stmt_i(m))
    print("exists c forall x Enrolled (rev.) :", stmt_i_reversed(m), "<- countermodel: not equivalent")

    m2 = Model({"drRao", "A", "B", "NLP", "AI"},
               Student={"A", "B"}, Course={"NLP", "AI"}, Instructor={"drRao"},
               Teaches={("drRao", "NLP")}, Passed={("A", "NLP")})
    print("(ii) some student passed all Rao courses:", stmt_ii(m2))
    print("(iii) no instructor teaches every course :", stmt_iii(m2))
    print("Every student passed NLP / some student did not:", every_student_passed_nlp(m2), some_student_not_passed_nlp(m2),
          "-> they can never both be True")

    m3 = Model({"Ana", "Bo", "NLP", "Logic", "Department"},
               Learner={"Ana", "Bo"}, Course={"NLP", "Logic"},
               OfferedBy={("NLP", "Department"), ("Logic", "Department")},
               Prerequisite={("Logic", "NLP")}, Enrolled={("Ana", "NLP"), ("Ana", "Logic"), ("Bo", "NLP")},
               Completed={("Ana", "Logic"), ("Ana", "NLP")})
    print("\nPlatform (i)  :", p_stmt_i(m3), "(Bo is enrolled in NLP but completed no prerequisite)")
    print("Platform (ii) :", p_stmt_ii(m3))
    print("Platform (iii):", p_stmt_iii(m3))

    kb = forward_chain({("Learner", "Ana"), ("Course", "NLP"), ("Completed", "Ana", "NLP")})
    print("\nKB query Enrolled(Ana,NLP):", ("Enrolled", "Ana", "NLP") in kb)
    print("KB query Enrolled(Ana,Logic):", ("Enrolled", "Ana", "Logic") in kb, "(unknown -> not derivable)")
