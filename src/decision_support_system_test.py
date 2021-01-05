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


