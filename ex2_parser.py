from conditionTree import cond_tree_node

R_attributes = ['R.A', 'R.B', 'R.C', 'R.D', 'R.E']
S_attributes = ['S.D', 'S.E', 'S.F', 'S.H', 'S.I']
valid_attributes = R_attributes+S_attributes

def get_valid_table(i_table):
    result = None
    table = i_table.strip()
    if (table == "R" or table == "S"):
        result = table

    return result


def get_valid_attribute_node(i_attribute):
    """returns node in condition tree (in this case leaf)"""
    new_node = None
    attribute = get_valid_att(i_attribute)

    if (attribute):
        new_node = cond_tree_node(attribute, "ATTRIBUTE")

    return new_node


def get_valid_constant_node(i_constant):
    """returns a cond_tree_node with constant"""
    new_node = None
    constant = i_constant.strip()
    # because it's a valid query - will either be attribute or integer
    new_node = get_valid_attribute_node(constant)
    if(new_node is None and constant.isnumeric()):
        new_node = cond_tree_node(constant, "INTEGER")

    return new_node


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


def get_valid_simple_condition_node(i_simple_condition):
    """returns cond_tree_node which is a root of simple-condition-sub-tree"""
    new_node = None
    simple_condition = i_simple_condition.strip()

    operator = find_valid_operator(simple_condition)
    if(operator != -1):
        parts_array = simple_condition.split(operator)

        left_node = get_valid_constant_node(parts_array[0])
        right_node = get_valid_constant_node(parts_array[1])
        if(left_node and right_node):
            new_node = cond_tree_node(
                operator, "REL_OP", left_node, right_node)

    return new_node


def check_both_sides_of_operator(i_condition, i_operator, i_index, i_node, i_checked_all_options):
    """function used in get_valid_condition"""
    """returns (operator_index, new_node, checked_all_options)"""
    offset = 3 if i_operator == "AND" else 2  # either "AND" or "OR"

    if(i_condition[i_index-1] == ")" or i_condition[i_index-1] == " "):
        if(i_condition[i_index+offset] == "(" or i_condition[i_index+offset] == " "):
            left_node = get_valid_condition(i_condition[0:i_index])
            right_node = get_valid_condition(i_condition[i_index+offset:])

            if(left_node and right_node):
                i_node = cond_tree_node(
                    i_operator, "LOGIC_OP", left_node, right_node)
            else:
                i_index = i_condition.find(i_operator, i_index+offset)
        else:
            i_checked_all_options = True
    else:
        i_checked_all_options = True

    return(i_index, i_node, i_checked_all_options)


def get_valid_condition(i_condition):
    """returns cond_tree_node which is a root of a condition tree"""
    condition = i_condition.strip()
    new_node = None

    new_node = get_valid_simple_condition_node(condition)
    if(new_node):
        return new_node
    else:  # meaning it's more than just a simple condition
        checked_all_options = False
        and_index = condition.find("AND")
        or_index = condition.find("OR")

        while((not checked_all_options) and (new_node is None)):
            if(or_index != -1):
                (or_index, new_node, checked_all_options) = check_both_sides_of_operator(
                    condition, "OR", or_index, new_node, checked_all_options)
            elif(and_index != -1):
                # check_both_sides_of_operator function includes the recursive call to get_valid_condition
                (and_index, new_node, checked_all_options) = check_both_sides_of_operator(
                    condition, "AND", and_index, new_node, checked_all_options)
            else:  # both indexes not found
                checked_all_options = True
                if (new_node is None):
                    if(condition[0] == "(" and condition[-1] == ")"):
                        new_node = get_valid_condition(condition[1:-1])

    return new_node


def get_valid_att(i_att):
    result = None
    att = i_att.strip()

    if (att in valid_attributes):
        result = att

    return result


def get_valid_att_list(i_att_list):
    att_list = i_att_list.strip()
    result = get_valid_att(att_list)
    if (result):
        result = [result]
    else:
        comma_index = att_list.find(",")
        if (comma_index > 0):
            first_attribute = get_valid_att(att_list[0:comma_index])
            if (first_attribute):
                other_attributes = get_valid_att_list(att_list[comma_index+1:])
                if (other_attributes):
                    result = [first_attribute] + other_attributes

    return result


def get_valid_table_list(i_table_list):
    table_list = i_table_list.strip()
    result = get_valid_table(table_list)
    if (result):
        # if we have a single table, return as a list with one element
        result = [result]
    else:
        comma_index = table_list.find(",")
        if(comma_index > 0):
            first_table = get_valid_table(table_list[0:comma_index])
            if (first_table):
                other_tables = get_valid_table_list(table_list[comma_index+1:])
                if (other_tables):
                    result = [first_table] + other_tables

    return result


def get_attribute_list(i_select_part):
    """returns a list of attributes"""
    attribute_list = None
    # i_select_part starts with "select" and there has to be a space right after it
    if (i_select_part[6] == " "):
        select_part = i_select_part[6:].strip()
        distinct_index = select_part.find("DISTINCT")
        if(distinct_index == 0):
            # attribute list starts after the distinct
            select_part = select_part[8:].strip()

        index_of_astrix = select_part.find("*")
        if(index_of_astrix == 0):
            if(select_part == "*"):  # the attribute list is only *
                attribute_list = valid_attributes  # replacing astrix withh all attributes
        else:
            attribute_list = get_valid_att_list(select_part)

    return attribute_list


def get_table_list(i_from_part):
    table_list = None

    # i_from_part starts with "from" and there has to be a space right after it
    if(i_from_part[4] == " "):
        from_part = i_from_part[4:].strip()
        table_list = get_valid_table_list(from_part)

    return table_list


def get_condition_tree(i_where_part):
    condition_tree = None
    # i_where_part starts with "where" and there has to be a space right after it
    if(i_where_part[5] == " "):
        where_part = i_where_part[5:].strip()
        condition_tree = get_valid_condition(where_part)

    return condition_tree


def parse_query(i_query):
    """returns tuple (table_list, attribute_list, condition_tree) or None if query is invalid"""
    query = i_query.strip()

    if(query[-1] != ";"):  # missing ; at the end of the query
        print("Invalid Parsing <condition> failed")
        return

    query = query[0:-1]
    select_index = query.find("SELECT")
    from_index = query.find("FROM")
    where_index = query.find("WHERE")

    table_list = get_table_list(query[from_index:where_index])
    if(table_list is None):
        print("Invalid. Parsing <table_list> failed")
        return

    attribute_list = get_attribute_list(query[select_index:from_index])
    if(attribute_list is None):
        print("Invalid. Parsing <attribute_list> failed")
        return

    condition_tree = get_condition_tree(query[where_index:])
    if(condition_tree is None):
        print("Invalid Parsing <condition> failed")
        return

    return(table_list, attribute_list, condition_tree)


def main():
    table_list = None
    attribute_list = None
    condition_tree = None

    query = input("Enter your query: ")
    (table_list, attribute_list, condition_tree) = parse_query(query)


if __name__ == "__main__":
    main()
