class PI:
    attribute_list = None
    applies_to = None

    def __init__(self, attribute_list, applies_to):
        self.attribute_list = attribute_list
        self.applies_to = applies_to

    def __str__(self):
        att_list_str = " ".join(self.attribute_list)
        string = "PI["+att_list_str+"]"
        string += "("+self.applies_to+")"

        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def apply_rule(self, rule_type):
        if (rule_type == "5a"):
            if (self.applies_to.get_type() == "SIGMA"):
                sigma = self.applies_to
                if (sigma.check_all_attributes_from(self.attribute_list)):
                    self.applies_to = sigma.applies_to
                    sigma.applies_to = self
                    return sigma
        elif(rule_type == "4" or rule_type == "4a"):
            self.applies_to.apply_rule(rule_type)
        return self

    def get_type(self):
        return "PI"


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

    def get_type(self):
        return "CARTESIAN"


class SIGMA:
    condition = None
    applies_to = None

    def __init__(self, condition, applies_to):
        self.condition = condition
        self.applies_to = applies_to

    def __str__(self):
        string = "SIGMA"
        string += "["+self.condition+"]"
        string += "("+self.applies_to+")"
        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def check_all_attributes_from(self, attribute_list):
        result = True
        all_cond_attributes = self.condition.get_all_atts_in_cond()
        for att in all_cond_attributes:
            result = result and (att in attribute_list)
        return result

    def get_type(self):
        return "SIGMA"

    def apply_rule(self, rule_type):
        if (rule_type == "5a"):
            self.applies_to.apply_rule(rule_type)
        elif(rule_type == "4"):
            if (self.condition.data == "AND"):
                self.applies_to = SIGMA(self.condition.right, self.applies_to)
                self.condition = self.condition.left
        elif(rule_type == "4a"):
            if(self.applies_to.get_type()=="SIGMA"):
                temp_condition_tree=self.applies_to.condition
                self.applies_to.condition= self.condition
                self.condition= temp_condition_tree
        return self
