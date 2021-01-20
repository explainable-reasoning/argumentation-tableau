from defeasible_tableau import *
from reasoning_elements import *
from propositional_parser import *
from decision_support_system import DecisionSupportSystem
import pytest

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
    test_logic_example_2()
    #test_example_one()
    #return
    #test_example_two()
    #test_example_three()
    #test_law_example()



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

main()