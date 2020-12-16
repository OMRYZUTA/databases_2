class cond_tree_node:
    data = None
    node_type = None  # ATTRIBUTE, INTEGER, REL_OP, LOGIC_OP
    left = None
    right = None

    def __init__(self, data, node_type):
        self.data = data
        self.node_type = node_type

    def __str__(self):
        result = ""
        if self.left:
            result += "(" + self.left.__str__()
        if self.data:
            result += " " + self.data + " "
        if self.right:
            result += self.right.__str__() + ")"

        return result

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)


def is_valid_table(i_table):
    table = i_table.strip()
    return (table == "R" or table == "S")


valid_attributes = [
    'R.A', 'R.B', 'R.C', 'R.D', 'R.E',
    'S.D', 'S.E', 'S.F', 'S.H', 'S.I']

# returns node in condition tree (in this case leaf)


def get_valid_attribute(i_attribute):
    new_node = None
    attribute = i_attribute.strip()

    if (attribute in valid_attributes):
        new_node = cond_tree_node(attribute, "ATTRIBUTE")

    return new_node


# returns a cond_tree_node with constant
def get_valid_constant(i_constant):
    new_node = None
    constant = i_constant.strip()
    # because it's a valid query - will either be attribute or integer
    new_node = get_valid_attribute(constant)
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


# returns cond_tree_node which is a root of simple-condition-sub-tree
def get_valid_simple_condition(i_simple_condition):
    new_node = None
    simple_condition = i_simple_condition.strip()

    operator = find_valid_operator(simple_condition)
    if(operator != -1):
        parts_array = simple_condition.split(operator)

        left_node = get_valid_constant(parts_array[0])
        right_node = get_valid_constant(parts_array[1])
        if(left_node and right_node):
            new_node = cond_tree_node(operator, "REL_OP")
            new_node.left = left_node
            new_node.right = right_node

    return new_node

# function used in get_valid_condition
# returns (operator_index, new_node, checked_all_options)


def check_both_sides_of_operator(i_condition, i_operator, i_index, i_node, i_checked_all_options):
    if(i_operator == "AND"):
        offset = 3
    elif(i_operator == "OR"):
        offset = 2

    if(i_condition[i_index-1] == ")" or i_condition[i_index-1] == " "):
        if(i_condition[i_index+offset] == "(" or i_condition[i_index+offset] == " "):
            left_node = get_valid_condition(i_condition[0:i_index])
            right_node = get_valid_condition(i_condition[i_index+offset:])

            if(left_node and right_node):
                i_node = cond_tree_node(i_operator, "LOGIC_OP")
                i_node.left = left_node
                i_node.right = right_node
            else:
                i_index = i_condition.find(i_operator, i_index+offset)
        else:
            i_checked_all_options = True
    else:
        i_checked_all_options = True
    return(i_index, i_node, i_checked_all_options)


# returns cond_tree_node which is a root of a condition tree
def get_valid_condition(i_condition):
    condition = i_condition.strip()
    new_node = None

    new_node = get_valid_simple_condition(condition)
    if(new_node):
        return new_node
    else:  # meaning it's more than just a simple condition
        checked_all_options = False
        and_index = condition.find("AND")
        or_index = condition.find("OR")

        while((not checked_all_options) and (new_node is None)):
            if(and_index != -1):
                # check_both_sides_of_operator function includes the recursive call to get_valid_condition
                (and_index, new_node, checked_all_options) = check_both_sides_of_operator(
                    condition, "AND", and_index, new_node, checked_all_options)
            elif(or_index != -1):
                (or_index, new_node, checked_all_options) = check_both_sides_of_operator(
                    condition, "OR", or_index, new_node, checked_all_options)
            else:  # both indexes not found
                checked_all_options = True
                if (new_node is None):
                    if(condition[0] == "(" and condition[-1] == ")"):
                        new_node = get_valid_condition(condition[1:-1])

    return new_node

# after handling optional distinct and astrix


def decipher_attribute_list(i_att_list):
    att_list = i_att_list.strip()
    att_list = att_list.split(",")
    att_list = list(map(str.strip, att_list))
    return att_list


# after handling optional distinct
def get_valid_attribute_list(i_attribute_list):
    attribute_list = None
    att_list = i_attribute_list.strip()
    index_of_astrix = att_list.find("*")

    if(index_of_astrix == 0):
        if(att_list == "*"):  # the attribute list is only *
            attribute_list = valid_attributes  # replacing astrix withh all attributes
    else:
        attribute_list = decipher_attribute_list(att_list)

    return attribute_list


def is_valid_table_list(i_table_list):
    table_list = i_table_list.strip()

    if(is_valid_table(table_list)):
        result = True
    else:
        comma_index = table_list.find(",")
        if(comma_index == -1):
            result = False
        else:
            result = is_valid_table(table_list[0:comma_index]) and is_valid_table_list(
                table_list[comma_index+1:])

    return result

# returns a list of attributes


def get_attribute_list(i_select_part):
    attribute_list = None
    # i_select_part starts with "select" and there has to be a space right after it
    if (i_select_part[6] == " "):
        select_part = i_select_part[6:].strip()
        distinct_index = select_part.find("DISTINCT")
        if(distinct_index == 0):
            # attribute list starts after the distinct
            select_part = select_part[8:]
        attribute_list = get_valid_attribute_list(select_part)

    return attribute_list


def get_table_list(i_from_part):
    table_list = None

    # i_from_part starts with "from" and there has to be a space right after it
    if(i_from_part[4] == " "):
        from_part = i_from_part[4:].strip()
        if(is_valid_table_list(from_part)):
            table_list = from_part.split(",")
            table_list = list(map(str.strip, table_list))

    return table_list


def get_condition_tree(i_where_part):
    condition_tree = None
    # i_where_part starts with "where" and there has to be a space right after it
    if(i_where_part[5] == " "):
        where_part = i_where_part[5:].strip()
        condition_tree = get_valid_condition(where_part)

    return condition_tree

# returns tuple (table_list, attribute_list, condition_tree)


def parse_query(i_query):
    table_list = None
    attribute_list = None
    condition_tree = None
    query = i_query.strip()

    if(query[-1] == ";"):
        query = query[0:-1]
        select_index = query.find("SELECT")
        from_index = query.find("FROM")
        where_index = query.find("WHERE")

        table_list = get_table_list(query[from_index:where_index])
        if(table_list is None):
            print("Invalid. Parsing <table_list> failed")
        else:
            attribute_list = get_attribute_list(query[select_index:from_index])
            if(attribute_list is None):
                print("Invalid. Parsing <attribute_list> failed")
            else:
                condition_tree = get_condition_tree(query[where_index:])
                if(condition_tree is None):
                    print("Invalid Parsing <condition> failed")
    else:  # missing ; at the end of the query
        print("Invalid Parsing <condition> failed")

    print("parser returns: ")
    print(table_list, attribute_list, condition_tree)
    return (table_list, attribute_list, condition_tree)


def main():
    table_list = None
    attribute_list = None
    condition_tree = None

    query = input("Enter your query: ")
    (table_list, attribute_list, condition_tree) = parse_query(query)


if __name__ == "__main__":
    main()
