from core.patterns.robotics.coremovement.coverage import OrderedVisit, Visit
from core.patterns.robotics.coremovement.surveillance import (
    OrderedPatrolling,
    Patrolling,
)
from tools.strings import StringMng

print("\n\n")
print(StringMng.latexit(str(Patrolling("l1", "l5"))))
print(StringMng.latexit(str(Patrolling("l3"))))


print("\n\n")
print(OrderedPatrolling("l1", "l3", "l5"))
print(StringMng.latexit("G(F(l1 & F(l3 & F(l5))))"))
print(StringMng.latexit("(!(l3) U l1) & (!(l5) U l3)"))
print(StringMng.latexit("G(((l3) -> (X((!(l3) U l1)))))"))
print(StringMng.latexit("G(((l5) -> (X((!(l5) U l3)))))"))
print(StringMng.latexit("G(((l1) -> (X((!(l1) U l5)))))"))

print("\n\n")
print(OrderedVisit("l1", "l3", "l5", "l4", "l2"))


print("\n\n\n")

print(StringMng.latexit(str(Patrolling("l1", "l5"))))
print(StringMng.latexit(str(Patrolling("l3"))))
print(StringMng.latexit(str(Visit("l3", "l1"))))
print(StringMng.latexit(str(Visit("l5"))))
