import ex2
import unittest

class TestConditionTree(unittest.TestCase):
    
    def test_parse_condition_tree(self):   
        self.assertEqual(ex2.decipher_condition_tree("S.D >4").data, "S.D >4")
        complicated_result = ex2.decipher_condition_tree("S.D >4 AND R.A = 10")
        self.assertEqual(complicated_result.data, "AND")
        self.assertEqual(complicated_result.left.data, "S.D >4")
        self.assertEqual(complicated_result.right.data, "R.A = 10")






if __name__ == "__main__":
    unittest.main()
