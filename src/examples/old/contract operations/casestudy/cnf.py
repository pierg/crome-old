from custom_world import CustomWorld

w = CustomWorld()

w["r1"] | w["r2"]

# original = Node(name="strict_patrolling",
#                 description="strict order patrolling regions r1 -> r2",
#                 specification=Contract(
#                     assumptions=GF(w["picture"]),
#                     guarantees=StrictOrderedPatrolling([w["r1"], w["r2"], w["r5"]])),
#                 world=w)
"""Contract
    A: TRUE
    G: G(F(r1 & F(r2))) & (!(r2) U r1) & G(((r2) -> (X((!(r2) U r1))))) & G(((r1) -> (X((!(r1) U r2)))))
"""

# print(original)
