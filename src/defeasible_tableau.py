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
                 question: Proposition,
                 initial_information: Set[Proposition] = set(),
                 rules: Set[Rule] = set()
                 ):
        """
        On initialization, the root node will be created and filled with the appropriate arguments.
        The `question` refers to the conclusion for which the tableau should generate (counter)arguments.
        """
        self.root = Node(
            # `|` is the union operation on sets
            # Arguments for the initial information:
            {Argument(set([p]), p) for p in initial_information}
            # Tests for the final conclusion:
            | {Argument(set([Test(Not(question))]), Not(question))}
            # Tests for the antecedences of all rules:
            | {Argument(set([Test(Not(rule.antecedence))]),
                        Not(rule.antecedence)) for rule in rules}
        )
        self.initial_information = initial_information
        self.rules = rules
        self.question = question

    def evaluate(self) -> Tuple[str, Union[Set[FrozenSet[str]], Tuple[List[Argument], List[Argument]]]]:
        """
        The main loop. It performs the following steps:
            1. Expand the tableau as far as possible.
            2. Retrieve all arguments for the closure of the tableau.
            3. Convert them into constructive arguments.
            4. Add them to all nodes (if they or more minimal ones are not already there).
            5. If new arguments could be created in the last step: Repeat from step 1.
        Then it retrieves all arguments for and against the `question` and returns them.
        """
        arguments_for_inconsistency: Set[Argument] = set()
        while True:
            self.root.expand()  # 1.
            candidates = self.transform_arguments(
                self.root.arguments_for_inconsistency())  # 2. & 3.
            new_arguments: Set[Argument] = set()
            # 4.:
            for c in candidates:
                exists_already = False
                for old in self.root.arguments:
                    if (c.conclusion == old.conclusion
                            and set(old.support).issubset(set(c.support))):
                        exists_already = True
                if not exists_already:
                    new_arguments.add(c)
            self.root.add(new_arguments)  # 4.
            if len(new_arguments) == 0:
                break  # 5
        pro, contra = self.root.arguments_for_and_against(
            self.question)
        if len(pro) > 0 or len(contra) > 0:
            # TODO Is this a good if-condition? Don't know.
            # TODO Maybe rather explicitly look if branches close.
            return 'known', (sorted(list(pro)), sorted(list(contra)))
        else:
            return 'unknown', [c for a in self.root.get_undecided_propositions() for c in a
                                    if str(to_proposition(c).strip_negation()) not in [str(b.strip_negation())
                                             for b in self.initial_information] and c.strip_negation() != str(self.question.strip_negation())]

    def transform_arguments(self, inconsistencies: Set[Argument]) -> Set[Argument]:
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
        new_arguments: Set[Argument] = set()
        for a in inconsistencies:
            tests: List[Test] = [p for p in a.support if isinstance(p, Test)]
            if len(tests) == 1:
                test = tests[0]
                support = {p for p in a.support if str(p) != str(test)}
                # 1.:
                if test.nonnegated_content() == self.question:
                    new_arguments.add(
                        Argument(support, test.nonnegated_content()))
                # 2.:
                for rule in self.rules:
                    if rule.antecedence == test.nonnegated_content():
                        new_arguments.add(
                            Argument(
                                set([Argument(support, rule)]),
                                rule.consequence
                            )
                        )
            elif len(tests) == 0:
                pass  # TODO deal with inconsistencies in the initial information
        return new_arguments

    def __str__(self):
        return str(self.root)
