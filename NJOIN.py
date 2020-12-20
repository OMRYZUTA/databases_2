class NJOIN:
    scheme1 = None
    scheme2 = None
    applies_to = None

    def __init__(self, scheme1, scheme2):
        self.scheme1 = scheme1
        self.scheme2 = scheme2

    def __str__(self):
        string = "NJOIN"
        string += "("+self.scheme1+","+self.scheme2+")"

        return string

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def get_type(self):
        return "NJOIN"

    def apply_rule(self, rule_type):
        return self
