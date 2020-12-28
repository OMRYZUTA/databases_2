import unittest
from conditionTree import cond_tree_node
import ex2_solution
import njoin
import sigma
from algebric_expression import Algebric_Expression
from cartesian import CARTESIAN
import tables
from pi import PI

class TestTree(unittest.TestCase):

    def setUp(self):
        RpointD = cond_tree_node("R.D", "ATTRIBUTE")
        RpointA = cond_tree_node("R.A", "ATTRIBUTE")
        SpointD = cond_tree_node("S.D", "ATTRIBUTE")
        four = cond_tree_node("4", "INTEGER")
        five = cond_tree_node("5", "INTEGER")
        
        self.simple_tree_R_DGreater_4 = cond_tree_node(">", "REL_OP", RpointD, four)
        self.simple_tree_R_D_equal_4 = cond_tree_node("=", "REL_OP", RpointD, four)
        self.simple_tree_5_equal_4 = cond_tree_node("=", "REL_OP", five, four)
        self.simple_tree_4_4 = cond_tree_node("=", "REL_OP", four, four)
        self.simple_treeR_A_equal_4 = cond_tree_node("=", "REL_OP", RpointA, four)
        self.simple_tree_R_A_equal_R_D = cond_tree_node("=", "REL_OP", RpointA, RpointD)
        self.simple_tree_R_D_equal_S_D = cond_tree_node("=", "REL_OP", SpointD, RpointD)
        self.and_tree = cond_tree_node("AND", "LOGIC_OP", self.simple_tree_R_A_equal_R_D, self.simple_tree_R_D_equal_S_D)
        self.or_tree = cond_tree_node("OR", "LOGIC_OP", self.simple_tree_R_A_equal_R_D, self.simple_tree_R_D_equal_S_D)

        
        query_str= "SELECT R.A,R.B FROM R,S WHERE R.A=10 AND R.B>R.A ;"
        parsed_query = ex2_solution.ex2_parser.parse_query(query_str)
        (table_list, attribute_list, condition_tree) = parsed_query
        self.alg_expr1 = ex2_solution.build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)
        njoin1 = njoin.NJOIN("R","S")
        sigi1 =sigma.SIGMA(self.simple_tree_R_DGreater_4,njoin1)
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
        self.assertEqual(self.simple_tree_R_DGreater_4.data,">")   
        self.assertEqual(self.simple_tree_R_DGreater_4.left.data,"R.D")  
        self.assertEqual(self.simple_tree_R_DGreater_4.right.data,"4") 
    
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
          
    def test_cartesian_estimation(self):
        tables.fill_tables('statistics.txt')
        carti = CARTESIAN("R","S")
        (num_of_rows, size_of_row) = carti.estimate_size()
        self.assertEqual(num_of_rows, 20000)
        self.assertEqual(size_of_row, 40)

    def test_PI_estimation(self):
        tables.fill_tables('statistics.txt')
        carti = CARTESIAN("R","S")
        pipi=(PI(["R.A","R.B"],carti))
        (num_of_rows, size_of_row) =pipi.estimate_size()
        self.assertEqual(num_of_rows, 20000)
        self.assertEqual(size_of_row, 8)
    
    def test_esitmate_simple_tree(self):
        tables.fill_tables('statistics.txt')
        self.assertEqual(sigma.estimate_simple_condition_propability(self.simple_tree_R_D_equal_4),1.0)  
        self.assertEqual(sigma.estimate_simple_condition_propability(self.simple_tree_5_equal_4),0.0) 
        self.assertEqual(sigma.estimate_simple_condition_propability(self.simple_tree_4_4),1.0) 
        self.assertEqual(sigma.estimate_simple_condition_propability(self.simple_tree_R_A_equal_R_D),0.02) 
        self.assertEqual(sigma.estimate_simple_condition_propability(self.simple_tree_R_D_equal_S_D),0.01)

    def test_estimate_condition_rec(self): 
        self.assertEqual(sigma.estimate_condition_rec(self.and_tree),0.0002)
        self.assertEqual(sigma.estimate_condition_rec(self.or_tree), 0.02980000000000005)

if __name__ == "__main__":
    unittest.main()
