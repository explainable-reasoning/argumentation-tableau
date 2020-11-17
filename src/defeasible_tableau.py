from typing import *
from reasoning_elements.proposition import *
from reasoning_elements.rule import *
from reasoning_elements.node import *
from reasoning_elements.test import *

"""
The logic for the defeasible tableau is split between this file and `node.py`.
"""


class Tableau:
    def __init__(self,
                 final_conclusion: Proposition,
                 initial_information: List[Proposition] = [],
                 rules: List[Rule] = []
                 ):
        """
        On initialization, the root node will be created and filled with the appropriate arguments.
        The `final_conclusion` refers to the conclusion for which the tableau should generate (counter)arguments.
        """
        self.root = Node(
            # Arguments for the initial information:
            [Argument([p], p) for p in initial_information]
            # Tests for the final conclusion:
            + [Argument([Test(Not(final_conclusion))], Not(final_conclusion))]
            # Tests for the antecedences of all rules:
            + [Argument([Test(Not(rule.antecedence))],
                        Not(rule.antecedence)) for rule in rules]
        )
        self.rules = rules
        self.final_conclusion = final_conclusion

    def evaluate(self) -> Tuple[List[Argument], List[Argument]]:
        """
        The main loop. It performs the following steps:
            1. Expand the tableau as far as possible.
            2. Retrieve all arguments for the closure of the tableau.
            3. Convert them into constructive arguments.
            4. Add them to all nodes (if they are not already there).
            5. If new arguments could be created in the last step: Repeat from step 1.
        Then it retrieves all arguments for and against the `final_conclusion` and returns them.
        """
        arguments_for_inconsistency: List[Argument] = []
        while True:
            self.root.expand()  # 1.
            inconsistencies = self.transform_arguments(
                self.root.arguments_for_inconsistency())  # 2. & 3.
            new_arguments = [a for a in inconsistencies
                             if a not in self.root.arguments]  # 4.
            self.root.add(new_arguments)  # 4.
            if len(new_arguments) == 0:
                break  # 5
        pro, contra = self.root.arguments_for_and_against(
            self.final_conclusion)
        return pro, contra

    def transform_arguments(self, inconsistencies: List[Argument]) -> List[Argument]:
        """
        This takes arguments for an inconsistency such as:
            ({¬a?, b, ¬c}, False)
        If the test is about the final conclusion, 
        then it will create a constructive argument:
            ({b, ¬c}, a)                (1.)
        If the test is about an antecedence of a rule
            a ~> d
        then it will create a constructive argument:
            ({b, ¬c}, a ~> d)           (2.)
        """
        new_arguments = []
        for a in inconsistencies:
            tests: List[Test] = [p for p in a.support if isinstance(p, Test)]
            if len(tests) == 1:
                test = tests[0]
                support = [p for p in a.support if str(p) != str(test)]
                # 1.:
                if test.nonnegated_content() == self.final_conclusion:
                    new_arguments.append(
                        Argument(support, test.nonnegated_content()))
                # 2.:
                else:
                    for rule in self.rules:
                        if rule.antecedence == test.nonnegated_content():
                            new_arguments.append(
                                Argument(
                                    [Argument(support, rule)],
                                    rule.consequence
                                )
                            )
            elif len(tests) == 0:
                pass  # TODO deal with inconsistencies in the initial information
        return new_arguments
