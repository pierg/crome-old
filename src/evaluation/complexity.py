import math

lamda = 3
tetha = 4
comps = 10
N = 4

c1 = 0
for c in range(N):
    c1 += math.comb(comps, c)

c1 *= tetha
print(f"c1={c1}")

c2 = 0
for c in range(N):
    if c2 == 0:
        c2 += math.comb(comps, c)
    else:
        c2 *= math.comb(comps, c)

print(f"c2={c2}")

c3 = 0
for c in range(lamda - 1):
    c3 += math.comb(lamda, c)

c3 = c3 ** 4
print(f"c3={c3}")

print(f"final={c1*c2*c3}")
