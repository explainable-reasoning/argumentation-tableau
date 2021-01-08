from propositional_parser import toProposition
from reasoning_elements.proposition import Proposition
from reasoning_elements.rule import *
from defeasible_tableau import Tableau
from i_o.user_input import *

class DecisionSupportSystem:
    """
    Decision Support System
    """

    ### preliminary in file config
    io = UserInput()
    ###

    def __init__(self,
                 question: Proposition,
                 initial_information: Set[Proposition] = set(),
                 rules: Set[Rule] = set(),
                 ):
        self.question = question
        self.initial_information = initial_information
        self.rules = rules

    def __str__(self):

        return

    def setup(self, proposition):


        return

    def run(self):
        done = False
        pro_arguments = []
        counter_arguments = []

        while not done:
            tableau = Tableau(question=self.question, initial_information=self.initial_information, rules=self.rules)
            status, return_values = tableau.evaluate()
            if status == 'known':
                pro_arguments, counter_arguments = return_values[0], return_values[1]
                done = True
            elif status == 'unknown':
                self.ask_question(self.get_promising_tests(return_values))

        self.process_results(pro_arguments, counter_arguments)

        return

    def get_promising_tests(self, tests):
        test_counter = {}
        for branch_tests in tests:
            for test in branch_tests:
                if test not in test_counter.keys():
                    test_counter[test] = 0
                test_counter[test] = test_counter[test] + 1

        ordered_by_frequency = {k: v for k, v in sorted(test_counter.items(), key=lambda item: item[1])}
        return list(ordered_by_frequency.keys())[0]

    def ask_question(self, test: Proposition):
        if not self.io.ask(test):
            test = test.negate()
        self.initial_information.append(test)
        return

    def process_results(self, pro_arguments, counter_arguments):
        for pro_argument in pro_arguments:
            print(pro_argument)
        for counter_argument in counter_arguments:
            print(counter_argument)
        return