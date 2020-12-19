from njoin import NJOIN
from conditionTree import cond_tree_node

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
   

    def is_NJOIN_condition(self):
        result = True
        cond_att_list = self.condition.get_all_atts_in_cond()                   
        common_columns = {"R.D","R.E","S.D","S.E" }
        for att in common_columns:
            result = result and (att in cond_att_list)

        if(self.condition.data=="AND" and result):
            lcs = self.condition.left
            rcs = self.condition.right
            if(lcs.data=="=" and rcs.data=="="):
               if(lcs.are_different_tables() and rcs.are_different_tables()):
                   if(lcs.are_same_attributes() and rcs.are_same_attributes()):
                       return True
        
        return False


    def apply_rule(self, rule_type):
        result = self
        if (rule_type == "5a"):
            self.applies_to.apply_rule(rule_type)
        elif(rule_type == "4"):
            if (self.condition.data == "AND"):
                self.applies_to = SIGMA(self.condition.right, self.applies_to)
                self.condition = self.condition.left
        elif(rule_type == "4a"):
            if(self.applies_to.get_type()=="SIGMA"):
                temp_condition_tree=self.applies_to.condition
                self.applies_to.condition= self.condition
                self.condition= temp_condition_tree
        elif(rule_type == "11b"):
            if(self.applies_to.get_type()=="CARTESIAN"):
                cartesian = self.applies_to
                if(is_NJOIN_condition(self.condition)):
                    #"SIGMA[p](CARTSIAN(R,S))=NJOIN[p](R,S)"
                    result = NJOIN(cartesian.scheme1, cartesian.scheme2) 

        return result
