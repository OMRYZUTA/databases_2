def get_table_size(i_table):
    num_of_rows = None
    size_of_row = None

    if(isinstance(i_table, str)):
        if(i_table == 'R'):
            num_of_rows = Table_R["n_R"]
            size_of_row = Table_R["num_of_atts"]*Table_R["att_size"]
        elif(i_table == 'S'):
            num_of_rows = Table_S["n_S"]
            size_of_row = Table_S["num_of_atts"]*Table_S["att_size"]
    return (num_of_rows, size_of_row)


def get_range_of_values(i_table, i_attribute):
    result = None

    if(i_table == "R"):
        result = vR[i_attribute]
    else:
        result = vS[i_attribute]
    return result


Table_S = {
    "num_of_atts": 5,
    "att_size": 4,  # integer
    "n_S": 0  # number of lines in a table
}

vS = {}
vS["D"] = 0  # V_att is the number of different values in attribute.
vS["E"] = 0
vS["F"] = 0
vS["H"] = 0
vS["I"] = 0

Table_R = {
    "num_of_atts": 5,
    "att_size": 4,
    "n_R": 0
}

vR = {}
vR["A"] = 0
vR["B"] = 0
vR["C"] = 0
vR["D"] = 0
vR["E"] = 0


def fill_statistics_for_attributes(i_content, i_v_dictionary, i_index):
    stringToFind_index = i_index
    for key in i_v_dictionary.keys():
        stringToFind_index = i_content.find("V("+key+")=", stringToFind_index)
        enter_index = i_content.find("\n", stringToFind_index)
        i_v_dictionary[key] = int(i_content[stringToFind_index+5:enter_index])
    return stringToFind_index


def fill_tables(i_file_name):
    with open(i_file_name) as file:
        content = file.read()
        stringToFind_index = 0
        stringToFind_index = fill_statistics_for_attributes(
            content, vR, stringToFind_index)
        fill_statistics_for_attributes(content, vS, stringToFind_index)
        
        stringToFind_index = content.find("n_R")
        enter_index = content.find("\n", stringToFind_index)
        Table_R["n_R"] = int(content[stringToFind_index+4:enter_index])

        stringToFind_index = content.find("n_S")
        enter_index = content.find("\n", stringToFind_index)
        Table_S["n_S"] = int(content[stringToFind_index+4:enter_index])
