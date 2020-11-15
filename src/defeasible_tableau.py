from typing import *
from reasoning_elements.proposition import *
from reasoning_elements.rule import *
from reasoning_elements.node import *
from reasoning_elements.test import *


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

    def evaluate(self) -> Tuple[List[Argument], List[Argument]]:
        old_arguments_for_inconsistency: List[Argument] = []
        new_arguments_for_inconsistency: List[Argument] = []
        while True:
            self.root.expand()  # expand node as far as possible
            arguments_for_inconsistency = self.root.arguments_for_inconsistency()
            new_arguments_for_inconsistency = \
                [a for a in arguments_for_inconsistency
                 if str(a) not in
                 [str(o) for o in old_arguments_for_inconsistency]]
            old_arguments_for_inconsistency += new_arguments_for_inconsistency
            new_arguments = self.transform_arguments(
                new_arguments_for_inconsistency)
            self.root.add(new_arguments)
            if len(new_arguments) == 0:
                break
        pro, contra = self.root.arguments_for_and_against(
            self.final_conclusion)
        return pro, contra

    def transform_arguments(self, arguments_for_inconsistency: List[Argument]) -> List[Argument]:
        # gets the support for the closure of the tableau (if there is such a support) and creates new arguments to be added to the root node
        new_arguments = []
        for a in arguments_for_inconsistency:
            tests: List[Test] = [p for p in a.support if isinstance(p, Test)]
            if len(tests) == 1:
                # add argument for the un-negated test
                test: Test = tests[0]
                conclusion: Proposition = test.content.children[0]
                support = [p for p in a.support if str(p) != str(test)]
                new_arguments.append(
                    Argument(support, conclusion)
                )
                # add arguments for rules with a matching antecedens
                for rule in self.rules:
                    if str(rule.antecedence) == str(conclusion):
                        new_arguments.append(
                            Argument(support, rule)
                        )
            else:
                pass  # TODO deal with inconsistencies in the initial information
        return new_arguments
