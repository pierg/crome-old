import spot

from core.patterns.robotics.coremovement.surveillance import OrderedPatrolling
from tools.strings import StringMng

# a_s = "G(ps -> pc) | !(G(ps -> Xpc) & GFps)"
# g_s = "G(ps -> Xpc) & GFps"
#
# print(StringMng.latexit(a_s))
# print(StringMng.latexit(g_s))
#
#
# a_m = "GFps & (G(ps -> pc) | !(G(ps -> Xpc) & GFps))"
# g_m = "(G(ps -> Xpc) & GFps & (GFps -> G(ps -> pc))) | !(GFps & (G(ps -> pc) | !(G(ps -> Xpc) & GFps)))"
#
# print("/n/n")
#
# print(StringMng.latexit(a_m))
# print(StringMng.latexit(g_m))

spec = OrderedPatrolling("r1", "r2")

print(StringMng.latexit(str(spec)))