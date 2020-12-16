# Orna's sketch idea
import ex2_parser


class PI:
    attribute_list = None
    apply_to = None

    def __init__(self, attribute_list, apply_to):
        self.attribute_list = attribute_list
        self.apply_to = apply_to

    def __str__(self):
        att_list_str = " ".join(self.attribute_list)
        string = "PI["+att_list_str+"]"
        string += "("+self.apply_to+")"

        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)


class CARTESIAN:
    scheme1 = None
    scheme2 = None

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


class SIGMA:
    condition = None
    apply_to = None

    def __init__(self, condition, apply_to):
        self.condition = condition
        self.apply_to = apply_to

    def __str__(self):
        string = "SIGMA"
        string += "["+self.condition+"]"
        string += "("+self.apply_to+")"
        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)


def build_initial_algebric_expression(table_list, attribute_list, condition_tree):
    cartesian = CARTESIAN(table_list[0], None)
    if(len(table_list) == 2):
        cartesian.scheme2 = table_list[1]    

    sigma = SIGMA(condition_tree, cartesian)
    pi = PI(attribute_list, sigma)
    
    print(pi)


def main():
    table_list = None
    attribute_list = None
    condition_tree = None

    query_str = input("Enter your query: ")
    (table_list, attribute_list, condition_tree) = ex2_parser.parse_query(query_str)

    build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)


if __name__ == "__main__":
    main()
