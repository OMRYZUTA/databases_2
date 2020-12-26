import unittest
from conditionTree import cond_tree_node
import ex2_solution
import njoin
import sigma
from algebric_expression import Algebric_Expression

class TestTree(unittest.TestCase):

    def setUp(self):
        RpointD = cond_tree_node("R.D", "ATTRIBUTE")
        four = cond_tree_node("4", "INTEGER")
        self.simple_tree1 = cond_tree_node(">", "REL_OP", RpointD, four)
        query_str= "SELECT R.A,R.B FROM R,S WHERE R.A=10 AND R.B>R.A ;"
        parsed_query = ex2_solution.ex2_parser.parse_query(query_str)
        (table_list, attribute_list, condition_tree) = parsed_query
        self.alg_expr1 = ex2_solution.build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)
        njoin1 = njoin.NJOIN("R","S")
        sigi1 =sigma.SIGMA(self.simple_tree1,njoin1)
        self.alg_expr_rule6 =Algebric_Expression(sigi1)
        SpointD = cond_tree_node("S.D", "ATTRIBUTE")
        four = cond_tree_node("4", "INTEGER")
        simple_tree1 = cond_tree_node(">", "REL_OP", SpointD, four)

        njoin2 = njoin.NJOIN("R", "S")
        sigi2 = sigma.SIGMA(simple_tree1, njoin2)
        self.alg_expr_rule6a = Algebric_Expression(sigi2)
        
      

    def test_parse_tree(self):
        RpointD = cond_tree_node("R.D", "ATTRIBUTE")
        self.assertEqual(RpointD.data, "R.D")
        self.assertEqual(self.simple_tree1.data,">")   
        self.assertEqual(self.simple_tree1.left.data,"R.D")  
        self.assertEqual(self.simple_tree1.right.data,"4") 
    
    def test_algebric_expression_to_str(self):
        self.assertEqual("PI[R.A,R.B](SIGMA[((R.A=10)AND(R.B>R.A))](CARTESIAN(R,S)))",self.alg_expr1.__str__())

    def test_rule_6(self):
        self.alg_expr_rule6.apply_rule("6")
        self.assertEqual(self.alg_expr_rule6.__str__(),"NJOIN(SIGMA[(R.D>4)](R),S)")
        self.alg_expr1.apply_rule("6")
        self.assertEqual(self.alg_expr1.__str__(),"PI[R.A,R.B](CARTESIAN(SIGMA[((R.A=10)AND(R.B>R.A))](R),S))")
        query_str= "SELECT R.A,R.B FROM R,S WHERE R.A=10 AND R.B>S.E ;"
        parsed_query = ex2_solution.ex2_parser.parse_query(query_str)
        (table_list, attribute_list, condition_tree) = parsed_query
        self.alg_expr3 = ex2_solution.build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)
        self.alg_expr3.apply_rule("6")
        self.assertEqual(self.alg_expr3.__str__(),"PI[R.A,R.B](SIGMA[((R.A=10)AND(R.B>S.E))](CARTESIAN(R,S)))")
        

    def test_rule_6a(self):
        self.alg_expr_rule6a.apply_rule("6a")
        self.assertEqual(self.alg_expr_rule6a.__str__(),"NJOIN(R,SIGMA[(S.D>4)](S))")
        query_str= "SELECT R.A,R.B FROM R,S WHERE S.E=10 AND S.D>S.F ;"
        parsed_query = ex2_solution.ex2_parser.parse_query(query_str)
        (table_list, attribute_list, condition_tree) = parsed_query
        self.alg_expr4 = ex2_solution.build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)
        self.alg_expr4.apply_rule("6a")
        self.assertEqual(self.alg_expr4.__str__(),"PI[R.A,R.B](CARTESIAN(R,SIGMA[((S.E=10)AND(S.D>S.F))](S)))")        


if __name__ == "__main__":
    unittest.main()
