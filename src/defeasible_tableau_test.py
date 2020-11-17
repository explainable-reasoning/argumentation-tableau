from typing import *
from defeasible_tableau import *
from reasoning_elements import *
from propositional_parser import *
import pytest

# Run all tests with `poetry run pytest src`.

# Annotate tests with `@skip` to skip them.
skip = pytest.mark.skip


def str_list(l):
    return [str(a) for a in l]


def test_law_example():
    """
    Tomas Cremers (2016), Appendix C.1
    """
    tableau = Tableau(
        initial_information=[
            parse('Employed'),
            parse('¬LessThanTenEmployees'),
            parse('¬ReachedOldAgeInsurance'),
            parse('MilitaryOfficial'),
            parse('WorkedForAtLeastTwentySixWeeks'),
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
        final_conclusion=parse('¬CanMakeRequestForChange')
    )
    preference = [
        (1, 0),  # R2 > R1
        (2, 0),  # R3 > R1
        (3, 0),  # R4 > R1
    ]
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        '({Employed, MilitaryOfficial}, Employed ∧ MilitaryOfficial ~> ¬CanMakeRequestForChange)'
    ]
    assert str_list(contra) == [
        '({Employed}, Employed ~> CanMakeRequestForChange)'
    ]

@skip
def test_logic_example_1():
    """
    Source: Roos (2016), p. 7-9
    """
    tableau = Tableau(
        initial_information=[
            parse('p ∨ q'),
            parse('¬q'),
        ],
        rules=[
            Rule(
                parse('p'),
                parse('r')
            ),
            Rule(
                parse('r'),
                parse('s')
            )
        ],
        final_conclusion=parse('s')
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        '({({({p ∨ q, ¬q}, p ~> r)}, r ~> s)}, s)'
    ]
    assert str_list(contra) == []


@skip
def test_logic_example_2():
    """
    Source: Mail by Nico
    """
    tableau = Tableau(
        initial_information=[
            parse('p')
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
        final_conclusion=parse('q')
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        '({p}, p ~> q)'
    ]
    assert str_list(contra) == [
        '({({p}, p ~> r), r ~> ¬q)'
    ]


@skip
def test_logic_example_3():
    """
    Source ???
    """
    tableau = Tableau(
        initial_information=[
            parse('¬(p & q)'),
            parse('r ∨ s'),
            parse('t'),
        ],
        rules=[
            Rule(
                parse('r'),
                parse('p')
            ),
            Rule(
                parse('t'),
                parse('q')
            )
        ],
        final_conclusion=parse('s'),
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        'TODO'
    ]
    assert str_list(contra) == [
        'TODO'
    ]
