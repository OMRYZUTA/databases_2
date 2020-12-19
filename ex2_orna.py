# Orna's sketch idea
import ex2_parser
from operators import PI, SIGMA, CARTESIAN

# optimization_rules = {}
# optimization_rules["4"] = "SIGMA[p1 AND p2](R)=SIGMA[p1](SIGMA[p2](R))"
# optimization_rules["4a"] = "SIGMA[p1](SIGMA[p2](R))=SIGMA[p2](SIGMA[p1](R))"
# optimization_rules["5a"] = "PI[X](SIGMA[p](R))=SIGMA[p](PI[X](R))"
# optimization_rules["6"] = "SIGMA[p](NJOIN(R,S))=NJOIN(SIGMA[p](R),S)"
# optimization_rules["11b"] = "SIGMA[p](CARTSIAN(R,S))=TJOIN[p](R,S)"


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
    alg_expr = build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)
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
