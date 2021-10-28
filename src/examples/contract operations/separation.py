from core.contract import Contract
from core.type import Boolean

p1 = Boolean("p1").to_atom()
p2 = Boolean("p2").to_atom()
p3 = Boolean("p3").to_atom()
p4 = Boolean("p4").to_atom()
p5 = Boolean("p5").to_atom()
q = Boolean("q").to_atom()

c1 = Contract(assumptions=p1, guarantees=p3)

c = Contract(assumptions=p1 & p2, guarantees=p4)

# assert (c1 <= c)

c2 = Contract.quotient(c, c1)

comp = Contract.composition({c1, c2})

assert (comp <= c)

print(c)
print(c1)
print(c2)
print(comp)
