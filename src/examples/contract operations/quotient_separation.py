from core.contract import Contract
from core.type import Boolean

x = Boolean("x").to_atom()
y = Boolean("y").to_atom()
z = Boolean("z").to_atom()

c1 = Contract(guarantees=x)
print(f"Contract c1:\n{c1}")

c = Contract(assumptions=z, guarantees=y)
print(f"Contract c:\n{c}")

assert not (c <= c1)
print(f"c is not a refinement of c1")

print(f"we compute the separation of c1 from c, i.e. c2")
c2 = Contract.separation(c, c1)
print(f"Contract c2:\n{c2}")

print(f"we merge the result to c1")
merger = Contract.merging({c1, c2})
print(f"Contract merger:\n{merger}")

assert (c <= merger)
print(f"now c is a refinement of merger = c1 * c2")
