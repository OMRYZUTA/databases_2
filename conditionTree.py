class cond_tree_node:
    data = None
    node_type = None  # ATTRIBUTE, INTEGER, REL_OP, LOGIC_OP
    left = None
    right = None

    def __init__(self, data, node_type, left=None, right=None):
        self.data = data
        self.node_type = node_type
        self.left = left
        self.right = right

    
    def __str__(self):
        result = ""
        if self.left:
            result += "(" + self.left.__str__()
        if self.data:
            result += "" + self.data + ""
        if self.right:
            result += self.right.__str__() + ")"

        return result

    
    def __add__(self, other):
        return str(self) + other

    
    def __radd__(self, other):
        return other + str(self)

    
    def get_all_atts_in_cond(self):
        if (self.left is None and self.right is None):  # is leaf
            if (self.node_type == "ATTRIBUTE"):
                return [self.data]
            else:
                return []

        return self.left.get_all_atts_in_cond() + self.right.get_all_atts_in_cond()


    def get_attribute_table(self):
        """receives an attribute-node and returns R or S"""        
        result = None        
        if(self.node_type == "ATTRIBUTE"):
            result = (self.data[0])    
        
        return result

        
    def get_attribute_alone(self):
        """receives an attribute-node and returns atribute alone"""        
        result = None        
        if(self.node_type == "ATTRIBUTE"):
            result = (self.data[2])    
        
        return result


    def are_different_tables(self):
        table1 = self.left.get_attribute_table()
        table2 = self.right.get_attribute_table()
        return (table1 != table2)

    
    def are_same_attributes(self):
        att1 = self.left.get_attribute_alone()
        att2 = self.right.get_attribute_alone()
        return (att1==att2)    