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
