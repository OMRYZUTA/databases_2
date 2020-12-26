import tables
from ex2_parser import R_attributes, S_attributes


class CARTESIAN:
    scheme1 = None
    scheme2 = None
    applies_to = None

    def __init__(self, scheme1, scheme2):
        self.scheme1 = scheme1
        self.scheme2 = scheme2

    def __str__(self):
        string = "CARTESIAN"
        string += "("+self.scheme1+","+self.scheme2+")"

        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def get_type(self):
        return "CARTESIAN"

    def apply_rule(self, rule_type):
        return self

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
        size_of_row = size_of_row_1+size_of_row_2

        msg = f"""
        CARTESIAN        
        input: n_scheme1={num_of_rows_1} n_scheme2={num_of_rows_2} R_scheme1={size_of_row_1} R_scheme2={size_of_row_2}
        output: n_new_scheme={num_of_rows} R_new_scheme={size_of_row}
        """
        print(msg)
        return (num_of_rows, size_of_row)

    def get_all_attributes(self, i_scheme):
        if(i_scheme == None):
            att_list =self.get_all_attributes("scheme1") +self.get_all_attributes("scheme2")
        if(self.scheme1 == 'R'):
            att_list = R_attributes
        elif(self.scheme1 == 'S'):
            att_list = S_attributes
        else:
            att_list = self.scheme1.get_all_attributes()
        return att_list
