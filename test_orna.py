import ex2_parser


def main():
    ex2_parser.parse_query("SELECT R.A FROM R,S WHERE R.A=10 AND R.B>R.A;")
    # ex2_parser.parse_query("SELECT R.A FROM R,S WHERE (R.A=10 AND R.B>R.A) OR (R.C=12 AND R.A>3);")


if __name__ == "__main__":
    main()
