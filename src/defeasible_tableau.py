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
                 rules: Set[Rule] = set(),
                 preference: Set[tuple] = set()
                 ):
        """
        On initialization, the root node will be created and filled with the appropriate arguments.
        The `question` refers to the conclusion for which the tableau should generate (counter)arguments.
        """
        self.root = Node(
            # Arguments for the initial information:
            {Argument(set([p]), p, -1) for p in initial_information}
            # Tests for the final conclusion:
            | {Argument(set([Test(Not(question))]), Not(question), -1)}
            # Tests for the antecedences of all rules:
            | {Argument(set([Test(Not(rule.antecedence))]),
                        Not(rule.antecedence), -1) for rule in rules}
        )
        self.preference = preference
        self.rules = self.rule_defeasible_level(rules,self.preference)
        self.question = question
        self.UnderCutting_argument = None
        self.defeating_order = []

    def evaluate(self) -> Tuple[List[Argument], List[Argument]]:
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
        return sorted(list(pro)), sorted(list(contra))

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
                # 2.: apply the rule
                try:
                    for index,rule in enumerate(self.rules):
                        if rule.antecedence == test.nonnegated_content():
                            new_arguments.add(
                                Argument(
                                    set([Argument(support, rule, index),]),
                                    rule.consequence,index
                                )
                            )
                except:
                    syslog = "can not load the index of rules, continue with no preference"
                    print(syslog)
                    for rule in self.rules:
                        if rule.antecedence == test.nonnegated_content():
                            new_arguments.add(
                                Argument(
                                    set([Argument(support, rule, -1)]),
                                    rule.consequence, -1
                                )
                            )

            elif len(tests) == 0:
                pass  # TODO deal with inconsistencies in the initial information
        return new_arguments

    @staticmethod
    def rule_defeasible_level(Inital_rule:Set[Rule], preference: Set[tuple]):
        """
                This inital the defeasibility of defeasible rule by the preference.
                the tuple(1,0) means rules[1] covers rules[0]
        """
        copy_perfence = set(preference.copy())
        weaker_set = set()
        while len(copy_perfence) > 0:

            prior_list = set([i[0] for i in copy_perfence])
            poor_list = set([i[1] for i in copy_perfence])

            weaker_set = weaker_set | poor_list - prior_list

            for index, rule in enumerate(Inital_rule):
                if index not in weaker_set:
                    Inital_rule[index].DefeasibleRule_priorUp()

            for prefernece_tuple in preference:
                if prefernece_tuple[1] in weaker_set:
                    copy_perfence.discard(prefernece_tuple)

        return Inital_rule


    def underCutting_Argument(self, argument: Argument):
        """
            This inital the defeasible level of defeasible rule by the preference.
            the tuple(1,0) means rules[1] covers rules[0]
        """
        search_list = []
        for spt in argument.support:
            if isinstance(spt,Argument):
                search_list.append(spt)

        underCutting_index = 0
        Cutting_argument = None
        while len(search_list) > 0:
            temp_argument = search_list.pop()
            if temp_argument.Applied_rule != -1:
                if self.rules[underCutting_index].defeasible_level > self.rules[temp_argument.Applied_rule].defeasible_level:
                    underCutting_index = temp_argument.Applied_rule
                    Cutting_argument = temp_argument
            for spt in temp_argument.support:
                if isinstance(spt, Argument):
                    search_list.append(spt)
        return underCutting_index, Cutting_argument

    def sort_argument(self, Argument_set: set([Argument])):
        sorted_Arguments = []
        for Arg in Argument_set:
            underCutting_index, Cutting_argument = self.underCutting_Argument(Arg)
            defeasiblility = self.rules[underCutting_index].defeasible_level
            sorted_Arguments.append((defeasiblility, Arg))

        sorted(sorted_Arguments, key=lambda Tuple: Tuple[1])
        return sorted_Arguments



















