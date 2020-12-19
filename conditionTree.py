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
            result += " " + self.data + " "
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
