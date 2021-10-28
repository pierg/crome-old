from core.contract import Contract
from core.type import Boolean

a1 = Boolean("a1").to_atom()
g1 = Boolean("g1").to_atom()
c1 = Contract(assumptions=a1, guarantees=g1)

a = Boolean("a").to_atom()
g = Boolean("g").to_atom()
c = Contract(assumptions=a, guarantees=g)

c2 = Contract.quotient(c, c1)

comp = Contract.composition({c1, c2})

print(c1)
print(c2)
print(c)
print(comp)


print(comp <= c)

