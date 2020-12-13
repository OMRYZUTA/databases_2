import ex2
import unittest


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.simple_tree1=ex2.CondTreeNode()
        self.simple_tree1.data ="R.D>4"
        self.empty_parse_tree =([], [], ex2.CondTreeNode())

    def test_parse_condition_tree(self):   
        self.assertEqual(ex2.decipher_condition_tree("S.D >4").data, "S.D >4")
        complicated_result = ex2.decipher_condition_tree("S.D >4 AND R.A = 10")
        self.assertEqual(complicated_result.data, "AND")
        self.assertEqual(complicated_result.left.data, "S.D >4")
        self.assertEqual(complicated_result.right.data, "R.A = 10")

    
    def test_algebric_expression(self):
        self.assertEqual(ex2.convert_algebric_expression([],[], ex2.CondTreeNode()),"PI[](SIGMA[](CARTESIAN()))")

        

        self.assertEqual(ex2.convert_algebric_expression(["R","S"],["R.D","S.E"],self.simple_tree1),"PI[R.D,S.E](SIGMA[R.D>4](CARTESIAN(R,S)))")





if __name__ == "__main__":
    unittest.main()
