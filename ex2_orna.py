# Orna's sketch idea
import ex2_parser


class PI:
    attribute_list = None
    apply_to = None

    def __init__(self, attribute_list, apply_to):
        self.attribute_list = attribute_list
        self.apply_to = apply_to

    def __str__(self):
        att_list_str = " ".join(self.attribute_list)
        string = "PI["+att_list_str+"]"
        string += "("+self.apply_to+")"

        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)


class CARTESIAN:
    scheme1 = None
    scheme2 = None

    def __init__(self, scheme1, scheme2):
        self.scheme1 = scheme1
        self.scheme2 = scheme2

    def __str__(self):
        string = "CARTESIAN"
        string += "("+self.scheme1+","+self.scheme2+")"

        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)


class SIGMA:    
    condition = None
    apply_to = None

    def __init__(self, condition, apply_to):
        self.condition = condition
        self.apply_to = apply_to

    def __str__(self):
        string = "SIGMA"
        string += "["+self.condition+"]"
        string += "("+self.apply_to+")"
        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

class Algebric_Expression:
    #how can we indicate operators order in terms of inner-to-outer??
    pi = None
    sigma = None
    cartesian = None

    def __init__(self, pi, sigma, cartesian):
        self.pi = pi
        self.sigma = sigma
        self.cartesian = cartesian


def build_initial_algebric_expression(
    table_list, attribute_list, condition_tree):
    
    cartesian = CARTESIAN(table_list[0], table_list[0])
    #if there's only one table it's a cartesian with itself?? delete later
    if(len(table_list) == 2):
        cartesian.scheme2 = table_list[1]    

    sigma = SIGMA(condition_tree, cartesian)
    pi = PI(attribute_list, sigma)    
   
    initial_expr = Algebric_Expression(pi, sigma, cartesian)
    return initial_expr

def apply_rule_4(i_expression):
    new_expression =  i_expression  
    cond = i_expression.sigma.condition
    if(cond.node_type=="LOGIC_OP"):
        if(cond.data=="AND"):
            #doesn't change cartesian
            inner_sigma = SIGMA(cond.right,new_expression.cartesian)
            #outer_sigma will be the new expression's sigma
            new_expression.sigma = SIGMA(cond.left,inner_sigma)
            new_expression.pi=PI(i_expression.pi.attribute_list, new_expression.sigma)
    print("after applying rule 4:")        
    print (new_expression.pi)
    return new_expression.pi
     

def main():
    table_list = None
    attribute_list = None
    condition_tree = None

    query_str = input("Enter your query: ")
    (table_list, attribute_list, condition_tree) = ex2_parser.parse_query(query_str)
    query_tuple = (table_list, attribute_list, condition_tree)

    alg_expr = build_initial_algebric_expression(
        table_list, attribute_list, condition_tree)
    print("initial algebric expression")
    print(alg_expr.pi)

    apply_rule_4(alg_expr)


if __name__ == "__main__":
    main()
