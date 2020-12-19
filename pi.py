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

