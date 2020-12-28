from ex2_parser import R_attributes, S_attributes
import tables

class PI:
    attribute_list = None
    applies_to = None

    
    def __init__(self, attribute_list, applies_to):
        self.attribute_list = attribute_list
        self.applies_to = applies_to

    
    def __str__(self):
        att_list_str = ",".join(self.attribute_list)
        string = "PI["+att_list_str+"]"
        string += "("+self.applies_to+")"

        return string

    
    def __add__(self, other):
        return str(self) + other

    
    def __radd__(self, other):
        return other + str(self)

    
    def get_type(self):
        return "PI"

    
    def matches_5a(self):
        if (self.applies_to.get_type() == "SIGMA"):
            sigma = self.applies_to
            return (sigma.check_all_cond_attributes_from(self.attribute_list))

        return False

    
    def apply_rule(self, rule_type):
        if (rule_type == "5a"):
            if (self.matches_5a()):
                sigma = self.applies_to
                self.applies_to = sigma.applies_to
                sigma.applies_to = self
                return sigma

        # the default case
        self.applies_to = self.applies_to.apply_rule(rule_type)
        return self
    
    
    def estimate_size(self):
        num_of_rows = None        
        before_size_of_row = None
        after_size_of_row = None

        (num_of_rows, before_size_of_row) = tables.get_table_size(self.applies_to)
        if(num_of_rows == None and before_size_of_row == None):
            (num_of_rows, before_size_of_row) = self.applies_to.estimate_size()
        
        #PI can only decrease previus number of attributes
        after_size_of_row = min(before_size_of_row, len(self.attribute_list) *tables.Table_R["att_size"])

        msg = f"""
        PI        
        input: n_scheme1={num_of_rows}  R_scheme1={before_size_of_row} 
        output: n_new_scheme={num_of_rows} R_new_scheme={after_size_of_row}
        """
        print(msg)
        return (num_of_rows, after_size_of_row)