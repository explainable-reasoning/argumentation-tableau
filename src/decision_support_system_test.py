from defeasible_tableau import *
from reasoning_elements import *
from propositional_parser import *
import pytest

def str_list(l):
    return [str(a) for a in l]

def test_example_one():
    tableau = Tableau(
        question=parse('d'),
        initial_information=[parse('((a or b) and c) -> d')])
    #pro, contra = tableau.evaluate()
    #print(str_list(pro))
    #assert

    tableau = Tableau(
        question=parse('e'),
        initial_information=[parse('((a and b) or (c and d)) -> e')]
    )
    #pro, contra = tableau.evaluate()
    #print(str_list(pro))
    # assert

    tableau = Tableau(
        question=parse('c'),
        initial_information=[parse('((a and b) or c) -> c')]
    )
    #pro, contra = tableau.evaluate()
    #print(str_list(pro))
    #assert

def test_defeasible_rules():
    tableau = Tableau(
        question=parse('f'),
        initial_information=[],
        rules=[
            Rule(
                parse('a or b'),
                parse('c')
            ),
            Rule(
                parse('c'),
                parse('f')
            ),
            Rule(
                parse('x'),
                parse('¬f')
            ),
            Rule(
                parse('y'),
                parse('z')
            )
        ]
    )
    preference = [
        (2, 1)
    ]


def read_file(filename):
    with open(filename, 'r') as reader:
        for line in reader:
            print(line)

#read_file('example.txt')

