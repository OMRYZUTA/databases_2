from ex2_solution import optimization_rules
from cartesian import CARTESIAN
from sigma import SIGMA
from conditionTree import cond_tree_node
#S.D=4 AND R.A=10
left1 = cond_tree_node("R.A","ATTRIBUTE")
right1= cond_tree_node("10","INTEGER")
simp_cond1 = cond_tree_node("=","REL_OP",left1,right1)

left2 = cond_tree_node("S.D","ATTRIBUTE")
right2= cond_tree_node("4","INTEGER")
simp_cond2 = cond_tree_node("=","REL_OP",left2,right2)
cond = cond_tree_node("AND","LOGIC_OP",simp_cond1,simp_cond2)
sigi =SIGMA(cond,CARTESIAN("R","S"))
print(sigi)
sigi.estimate_size()
# expr=CARTESIAN("R","S")
# print(CARTESIAN)
# (n,r)=expr.estimate_size()
# print(n,r)