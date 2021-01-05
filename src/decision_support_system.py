from propositional_parser import toProposition
from defeasible_tableau import Tableau

class DecisionSupportSystem:
    """
    Decision Support System
    """

    ### preliminary in file config
    io = 'TODO ADD HERE'
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

        while not done:
            tableau = Tableau(question=self.question, initial_information=self.initial_information, rules=rules)
            status, return_values = tableau.evaluate()
            if status == 'known':
                pro_arguments, counter_arguments = return_values[0], return_values[1]
                done = True
            elif status == 'unknown':
                self.initial_information.add(self.get_promising_test(tests))

        self.process_results(pro_arguments, counter_arguments)

        return

    def get_promising_tests(self, tests):
        test_counter = []
        for branch_tests in tests:
            for test in branch_tests:
                if test not in test_counter.keys():
                    test_counter[test] = 0
                test_counter[test] = test_counter[test] + 1
        return [tests[0][0]]

    def ask_question(self, test):
        if not io.ask(test):
            test = '¬' + test
            self.initial_information.add(test)
        return

    def process_results(pro_arguments, counter_arguments):
        for pro_argument in pro_arguments:
            print(pro_argument)
        for counter_argument in counter_arguments:
            print(counter_argument)
        return