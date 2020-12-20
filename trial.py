from ex2_solution import optimization_rules
from cartesian import CARTESIAN
from sigma import SIGMA
from conditionTree import cond_tree_node

left = cond_tree_node("R.A","ATTRIBUTE")
right= cond_tree_node("10","INTEGER")
cond = cond_tree_node("=","REL_OP",left,right)
sigi =SIGMA(cond,CARTESIAN("R","S"))
print(sigi)
sigi.estimate_size()
# expr=CARTESIAN("R","S")
# print(CARTESIAN)
# (n,r)=expr.estimate_size()
# print(n,r)