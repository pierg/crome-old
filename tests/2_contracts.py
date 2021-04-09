from contract import Contract
from contract.exceptions import ContractException
from specification.atom.pattern.basic import Init
from worlds.simple_gridworld import SimpleGridWorld, SeA, SeB, GoA, GoB

sw = SimpleGridWorld()

t = sw.typeset

"""We are using the Init pattern which is basically atom corresponding to the type at time zero, 
    e.g. type: a => atom: a"""

c1 = Contract(assumptions=Init(t["se_a"]), guarantees=Init(t["a"]))
print(c1)

c2 = Contract(assumptions=Init(t["se_b"]), guarantees=Init(t["b"]))
print(c2)

try:
    c12 = Contract.composition({c1, c2})
    print(c12)
except ContractException as e:
    print(e.message)
    print("Unsatisfiable because se_a and se_b are mutually exclusive")

"""We can compute the conjunction"""

try:
    c12 = Contract.conjunction({c1, c2})
    print(c12)
    print("Conjunction is OK")
except ContractException as e:
    print(e.message)

"""Let's change the assumptions to be not mutually exclusive"""


class SeAMod(SeA):

    @property
    def mutex_group(self) -> str:
        return ""


class SeBMod(SeB):

    @property
    def mutex_group(self) -> str:
        return ""


new_se_a = SeAMod()
new_se_b = SeBMod()

c1 = Contract(assumptions=Init(new_se_a), guarantees=Init(t["a"]))
print(c1)

c2 = Contract(assumptions=Init(new_se_b), guarantees=Init(t["b"]))
print(c2)

try:
    c12 = Contract.composition({c1, c2})
    print(c12)
except ContractException as e:
    print(e.message)
    print("Unfeasible because a and b are mutually exclusive")

"""Let's change the guarantees to be not mutually exclusive"""


class GoAMod(GoA):

    @property
    def mutex_group(self) -> str:
        return ""


class GoBMod(GoB):

    @property
    def mutex_group(self) -> str:
        return ""


new_go_a = GoAMod()
new_go_b = GoBMod()

c1 = Contract(assumptions=Init(new_se_a), guarantees=Init(new_go_a))
print(c1)

c2 = Contract(assumptions=Init(new_se_b), guarantees=Init(new_go_b))
print(c2)

try:
    c12_comp = Contract.composition({c1, c2})
    print(c12_comp)
    print("Composition successful!")
except ContractException as e:
    print(e.message)

