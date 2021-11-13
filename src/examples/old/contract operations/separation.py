from core.contract import Contract
from core.type import Boolean

p1 = Boolean("p1").to_atom()
p2 = Boolean("p2").to_atom()
p3 = Boolean("p3").to_atom()
p4 = Boolean("p4").to_atom()

c1 = Contract(assumptions=p4 & p3, guarantees=p1 & p2)
print(f"Contract c1:\n{c1}")

c = Contract(assumptions=p4, guarantees=p2)
print(f"Contract c:\n{c}")

assert not (c <= c1)
print(f"c is not a refinement of c1")

print(f"we compute the separation of c1 from c, i.e. c2")
c2 = Contract.separation(c, c1)
print(f"Contract c2:\n{c2}")

print(f"we merge the result to c1")
merger = Contract.merging({c1, c2})
print(f"Contract merger:\n{merger}")

assert c <= merger
print(f"now c is a refinement of merger = c1 * c2")
