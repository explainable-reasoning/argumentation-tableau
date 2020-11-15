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
            [Argument([p], p) for p in initial_information]
            + [Argument([Test(Not(final_conclusion))], Not(final_conclusion))]
            + [Argument([Test(Not(rule.antecedence))],
                        Not(rule.antecedence)) for rule in rules]
        )
        self.rules = rules
        self.final_conclusion = final_conclusion

    def evaluate(self) -> List[Argument]:
        done = False
        old_arguments_for_inconsistency: List[Argument] = []
        new_arguments_for_inconsistency: List[Argument] = []
        while True:
            new_arguments = self.transform_arguments(
                new_arguments_for_inconsistency)
            self.root.add(new_arguments)
            # expand node as far as possible
            self.root.expand()
            arguments_for_inconsistency = self.root.arguments_for_inconsistency()
            new_arguments_for_inconsistency = [a for a in arguments_for_inconsistency if str(a) not in [str(o) for o in old_arguments_for_inconsistency]]
            old_arguments_for_inconsistency += new_arguments_for_inconsistency
            if len(new_arguments_for_inconsistency) == 0:
                break
        # print([str(a) for a in self.transform_arguments(old_arguments_for_inconsistency)])
        pro, contra = self.root.arguments_for_and_against(self.final_conclusion)
        return pro, contra

    def transform_arguments(self, arguments_for_inconsistency: List[Argument]) -> List[Argument]:
        # gets the support for the closure of the tableau (if there is such a support) and creates new arguments to be added to th root node
        new_arguments = []
        for a in arguments_for_inconsistency:
            tests = [p for p in a.support if isinstance(p, Test)]
            if len(tests) == 1:
                test = tests[0]

                conclusion = test.children[0].children[0]  # that is, the un-negated test
                support = [p for p in a.support if str(p) != str(test)]
                new_arguments.append(
                    Argument(support, conclusion)
                )
                for rule in self.rules:
                    if str(rule.antecedence) == str(conclusion):
                        new_arguments.append(
                            Argument(support, rule)
                        )
            else:
                pass  # TODO deal with inconsistencies in the initial information
        return new_arguments

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
