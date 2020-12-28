import tables
from ex2_parser import R_attributes, S_attributes
from conditionTree import cond_tree_node
import sigma
class NJOIN:
    scheme1 = None
    scheme2 = None
    applies_to = None

    def __init__(self, scheme1, scheme2):
        self.scheme1 = scheme1
        self.scheme2 = scheme2

    def __str__(self):
        string = "NJOIN"
        string += "("+self.scheme1+","+self.scheme2+")"

        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def get_type(self):
        return "NJOIN"

    def apply_rule(self, rule_type):
        return self

    def get_all_attributes_from_scheme(self, i_scheme):
        if(i_scheme == 'R'):
            att_list = R_attributes
        elif(i_scheme == 'S'):
            att_list = S_attributes
        else:
            att_list = i_scheme.get_all_attributes()

        return att_list

    def get_all_attributes(self, i_scheme=None):
        att_list = None

        if(i_scheme == None):
            att_list = self.get_all_attributes_from_scheme(
                self.scheme1)+self.get_all_attributes_from_scheme(self.scheme2)
        elif(i_scheme == "scheme1"):
            att_list = self.get_all_attributes_from_scheme(self.scheme1)
        elif(i_scheme == "scheme2"):
            att_list = self.get_all_attributes_from_scheme(self.scheme2)

        return att_list

    

    def estimate_size(self):
        num_of_rows = None
        size_of_row = None

        (num_of_rows_1, size_of_row_1) = tables.get_table_size(self.scheme1)
        (num_of_rows_2, size_of_row_2) = tables.get_table_size(self.scheme2)

        if(num_of_rows_1 == None and size_of_row_1 == None):
            (num_of_rows_1, size_of_row_1) = self.scheme1.estimate_size()
        if(num_of_rows_2 == None and size_of_row_2 == None):
            (num_of_rows_2, size_of_row_2) = self.scheme2.estimate_size()

        num_of_rows = num_of_rows_1*num_of_rows_2
        num_of_rows = esitmate_njoin_rows(num_of_rows)
        size_of_row = size_of_row_1+size_of_row_2- 2*tables.Table_R["att_size"]

        msg = f"""
        NJOIN        
        input: n_scheme1={num_of_rows_1} n_scheme2={num_of_rows_2} R_scheme1={size_of_row_1} R_scheme2={size_of_row_2}
        output: n_new_scheme={num_of_rows} R_new_scheme={size_of_row}
        """
        print(msg)
        return (num_of_rows, size_of_row)


def esitmate_njoin_rows(i_num_of_rows):
    #building the njoin condition
    RD = cond_tree_node("R.D", "ATTRIBUTE")
    SD = cond_tree_node("S.D", "ATTRIBUTE")
    RE = cond_tree_node("R.E", "ATTRIBUTE")
    SE = cond_tree_node("S.E", "ATTRIBUTE")
      
    simp_cond_1 = cond_tree_node("=", "REL_OP", RD, SD)
    simp_cond_2 = cond_tree_node("=", "REL_OP", RE, SE)
    and_cond = cond_tree_node("AND","LOGIC_OP",simp_cond_1,simp_cond_2)
    propablity = sigma.estimate_condition_rec(and_cond)
    return int(propablity*i_num_of_rows)