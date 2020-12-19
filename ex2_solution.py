# Orna's sketch idea
import ex2_parser
from sigma import SIGMA
from pi import PI
from cartesian import CARTESIAN
from njoin import NJOIN

optimization_rules = {
    "4": "SIGMA[p1 AND p2](T)=SIGMA[p1](SIGMA[p2](T))",
    "4a": "SIGMA[p1](SIGMA[p2](T))=SIGMA[p2](SIGMA[p1](T))",
    "5a": "PI[x](SIGMA[p](T))=SIGMA[p](PI[x](T))",
    "6": "SIGMA[p](NJOIN(T1,T2))=NJOIN(SIGMA[p](T1),T2)",
    "6a": "SIGMA[q](NJOIN(T1,T2))=NJOIN(T1,SIGMA[q](T2))",
    "11b": "SIGMA[p](CARTESIAN(T1,T2))=NJOIN(T1,T2)"
}


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


def get_optimization_rule():
    message = "please choose from the followoing optimization rules:\n"
    for key, value in optimization_rules.items():
        message += key + ":\t" + value + "\n"

    optimization_rule = input(message)
    return optimization_rule


def question_1():
    # input("Enter your query: ")
    query_str = "SELECT R.A,R.B FROM R,S WHERE R.E=S.E AND R.D=S.D ;"
    optimization_rule = get_optimization_rule()

    parsed_query = ex2_parser.parse_query(query_str)
    if (not parsed_query):
        return
    (table_list, attribute_list, condition_tree) = parsed_query

    alg_expr = build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)

    print("initial algebric expression:")
    print(alg_expr)
    alg_expr.apply_rule(optimization_rule)
    print(
        f"after rule {optimization_rule}: {optimization_rules[optimization_rule]}")
    print(alg_expr)


def show_main_menu():
    message = """
    please insert the part to check:
    1 - apply optimization rules
    2 - get 4 random logical query plans
    3 - Size Estimation
    """
    choice = input(message)
    if choice == "1":
        question_1()
    # elif choice == "2":
    #     question_2()
    # elif choice == "3":
    #     question_3()


def main():
    show_main_menu()


if __name__ == "__main__":
    main()
