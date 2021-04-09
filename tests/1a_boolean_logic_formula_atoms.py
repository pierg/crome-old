from typing import Set

from specification import NotSatisfiableException
from specification.formula import FormulaOutput
from specification.atom import Atom
from type.subtypes.locations import ReachLocation
from typeset import Typeset


class GoA(ReachLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name)


class GoB(ReachLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name)


class GoC(ReachLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name)


class GoD(ReachLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name)


a = GoA()
b = GoB()
c = GoC()
d = GoD()

a = Atom((a.name, Typeset({a})))
b = Atom((b.name, Typeset({b})))

c = Atom((c.name, Typeset({c})))
d = Atom((d.name, Typeset({d})))

test = a >> ~ a

print(test.formula(FormulaOutput.CNF)[0])
print(test.formula(FormulaOutput.DNF)[0])

one = a & b

print("\none")
print(one.formula(FormulaOutput.CNF)[0])
print(one.formula(FormulaOutput.DNF)[0])

one = ~ one

print("\nNOT one")
print(one.formula(FormulaOutput.CNF)[0])
print(one.formula(FormulaOutput.DNF)[0])

one = ~ one

print("\nNOT NOT one")
print(one.formula(FormulaOutput.CNF)[0])
print(one.formula(FormulaOutput.DNF)[0])

two = c | d

print("\ntwo")
print(two.formula(FormulaOutput.CNF)[0])
print(two.formula(FormulaOutput.DNF)[0])

three = one & two

print("\nthree")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])

four = one | two

three = ~three

print("\nNOT three")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])

three = ~three

print("\nNOT NOT three")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])

print("\nfour")
print(four.formula(FormulaOutput.CNF)[0])
print(four.formula(FormulaOutput.DNF)[0])

five = three & four

print("\nfive")
print(five.formula(FormulaOutput.CNF)[0])
print(five.formula(FormulaOutput.DNF)[0])

print(three.formula(FormulaOutput.CNF)[0])
print(four.formula(FormulaOutput.CNF)[0])

six = three | four

print("\nsix")
print(six.formula(FormulaOutput.CNF)[0])
print(six.formula(FormulaOutput.DNF)[0])

seven = five >> six

print("\nseven")
print(seven.formula(FormulaOutput.CNF)[0])
print(seven.formula(FormulaOutput.DNF)[0])


"""Let's change the variables adding mutex constraints"""



class GoA(ReachLocation):

    def __init__(self, name: str = "a"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoB(ReachLocation):

    def __init__(self, name: str = "b"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoC(ReachLocation):

    def __init__(self, name: str = "c"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "locations"


class GoD(ReachLocation):

    def __init__(self, name: str = "d"):
        super().__init__(name)

    @property
    def mutex_group(self) -> str:
        return "locations"


a = GoA()
b = GoB()
c = GoC()
d = GoD()

a = Atom((a.name, Typeset({a})))
b = Atom((b.name, Typeset({b})))

c = Atom((c.name, Typeset({c})))
d = Atom((d.name, Typeset({d})))

test = a >> ~ a

print(test.formula(FormulaOutput.CNF)[0])
print(test.formula(FormulaOutput.DNF)[0])

try:
    one = a & b
    print("\none")
    print(one.formula(FormulaOutput.CNF)[0])
    print(one.formula(FormulaOutput.DNF)[0])

    one = ~ one

    print("\nNOT one")
    print(one.formula(FormulaOutput.CNF)[0])
    print(one.formula(FormulaOutput.DNF)[0])

    one = ~ one

    print("\nNOT NOT one")
    print(one.formula(FormulaOutput.CNF)[0])
    print(one.formula(FormulaOutput.DNF)[0])
except NotSatisfiableException as e:
    print("Non satisfiable sin a & b = FALSE. However we raise an axception and do not allow FALSE propositions")

two = c | d

print("\ntwo")
print(two.formula(FormulaOutput.CNF)[0])
print(two.formula(FormulaOutput.DNF)[0])

three = a | two

print("\nthree")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])


three = ~three

print("\nNOT three")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])

three = ~three

print("\nNOT NOT three")
print(three.formula(FormulaOutput.CNF)[0])
print(three.formula(FormulaOutput.DNF)[0])

