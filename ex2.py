def decipher_attribute_list(i_select_part):
    select_part = i_select_part.strip()
    attribute_list =select_part.split(",")
    attribute_list = list(map(str.strip,attribute_list))
    return attribute_list


def decipher_table_list(i_from_part):
    table_list = i_from_part.split(",")

    table_list = list(map(str.strip, table_list))

    return table_list


def  question_3():
    pass


def  question_2():
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
    optimization_rule =input(message)
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
    #condition_list= is_where_part_valid(query[where_index:], table_list)):

    return query 
    



def  question_1():
    query =get_query()
    optimization_rule = get_optimization_rule()





def show_main_menu():
    message = """
    please insert the part to check:
    1 - apply optimization rules
    2 - get 4 random logical query plans
    3 - Size Estimation
    """
    choice = input(message)
    if choice =="1":
        question_1()
    elif choice =="2":
        question_2()
    elif choice == "3":
        question_3()
        



def main():
    show_main_menu()
    
    


if __name__ == "__main__":
    main()