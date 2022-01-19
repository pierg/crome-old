from casestudies.find_and_repair_specifications.goals import w
from core.cgg import Node
from core.contract import Contract
from core.patterns.robotics.trigger import InstantaneousReaction, PromptReaction
from core.specification import Specification
from core.specification.lformula import LTL
from tools.strings import StringMng

g = Node(
    name="day_wave",
    description="During the day wave when seeing a person",
    specification=Contract(
        assumptions=None,
        guarantees=LTL(InstantaneousReaction("ps", "pc"), w.typeset),
    ),
    world=w,
)

print(f"INITIAL GOAL:\n{g}")

l1 = Node(
    name="lib_goal",
    description="During the day wave when seeing a person after one step",
    specification=Contract(
        assumptions=None, guarantees=LTL(PromptReaction("ps", "pc"), w.typeset)
    ),
    world=w,
)

print(f"LIBRARY GOAL:\n{l1}")

assert not l1 <= g
print(l1 <= g)

sep = Node.separation(l1, g)
print(f"SEPARATION:\n{sep}")
print(StringMng.latexit(sep.specification.assumptions))
print(StringMng.latexit(sep.specification.guarantees))

new = Node.merging({g, sep})
print(f"MERGING RES:\n{new}")
print(StringMng.latexit(new.specification.assumptions))
print(StringMng.latexit(new.specification.guarantees))

print("\n\n")
print(l1)
print("REFINES")
print(new)
print(l1 <= new)

print(new.specification.guarantees.represent(Specification.OutputStr.SUMMARY))
