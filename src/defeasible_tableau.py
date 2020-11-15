from typing import *
from reasoning_elements.proposition import *
from reasoning_elements.rule import *
from reasoning_elements.node import *


class Tableau:
    def __init__(self,
                 initial_information: List[Proposition],
                 rules: List[Rule],
                 final_conclusion: Proposition
                 ):
        # initialize the root node
        self.root = Node(
            [([p], p) for p in initial_information]
            + [([Test(Not(final_conclusion))], Not(final_conclusion))]
            + [([Test(Not(rule.antecedence))],
                Not(rule.antecedence)) for rule in rules]
        )
        self.rules = rules
        self.final_conclusion = final_conclusion

    def evaluate(self) -> List[Argument]:
        done = False
        arguments_for_incosistency: List[Argument] = []
        while not done:
            # get support for inconsistencies:
            new_arguments = self.create_arguments(arguments_for_incosistency)

            # expand node until inconsistencies occur in all branches:
            done, arguments_for_incosistency = self.root.expand(new_arguments)
        return self.root.arguments_for(self.final_conclusion)

    def create_arguments(self, arguments_for_incosistency: List[Argument]) -> List[Argument]:
        # gets the support for the closure of the tableau (if there is such a support) and creates new arguments to be added to th root node
        """
        if the root node closes with support S (see below):
            if S includes exactly one test:
                if the test is ¬p?, return success (S\{¬p}, p) AND GO ON
                for each antecedence x of a rule x~>y:
                if the test is ¬x?, add (S\{¬x}, x), (S\{¬x}, x~>y) to every leaf node
            if S includes no tests:
                TODO deal with inconsistency in the initial information
        """
        return []

    def forward_search_rule(self, rule_list: List[Rule], antecedence_proposition: Proposition) -> List[Rule]:
        applied_rule = []
        for single_rule in rule_list:
            if hash(str(single_rule.consequence)) == hash(str(antecedence_proposition)):
                applied_rule.append(single_rule)
        return applied_rule

    def backward_search_rule(self, rule_list: List[Rule], consequence_proposition: Proposition) -> List[Rule]:
        applied_rule = []
        for single_rule in rule_list:
            if hash(str(single_rule.consequence)) == hash(str(consequence_proposition)):
                applied_rule.append(single_rule)
        return applied_rule
