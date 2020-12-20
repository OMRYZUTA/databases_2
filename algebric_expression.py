class Algebric_Expression:
    root = None

    def __init__(self, root):
        self.root = root

    def __str__(self):
        return str(self.root)

    def apply_rule(self, rule_type):
        self.root = self.root.apply_rule(rule_type)

   

