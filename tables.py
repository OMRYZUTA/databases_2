def get_table_size(i_table):        
        num_of_rows=None
        size_of_row=None       
        
        if( isinstance(i_table,str)):
            if(i_table =='R'):
                num_of_rows=Table_R.n_R
                size_of_row=Table_R.num_of_atts*Table_R.att_size
            elif(i_table =='S'):
                num_of_rows=Table_S.n_S
                size_of_row=Table_S.num_of_atts*Table_S.att_size
        return (num_of_rows,size_of_row)  

def get_range_of_values(i_table, i_attribute):
    result=None

    if(i_table=="R"):
        if(i_attribute=="A"):
            result = Table_R.V_A


class Table_S():
    num_of_atts=5
    att_size=4  #integer
    n_S = 200 #number of lines in a table
    V_D = 100 #V_att is the number of different values in attribute.
    V_E = 100
    V_F = 100
    V_H = 8
    V_I = 200

class Table_R():
    num_of_atts=5
    att_size=4
    n_R=100
    V_A=50
    V_B=100
    V_C=50
    V_D=1
    V_E=8
