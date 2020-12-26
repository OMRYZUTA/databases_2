import tables
from ex2_parser import R_attributes, S_attributes

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
            att_list =self.get_all_attributes_from_scheme(self.scheme1)+self.get_all_attributes_from_scheme(self.scheme2)
        elif(i_scheme == "scheme1"):
            att_list = self.get_all_attributes_from_scheme(self.scheme1)
        elif(i_scheme == "scheme2"):
            att_list = self.get_all_attributes_from_scheme(self.scheme2)      
           
        return att_list