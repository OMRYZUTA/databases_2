def get_table_size(i_table):        
        num_of_rows=None
        size_of_row=None       
        
        if( isinstance(i_table,str)):
            if(i_table =='R'):
                num_of_rows=Table_R["n_R"]
                size_of_row=Table_R["num_of_atts"]*Table_R["att_size"]
            elif(i_table =='S'):
                num_of_rows=Table_S["n_S"]
                size_of_row=Table_S["num_of_atts"]*Table_S["att_size"]
        return (num_of_rows,size_of_row)  

def get_range_of_values(i_table, i_attribute):
    result=None

    if(i_table=="R"):
        result = vR[i_attribute]
    else:
        result =vS[i_attribute]
    return result

Table_S={
    "num_of_atts":5,
    "att_size":4,  #integer
    "n_S": 200 #number of lines in a table
}

vS ={}
vS["D"] = 100 #V_att is the number of different values in attribute.
vS["E"] = 100
vS["F"] = 100
vS["H"] = 8
vS["I"] = 200
Table_R={
    "num_of_atts":5,
    "att_size":4,
    "n_R":100
}

vR ={}
vR["A"]=50
vR["B"]=100
vR["C"]=50
vR["D"]=1
vR["E"]=8