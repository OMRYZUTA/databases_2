import ex2_parser


def main():
    (table_list, attribute_list, condition_tree) = ex2_parser.parse_query("SELECT R.A,R.B FROM R,S WHERE R.A=10 AND R.B>R.A OR R.C=5 AND R.A>R.B;")
    print(table_list, attribute_list, condition_tree)
    # ex2_parser.parse_query("SELECT R.A FROM R,S WHERE (R.A=10 AND R.B>R.A) OR (R.C=12 AND R.A>3);")


if __name__ == "__main__":
    main()
