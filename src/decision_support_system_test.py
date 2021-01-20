from decision_support_system import DecisionSupportSystem
from defeasible_tableau import *
from propositional_parser import *
from reasoning_elements import *

from TEMP_file_reader import Configuration


def str_list(l):
    return [str(a) for a in l]

def test_example_one():
    decisionSupportSystem = DecisionSupportSystem(
        question=parse('d'),
        initial_information=[parse('((a or b) and c) -> d')])
    decisionSupportSystem.run()

def test_example_two():
    decisionSupportSystem = DecisionSupportSystem(
        question=parse('e'),
        initial_information=[parse('((a and b) or (c and d)) -> e')]
    )
    decisionSupportSystem.run()

def test_example_three():
    decisionSupportSystem = DecisionSupportSystem(
        question=parse('c'),
        initial_information=[parse('((a and b) or c) -> c')]
    )
    decisionSupportSystem.run()

def test_defeasible_rules():
    decisionSupportSystem = DecisionSupportSystem(
        question=parse('¬f'),
        initial_information=[],
        rules=[
            Rule(
                parse('(a or b)'),
                parse('c')
            ),
            Rule(
                parse('c and x'),
                parse('f')
            ),
            Rule(
                parse('x or c'),
                parse('¬f')
            )
        ]
    )
    decisionSupportSystem.run()
    preference = [
        (2, 1)
    ]

def test_logic_example_2():
    """
    Source: Mail by Nico
    """
    decisionSupportSystem = DecisionSupportSystem(
        initial_information=[
            #parse('p')
        ],
        rules=[
            Rule(
                parse('p'),
                parse('q')
            ),
            Rule(
                parse('q'),
                parse('r')
            ),
            Rule(
                parse('r'),
                parse('¬q')
            )
        ],
        question=parse('q')
    )
    decisionSupportSystem.run()

### Test Code
def main():
    #test_logic_example_2()
    #test_example_one()
    #return
    #test_example_two()
    #test_example_three()
    test_law_example()
    #test_BNA()
    #test_cremers()



def test_law_example():
    """
    Tomas Cremers (2016), Appendix C.1
    """
    decisionSupportSystem = DecisionSupportSystem(
        initial_information=[

        ],
        rules=[
            Rule(
                parse('Employed'),
                parse('CanMakeRequestForChange')
            ),
            Rule(
                parse('Employed & LessThanTenEmployees'),
                parse('¬CanMakeRequestForChange')
            ),
            Rule(
                parse('Employed & ReachedOldAgeInsurance'),
                parse('¬CanMakeRequestForChange')
            ),
            Rule(
                parse('Employed & MilitaryOfficial'),
                parse('¬CanMakeRequestForChange')
            )
        ],
        question=parse('¬CanMakeRequestForChange')
    )
    decisionSupportSystem.run()

def test_BNA():
    config = Configuration()
    a, b = config.parse_json("./sample_rule_sets/british_national_act.json")
    #rules = set(a)
    #initial = set(b)
    rules = set()
    initial = set()
    for i in a:
        rules.add(i)
    for j in b:
        initial.add(j)
    #print(type(set(a)))
    #print(type(set(b)))
    decisionSupportSystem = DecisionSupportSystem(
        initial_information=[],
        rules=rules,
        question=parse('BritishCitizen')
    )
    decisionSupportSystem.run()

def test_cremers():
    config = Configuration()
    a, b = config.parse_json("./sample_rule_sets/cremers_example.json")
    rules = set(a)
    initial = set(b)
    decisionSupportSystem = DecisionSupportSystem(
        initial_information=[],
        rules=rules,
        question=parse('LEGAL_RequestedChangeWorkingHours')
    )
    decisionSupportSystem.run()


main()