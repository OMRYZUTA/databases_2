import ex2_parser
import ex2_solution


def main():
    (table_list, attribute_list, condition_tree) = ex2_parser.parse_query("SELECT R.A,R.B FROM R,S WHERE R.A=10 AND R.B>R.A ;")
    print(table_list, attribute_list, condition_tree)
    # ex2_parser.parse_query("SELECT R.A FROM R,S WHERE (R.A=10 AND R.B>R.A) OR (R.C=12 AND R.A>3);")
    # SELECT R.A,R.B FROM R,S WHERE R.E=S.E AND R.D=S.D ;


if __name__ == "__main__":
    main()
