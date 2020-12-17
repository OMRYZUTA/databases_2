class CondTreeNode:
    data = None
    left = None
    right = None

    def to_string(self):
        result = ""
        if self.left:
            result += self.left.to_string()
        if self.data:
            result += self.data
        if self.right:
            result += self.right.to_string()
        return result


def convert_algebric_expression(i_table_list, i_attribute_list, i_condition_tree):
    #my_string = ','.join(my_list)
    algebric_expression = "PI["

    algebric_expression += ','.join(i_attribute_list)
    algebric_expression += "](SIGMA["
    algebric_expression += i_condition_tree.to_string()
    algebric_expression += "](CARTESIAN("
    algebric_expression += ','.join(i_table_list)
    algebric_expression += ")))"
    return algebric_expression


def is_valid_attribute(i_attribute):
    attribute = i_attribute.strip()
    result = (attribute == "R.A" or attribute == "R.B"
              or attribute == "R.C" or attribute == "R.D" or attribute == "R.D" or attribute == "S.D" or attribute == "S.E"
              or attribute == "S.F" or attribute == "S.H" or attribute == "R.I")

    return result


def is_valid_constant(i_constant):
    constant = i_constant.strip()
    result = False

    if(is_valid_attribute(constant)):
        result = True
    elif(constant.isnumeric()):
        result = True

    return result


def find_valid_operator(i_simple_condition):
    simple_condition = i_simple_condition.strip()
    if(simple_condition.find("<=") != -1):
        result = "<="
    elif(simple_condition.find(">=") != -1):
        result = ">="
    elif(simple_condition.find("<>") != -1):
        result = "<>"
    elif(simple_condition.find("=") != -1):
        result = "="
    elif(simple_condition.find("<") != -1):
        result = "<"
    elif(simple_condition.find(">") != -1):
        result = ">"
    else:
        result = -1

    return result


def is_valid_simple_condition(i_simple_condition):
    simple_condition = i_simple_condition.strip()
    result = False

    operator = find_valid_operator(simple_condition)
    if(operator != -1):
        parts_array = simple_condition.split(operator)
        const1_result = is_valid_constant(
            parts_array[0])
        const2_result = is_valid_constant(
            parts_array[1])
        if(const1_result and const2_result):
            result = True

    return result


def check_both_sides_of_operator(i_condition, i_operator, i_index,  i_checked_all_options):
    offset = 0
    if(i_operator == "AND"):
        offset = 3
    elif(i_operator == "OR"):
        offset = 2

    if(i_condition[i_index-1] == ")" or i_condition[i_index-1] == " "):
        if(i_condition[i_index+offset] == "(" or i_condition[i_index+offset] == " "):
            left_operator_part = i_condition[0:i_index]
            right_operator_part = i_condition[i_index+offset:]
            if(decipher_condition_tree(left_operator_part) != None and decipher_condition_tree(right_operator_part) != None):
                result = CondTreeNode()
                result.data = i_operator
                result.left = decipher_condition_tree(
                    left_operator_part)
                result.right = decipher_condition_tree(right_operator_part)
            else:
                i_index = i_condition.find(
                    i_operator, i_index+offset)
        else:
            i_checked_all_options = True
    else:
        i_checked_all_options = True
    return(i_index, result, i_checked_all_options)


def decipher_condition_tree(i_condition):
    condition = i_condition.strip()
    result = None

    if(is_valid_simple_condition(condition)):
        result = CondTreeNode()
        result.data = condition
    else:
        checked_all_options = False
        and_index = condition.find("AND")
        or_index = condition.find("OR")

        while(not checked_all_options and result == None):
            if(and_index != -1):
                (and_index, result, checked_all_options) = check_both_sides_of_operator(
                    condition, "AND", and_index, checked_all_options,)
            elif(or_index != -1):
                (or_index, result, checked_all_options) = check_both_sides_of_operator(
                    condition, "OR", or_index, checked_all_options)
            else:  # both indexes not found
                checked_all_options = True
                if (not result):
                    if(condition[0] == "(" and condition[-1] == ")"):
                        result = decipher_condition_tree(condition[1:-1])

    return result


def decipher_attribute_list(i_select_part):
    select_part = i_select_part.strip()
    attribute_list = select_part.split(",")
    attribute_list = list(map(str.strip, attribute_list))
    return attribute_list


def decipher_table_list(i_from_part):
    table_list = i_from_part.split(",")

    table_list = list(map(str.strip, table_list))

    return table_list


def question_3():
    pass


def question_2():
    pass


def get_optimization_rule():
    message = """
    please choose from the followoing optimization rules:
    1. 4
    2. 4a
    3. 5a
    3. 6
    4. 11b
    """
    optimization_rule = input(message)
    return optimization_rule


def get_query():
    query = input("Enter your query: ")
    query = query.strip()
    query = query[0:-1]

    select_index = query.find("SELECT")
    from_index = query.find("FROM")
    where_index = query.find("WHERE")
    table_list = decipher_table_list(query[from_index+4:where_index])
    attribute_list = decipher_attribute_list(query[select_index+6:from_index])

    condition_tree = decipher_condition_tree(query[where_index+5:])
    parse_tree = (table_list, attribute_list, condition_tree)
    return parse_tree


def apply_5a(i_table_list, i_attribute_list, i_condition_tree):
    if(len(i_table_list) == 1):
        None
        # check all atributes in p


def question_1():
    (table_list, attribute_list, condition_tree) = get_query()
    algebric_expression = convert_algebric_expression(
        table_list, attribute_list, condition_tree)
    Foptimization_rule = get_optimization_rule()


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
    elif choice == "2":
        question_2()
    elif choice == "3":
        question_3()


def main():
    show_main_menu()


if __name__ == "__main__":
    main()
