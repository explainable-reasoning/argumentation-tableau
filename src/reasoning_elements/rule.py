class Rule:

    def __init__(self, antecedence, consequence,default_defeasible_level = 5):
        self.antecedence = []
        self.basic_antecedence = []
        self.consequence = []
        self.defeasible_level = default_defeasible_level
        # decompose antecendece
        self.antecedence = antecedence # contains all primitive propositions that need to be true to make the antecendence true
        # FIXME that should probably be multiple sets of propositions to account for disjunctive statements!!!
        self.consequence = consequence

        for proposition in antecedence:
            if propositions.is_basic():
                basic_antecedence.append(proposition)
            else:
                proposition.decompose()
                # do until there are only basic propositions left
        return

    def __str__(self):
        return

    def check_antecedence(current_support):
        # decompose non basic support propositions
        basic_support = []
        basic_antecedence = []

        for support in current_support:

        for proposition in antecedence:

        return