from typing import *
from defeasible_tableau import *
from reasoning_elements import *
from propositional_parser import *
import pytest

# Run all tests with `poetry run pytest src`.
# Annotate tests with `@skip` to skip them.
skip = pytest.mark.skip


# HELPER

def str_list(l):
    return [str(a) for a in l]


# SIMPLE TESTS

def test_simple_nondefeasible_proposition():
    tableau = Tableau(
        question=parse('a'),
        initial_information=[parse('a')]
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == ['({a}, a)']
    assert str_list(contra) == []

    tableau = Tableau(
        question=parse('a'),
        initial_information=[parse('¬a')]
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == []
    assert str_list(contra) == ['({¬a}, ¬a)']

    tableau = Tableau(
        question=parse('¬a'),
        initial_information=[parse('a')]
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == []
    assert str_list(contra) == ['({a}, a)']

    tableau = Tableau(
        question=parse('¬a'),
        initial_information=[parse('¬a')],
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == ['({¬a}, ¬a)']
    assert str_list(contra) == []


def test_simple_nondefeasible_tautology():
    tableau = Tableau(question=parse('True'))
    pro, contra = tableau.evaluate()
    assert str_list(pro) == ['({}, True)']
    assert str_list(contra) == []


def test_simple_nondefeasible_contradiction():
    """
    The tableau does not find a counterargument to a contradiction. 
    TODO Is this desired behaviour?
    """
    tableau = Tableau(question=parse('¬True'))
    pro, contra = tableau.evaluate()
    assert str_list(pro) == []
    assert str_list(contra) == []


def test_complex_nondefeasible_proposition():
    """
    Cf. `test_propositional_tableau.py`
    """
    tableau = Tableau(
        question=parse('(p ∨ (q ∧ r)) → ((p ∨ q) ∧ (p ∨ r))')
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        '({}, (p ∨ (q ∧ r)) → ((p ∨ q) ∧ (p ∨ r)))'
    ]
    assert str_list(contra) == []


def test_apply_1_rule():
    tableau = Tableau(
        question=parse('b'),
        initial_information=[parse('a')],
        rules=[Rule(parse('a'), parse('b'))]
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == ['({({a}, a ~> b)}, b)']
    assert str_list(contra) == []


def test_chain_2_rules():
    tableau = Tableau(
        question=parse('c'),
        initial_information=[parse('a')],
        rules=[
            Rule(parse('a'), parse('b')),
            Rule(parse('b'), parse('c'))
        ]
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == ['({({({a}, a ~> b)}, b ~> c)}, c)']
    assert str_list(contra) == []


def test_chain_3_rules():
    tableau = Tableau(
        question=parse('d'),
        initial_information=[parse('a')],
        rules=[
            Rule(parse('a'), parse('b')),
            Rule(parse('b'), parse('c')),
            Rule(parse('c'), parse('d'))
        ]
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == ['({({({({a}, a ~> b)}, b ~> c)}, c ~> d)}, d)']
    assert str_list(contra) == []


# LOGIC EXAMPLES

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
        question=parse('s'),
        preference=[
            (1, 2)
        ]
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        '({({({p ∨ q, ¬q}, p ~> r), p ∨ q, ¬q}, r ~> s)}, s)',  # TODO
        '({({({p ∨ q, ¬q}, p ~> r)}, r ~> s)}, s)'
    ]
    assert str_list(contra) == []


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
        question=parse('q'),
        preference=[
            (0, 1),  # R2 > R1
            (1, 2),  # R3 > R1
        ]

    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        '({({p}, p ~> q)}, q)'
    ]
    assert str_list(contra) == [
        '({({({({p}, p ~> q)}, q ~> r)}, r ~> ¬q)}, ¬q)'
    ]


@skip
def test_logic_example_3():
    """
    Source: from Nico's paper at page at page 13
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
        question=parse('s'),
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        'TODO'
    ]
    assert str_list(contra) == [
        'TODO'
    ]


# LAW EXAMPLES

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
        question=parse('¬CanMakeRequestForChange'),
        preference = [
        (1, 0),  # R2 > R1
        (2, 0),  # R3 > R1
        (3, 0),  # R4 > R1
    ]
    )
    pro, contra = tableau.evaluate()
    assert str_list(pro) == [
        '({({Employed, MilitaryOfficial}, Employed ∧ MilitaryOfficial ~> ¬CanMakeRequestForChange)}, ¬CanMakeRequestForChange)'
    ]
    assert str_list(contra) == [
        '({({Employed}, Employed ~> CanMakeRequestForChange)}, CanMakeRequestForChange)'
    ]


@skip
def test_law_example_2():
    """
    Tomas Cremers, Appendix C.2
    """
    tableau = Tableau(
        question=parse('LEGAL_RequestedChangeWorkingHours'),
        initial_information=[
            parse('Employed'),
            parse('¬LessThanTenEmployees'),
            parse('¬ReachedOldAgeInsurance'),
            parse('¬MilitaryOfficial'),
            parse('WorkedForAtLeastTwentySixWeeks'),
            parse('TimeSinceLastRequestMinOneYear'),
            parse('RequestSubmittedInWriting'),
            parse('¬UnforseenCircumstances'),
            parse('DOES_RequestChangeWorkingHours'),
            parse('DOES_RequestChangeWorkingTimes'),
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
            ),
            Rule(
                parse('Employed & UnforseenCircumstances'),
                parse('CanMakeRequestForChange')
            ),
            Rule(
                parse('CanMakeRequestForChange & DOES_RequestChangeWorkingHours'),
                parse('LEGAL_RequestedChangeWorkingHours')
            ),
            Rule(
                parse(
                    'CanMakeRequestForChange & DOES_RequestChangeWorkingHours & (¬RequestSubmittedInWriting)'),
                parse('¬LEGAL_RequestedChangeWorkingHours')
            ),
            Rule(
                parse(
                    'CanMakeRequestForChange & DOES_RequestChangeWorkingHours & (¬TimeSinceLastRequestMinOneYear)'),
                parse('¬LEGAL_RequestedChangeWorkingHours')
            ),
            Rule(
                parse(
                    'CanMakeRequestForChange & DOES_RequestChangeWorkingHours & (¬WorkedForAtLeastTwentySixWeeks)'),
                parse('¬LEGAL_RequestedChangeWorkingHours')
            ),
            Rule(
                parse(
                    'CanMakeRequestForChange & DOES_RequestChangeWorkingHours &  UnforseenCircumstances'),
                parse('LEGAL_RequestedChangeWorkingHours')
            )
        ],
        preference=[
            (1, 0),  # R2 > R1
            (2, 0),  # R3 > R1
            (3, 0),
            (4, 1),# R4 > R1
            (4, 2),
            (4, 3),
            (6, 5),
            (7, 5),
            (8, 5),
            (9, 6),
            (9, 7),
            (9, 8)
        ]
    )

    pro, contra = tableau.evaluate()
    print(pro)
    print(contra)
    assert str_list(pro) == [
        '({{Employed}, Employed ~> CanMakeRequestForChange)} CanMakeRequestForChange ~> LEGAL_RequestedChangeWorkingHours)'
    ]
    assert str_list(contra) == []


def test_undercutting_argument():
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
        question=parse('q'),
        preference=[
            (0, 1),  # R2 > R1
            (1, 2),  # R3 > R1
        ]

    )
    pro, contra = tableau.evaluate()
    under_cutting = {}
    for argum in contra:
        underCutting_index, Cutting_argument = under_cutting[str(argum)] = tableau.underCutting_Argument(argum)
        assert str(Cutting_argument) == '({({({p}, p ~> q)}, q ~> r)}, r ~> ¬q)'
        assert underCutting_index == 2


def stay_your_grand_law_original_type():
    tableau = Tableau(
        initial_information=[
            parse('a'),
            parse('b'),
            parse('c'),
            parse('k')
        ],
        rules=[
            Rule(
                parse('a & b'),
                parse('k -> d')
            ),
            Rule(
                parse('c'),
                parse('x')
            ),
            Rule(
                parse('d'),
                parse('¬x')
            )
        ],
        question=parse('x'),
        preference=[
            (0, 1),  # R0 > R1
            (2, 1),  # R2 > R1
        ]

    )
    pro, contra = tableau.evaluate()
    arguments_list = tableau.sort_argument(pro + contra)
    most_strong_argument = arguments_list[len(arguments_list) - 1]
    assert most_strong_argument[1] == '({({({a, b}, a ∧ b ~> k → d), k}, d ~> ¬x)}, ¬x)'


def stay_your_grand_law():
    tableau = Tableau(
        initial_information=[
            parse('be_threaten'),
            parse('be_attacked'),
            parse('kill_person'),
            parse('believe_will_be_killed')
        ],
        rules=[
            Rule(
                parse('be_threaten & be_attacked'),
                parse('believe_will_be_killed -> justifiable_defense')
            ),
            Rule(
                parse('kill_person'),
                parse('conviction')
            ),
            Rule(
                parse('justifiable_defense'),
                parse('¬conviction')
            )
        ],
        question=parse('conviction'),
        preference=[
            (0, 1),  # R0 > R1
            (2, 1),  # R2 > R1
        ]

    )
    pro, contra = tableau.evaluate()
    arguments_list = tableau.sort_argument(pro + contra)
    strongest_argument = arguments_list[len(arguments_list) - 1]
    assert strongest_argument[1] == '({({({be_attacked, be_threaten}, be_threaten ∧ be_attacked ~> believe_will_be_killed → justifiable_defense), believe_will_be_killed}, justifiable_defense ~> ¬conviction)}, ¬conviction)'

stay_your_grand_law()