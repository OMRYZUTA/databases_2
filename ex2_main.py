import random
import copy
import ex2_parser
from sigma import SIGMA
from pi import PI
from cartesian import CARTESIAN
from njoin import NJOIN
from algebric_expression import Algebric_Expression
import tables

optimization_rules = {
    "4": "SIGMA[p1 AND p2](T)=SIGMA[p1](SIGMA[p2](T))",
    "4a": "SIGMA[p1](SIGMA[p2](T))=SIGMA[p2](SIGMA[p1](T))",
    "5a": "PI[x](SIGMA[p](T))=SIGMA[p](PI[x](T))",
    "6": "SIGMA[p](NJOIN(T1,T2))=NJOIN(SIGMA[p](T1),T2)",
    "6a": "SIGMA[q](NJOIN(T1,T2))=NJOIN(T1,SIGMA[q](T2))",
    "11b": "SIGMA[p](CARTESIAN(T1,T2))=NJOIN(T1,T2)"
}


def build_initial_algebric_expression(table_list, attribute_list, condition_tree):

    cartesian = CARTESIAN(table_list[0], table_list[0])
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


def get_initial_algebric_expression():
    query_str = input("Enter your query: ")
    parsed_query = ex2_parser.parse_query(query_str)
    if (not parsed_query):
        return
    (table_list, attribute_list, condition_tree) = parsed_query

    alg_expr = build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)
    return alg_expr


def apply_and_show_rule(i_alg_expr, i_rule):
    print("before applying rule:")
    print(i_alg_expr)
    i_alg_expr.apply_rule(i_rule)
    print(
        f"after rule {i_rule} - {optimization_rules[i_rule]}:")
    print(i_alg_expr)


def randomly_apply_10_rules(i_alg_expr):
    for num in range(10):
        print(f"iteration number: {num}")
        rule = random.choice(list(optimization_rules.keys()))
        apply_and_show_rule(i_alg_expr, rule)
        print("")


def question_1():
    alg_expr = get_initial_algebric_expression()
    optimization_rule = get_optimization_rule()
    apply_and_show_rule(alg_expr, optimization_rule)


def question_2():
    alg_expr1 = get_initial_algebric_expression()
    alg_expr2 = copy.deepcopy(alg_expr1)
    alg_expr3 = copy.deepcopy(alg_expr1)
    alg_expr4 = copy.deepcopy(alg_expr1)
    alg_expressions = [alg_expr1, alg_expr2, alg_expr3, alg_expr4]
    
    for alg_expr in alg_expressions:
        randomly_apply_10_rules(alg_expr)

    print("the 4 resulting logical query plans:")
    for alg_expr in alg_expressions:
        print(f"\n - {alg_expr}")
    return alg_expressions


def question_3():
    alg_expressions = question_2()
    
    for alg_expr in alg_expressions:
        print(f" \n estimate cost of:{alg_expr}")
        alg_expr.estimate_size()
        print("*****************************************************")


def show_main_menu():
    message = """
    please select the part to check:
    1 - apply single optimization rule
    2 - get 4 random logical query plans
    3 - estimate size of logical query plans
    """
    choice = input(message)
    if choice == "1":
        question_1()
    elif choice == "2":
        question_2()
    elif choice == "3":
        question_3()


def main():
    tables.fill_tables('statistics.txt')
    show_main_menu()


if __name__ == "__main__":
    main()
