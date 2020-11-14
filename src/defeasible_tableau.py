from typing import *
from reasoning_elements.proposition import *


# mypy src/__main__.py

class Tableaux:
    root = {propositions: [], tests: []}
    rules = []
    
    def __init__(self,
        initial_information: List[Proposition],
        rules: List[Rule],
        final_conclusion: Proposition
    ):
        # initialize the root node
        self.root = [([proposition], proposition) for proposition in initial_information]
        self.root += (Test(Not(final_conclusion)), Not(final_conclusion))  # should be annotated as a test
        self.root += [([Test(Not(rule.antecedence))], Not(rule.antecedence)) for rule in rules] # should be annotated as tests
        self.rules = rules

        

    def evaluate(self) -> List[Argument]:
        done = False
        arguments_for_incosistency = []
        while not done:
            # get support for inconsistencies
            new_arguments = create_arguments(arguments_for_incosistency)

            # expand node until inconsistencies occur in all branches
            done, arguments_for_incosistency = self.root.expand(new_arguments)
            
            """
            rule q ~> m
            branch a ([ ¬q?, a, ...], ⟘ )
            branch a ([ ¬n?, z, ...], ⟘ )
            branch b ([ b, ...], ⟘ )
            combined ([ ¬q?, a, b, ...], ⟘)
            combined ([ ¬n?, z, b, ...], ⟘)
            ([a, b, ...], q ~> m)
            ([z, b, ...], n)
            """
        return
            

    def create_arguments(self) -> List[Argument]:
        # gets the support for the closure of the tableau (if there is such a support) and creates new arguments to be added to th root node
        
        # evaluate tests 

        # apply rules
        
        """
        if the root node closes with support S (see below):
            if S includes exactly one test:
                if the test is ¬p?, return success (S\{¬p}, p) AND GO ON
                for each antecedence x of a rule x~>y:
                if the test is ¬x?, add (S\{¬x}, x), (S\{¬x}, x~>y) to every leaf node
            if S includes no tests:
                TODO deal with inconsistency in the initial information
        """


    def forward_search_rule(self, rule_list: list[Rule], antecedence_proposition:Proposition) -> list[Rule]:
        applied_rule = []
        for single_rule in rule_list:
            if hash(str(single_rule.consequence)) == hash(str(antecedence_proposition)):
                applied_rule.append(single_rule)
        return applied_rule

    def backward_search_rule(self, rule_list: list[Rule], consequence_proposition:Proposition) -> list[Rule]:
        applied_rule = []
        for single_rule in rule_list:
            if hash(str(single_rule.consequence)) == hash(str(consequence_proposition)):
                applied_rule.append(single_rule)
        return applied_rule
        



"""proving a proposition p, given support Σ, rules D, and preference > :
    for every proposition s ∈ Σ, add an argument ({s}, s) to the root node
    for the proposition p to be proven, add an argument ({¬p?}, ¬p) to the root node
    add each antecedence of a rule as a negated test to the root node
    Repeat:
        expand every leaf recursively (see below)
        
        if the size of the tableau has not changed since the last iteration:
            return failure

"""
