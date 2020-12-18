# Orna's sketch idea
import ex2_parser


# optimization_rules = {}
# optimization_rules["4"] = "SIGMA[p1 AND p2](R)=SIGMA[p1](SIGMA[p2](R))"
# optimization_rules["4a"] = "SIGMA[p1](SIGMA[p2](R))=SIGMA[p2](SIGMA[p1](R))"
# optimization_rules["5a"] = "PI[X](SIGMA[p](R))=SIGMA[p](PI[X](R))"
# optimization_rules["6"] = "SIGMA[p](NJOIN(R,S))=NJOIN(SIGMA[p](R),S)"
# optimization_rules["11b"] = "SIGMA[p](CARTSIAN(R,S))=TJOIN[p](R,S)"


class PI:
    attribute_list = None
    applies_to = None

    def __init__(self, attribute_list, applies_to):
        self.attribute_list = attribute_list
        self.applies_to = applies_to

    def __str__(self):
        att_list_str = " ".join(self.attribute_list)
        string = "PI["+att_list_str+"]"
        string += "("+self.applies_to+")"

        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def apply_rule(self, rule_type):
        if (rule_type == "5a"):
            if (self.applies_to.get_type() == "SIGMA"):
                sigma = self.applies_to
                if (sigma.check_all_attributes_from(self.attribute_list)):
                    self.applies_to = sigma.applies_to
                    sigma.applies_to = self
                    return sigma
        elif(rule_type == "4" or rule_type == "4a"):
            self.applies_to.apply_rule(rule_type)
        return self

    def get_type(self):
        return "PI"


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

    def get_type(self):
        return "CARTESIAN"


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

    def apply_rule(self, rule_type):
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
        return self


class Algebric_Expression:
    root = None

    def __init__(self, root):
        self.root = root

    def __str__(self):
        return str(self.root)

    def apply_rule(self, rule_type):
        self.root = self.root.apply_rule(rule_type)

def build_initial_algebric_expression(table_list, attribute_list, condition_tree):

    cartesian = CARTESIAN(table_list[0], table_list[0])
    # if there's only one table it's a cartesian with itself?? delete later
    if(len(table_list) == 2):
        cartesian.scheme2 = table_list[1]
    sigma = SIGMA(condition_tree, cartesian)
    pi = PI(attribute_list, sigma)
    return Algebric_Expression(pi)


# def apply_rule_4(i_expression):
#     new_expression = i_expression
#     cond = i_expression.sigma.condition
#     if(cond.node_type == "LOGIC_OP"):
#         if(cond.data == "AND"):
#             # doesn't change cartesian
#             inner_sigma = SIGMA(cond.right, new_expression.cartesian)
#             # outer_sigma will be the new expression's sigma
#             new_expression.sigma = SIGMA(cond.left, inner_sigma)
#             new_expression.pi = PI(
#                 i_expression.pi.attribute_list, new_expression.sigma)

#     return new_expression.pi


def main():
    query_str = input("Enter your query: ")
    parsed_query = ex2_parser.parse_query(query_str)
    if (not parsed_query):
        return

    (table_list, attribute_list, condition_tree) = parsed_query
    alg_expr = build_initial_algebric_expression(table_list, attribute_list, condition_tree)
    print("initial algebric expression")
    print(alg_expr)

    alg_expr.apply_rule("4")
    print("after rule 4")
    print(alg_expr)
    alg_expr.apply_rule("4a")
    print("after rule 4a")
    print(alg_expr)


if __name__ == "__main__":
    main()
