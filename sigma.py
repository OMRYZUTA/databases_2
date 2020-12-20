from ex2_parser import R_attributes, S_attributes
from njoin import NJOIN
from conditionTree import cond_tree_node
import tables


class SIGMA:
    condition = None
    applies_to = None

    def __init__(self, condition, applies_to):
        self.condition = condition
        self.applies_to = applies_to

    def __str__(self):
        string = "SIGMA"
        string += "["+self.condition+"]"
        string += "("+self.applies_to+")"
        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def check_all_attributes_from(self, attribute_list):
        result = True
        all_cond_attributes = self.condition.get_all_atts_in_cond()
        for att in all_cond_attributes:
            result = result and (att in attribute_list)
        return result

    def get_type(self):
        return "SIGMA"

    def matches_11b(self):
        if(self.condition.data == "AND"):
            cond_att_list = self.condition.get_all_atts_in_cond()
            common_columns = {"R.D", "R.E", "S.D", "S.E"}
            result = True
            for att in common_columns:
                result = result and (att in cond_att_list)

            if (result):
                left_cond = self.condition.left
                right_cond = self.condition.right
                if(left_cond.data == "=" and right_cond.data == "="):
                    if(left_cond.are_different_tables() and right_cond.are_different_tables()):
                        if(left_cond.are_same_attributes() and right_cond.are_same_attributes()):
                            return True

        return False

    def matches_6(self):
        att_list = None

        if(self.applies_to.get_type() == "NJOIN"):
            njoin = self.applies_to
            if(njoin.scheme1 == 'R'):
                att_list = R_attributes
            elif(njoin.scheme1 == 'S'):
                att_list = S_attributes

            return self.check_all_attributes_from(att_list)

        return False

    def matches_6a(self):
        att_list = None

        if(self.applies_to.get_type() == "NJOIN"):
            njoin = self.applies_to
            if(njoin.scheme2 == 'R'):
                att_list = R_attributes
            elif(njoin.scheme2 == 'S'):
                att_list = S_attributes

            return self.check_all_attributes_from(att_list)

        return False

    def apply_rule(self, rule_type):
        if (rule_type == "4"):
            if (self.condition.data == "AND"):
                self.applies_to = SIGMA(self.condition.right, self.applies_to)
                self.condition = self.condition.left
                return self
        elif (rule_type == "4a"):
            # self.apply_rule("4") - in case Roy says we need to first apply rule 4 in order to apply 4a
            if(self.applies_to.get_type() == "SIGMA"):
                sigma = self.applies_to
                self.applies_to = sigma.applies_to
                sigma.applies_to = self
                return sigma  # return new outer-sigma
        elif (rule_type == "6"):
            if (self.matches_6()):
                njoin = self.applies_to
                self.applies_to = njoin.scheme1  # apply sigma to scheme1 alone
                njoin.scheme1 = self
                return njoin
        elif (rule_type == "6a"):
            if (self.matches_6a()):
                njoin = self.applies_to
                self.applies_to = njoin.scheme2  # apply sigma to scheme2 alone
                njoin.scheme2 = self
                return njoin
        elif (rule_type == "11b"):
            if(self.matches_11b()):
                cartesian = self.applies_to
                return NJOIN(cartesian.scheme1, cartesian.scheme2)

        # the default case
        self.applies_to = self.applies_to.apply_rule(rule_type)
        return self
# assumiing there's only one att per simple condition here

    def estimate_simple_condition_rows(self, i_before_num_of_rows):
        attribute_node = None

        if(self.condition.left.node_type == "ATTRIBUTE"):
            attribute_node = self.condition.left
        elif(self.condition.right.node_type == "ATTRIBUTE"):
            attribute_node = self.condition.right
        attribute = attribute_node.get_attribute_alone()
        table = attribute_node.get_attribute_table()
        range_of_attribute = tables.get_range_of_values(table, attribute)
        return int(i_before_num_of_rows / range_of_attribute)

    def estimate_size(self):
        before_num_of_rows = None
        after_num_of_rows = None
        size_of_row = None
        (before_num_of_rows, size_of_row) = tables.get_table_size(self.applies_to)
        if(before_num_of_rows == None and size_of_row == None):
            (before_num_of_rows, size_of_row) = self.applies_to.estimate_size()

        if(self.condition.data == "="):  # meaning it's a simple condition
            after_num_of_rows = self.estimate_simple_condition_rows(
                before_num_of_rows)
        else:
            pass

        msg = f"""
        SIGMA        
        input: n_scheme1={before_num_of_rows}  R_scheme1={size_of_row} 
        output: n_new_scheme={after_num_of_rows} R_new_scheme={size_of_row}
        """
        print(msg)
        return (after_num_of_rows, size_of_row)
