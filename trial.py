from ex2_solution import optimization_rules
from cartesian import CARTESIAN

expr=CARTESIAN("R","S")
print(CARTESIAN)
(n,r)=expr.estimate_size()
print(n,r)