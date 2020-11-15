class Rule:

    def __init__(self, antecedence, consequence, default_defeasible_level=5):
        self.antecedence = []
        self.consequence = []
        self.defeasible_level = default_defeasible_level
        self.antecedence = antecedence
        self.consequence = consequence

    def __str__(self):
        return str(antecedence) + ' ~> ' + str(consequence)
