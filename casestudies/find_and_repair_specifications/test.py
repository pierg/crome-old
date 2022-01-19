import spot

original = "((((TRUE & TRUE) & TRUE) | !(((TRUE -> ( G ( F l1) &  G ( F l5))) & (TRUE -> ( F l3 &  F l1))) & (TRUE ->  G ( F l3)))) & (((TRUE -> ( G ( F l1) &  G ( F l5))) & (TRUE -> ( F l3 &  F l1))) & (TRUE ->  G ( F l3)))) &  G ((((l5 & !l1) & !l3) | ((l1 & !l5) & !l3)) | ((l3 & !l5) & !l1))"


s = spot.formula(original)
print(s)


s = s.simplify()
print(s)
