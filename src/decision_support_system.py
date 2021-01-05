from propositional_parser import toProposition
from defeasible_tableau import Tableau

class DecisionSupportSystem:
    """
    Decision Support System
    """

    def __init__(self,
                 question: Proposition,
                 initial_information: Set[Proposition] = set(),
                 rules: Set[Rule] = set()
                 ):
        self.question = question
        self.initial_information = initial_information
        self.rules = rules

    def __str__(self):

        return

    def setup(self, proposition):


        return

    def run(self):
        done = false
        results = None

        while not done:
            tableau = Tableau(question=self.question, initial_information=self.initial_information, rules=rules)
            status, return_values = tableau.evaluate()
            if status == 'known':
                pro_arguments, contra_arguments = return_values[0], return_values[1]
                done = true
            elif status == 'unknown':
                self.initial_information.add(self.get_promising_test(tests))

        self.process_results(pro_arguments, contra_arguments)

        return

    def get_promising_tests(self, tests):
        return [tests[0][0]]

    def process_results(pro_arguments, contra_arguments):
        for pro_argument in pro_arguments:
            print(pro_argument)
        for counter_argument in counter_arguments:
            print(counter_argument)
        return