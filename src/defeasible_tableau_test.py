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
    _, (pro, contra) = tableau.evaluate()
    assert str_list(pro) == ['({a}, a)']
    assert str_list(contra) == []

    tableau = Tableau(
        question=parse('a'),
        initial_information=[parse('¬a')]
    )
    _, (pro, contra) = tableau.evaluate()
    assert str_list(pro) == []
    assert str_list(contra) == ['({¬a}, ¬a)']

    tableau = Tableau(
        question=parse('¬a'),
        initial_information=[parse('a')]
    )
    _, (pro, contra) = tableau.evaluate()
    assert str_list(pro) == []
    assert str_list(contra) == ['({a}, a)']

    tableau = Tableau(
        question=parse('¬a'),
        initial_information=[parse('¬a')],
    )
    _, (pro, contra) = tableau.evaluate()
    assert str_list(pro) == ['({¬a}, ¬a)']
    assert str_list(contra) == []


def test_simple_nondefeasible_tautology():
    tableau = Tableau(question=parse('True'))
    _, (pro, contra) = tableau.evaluate()
    assert str_list(pro) == ['({}, True)']
    assert str_list(contra) == []


def test_simple_nondefeasible_contradiction():
    """
    The tableau does not find a counterargument to a contradiction.
    TODO Is this desired behaviour?
    """
    tableau = Tableau(question=parse('¬True'))
    result, _ = tableau.evaluate()
    assert result == 'unknown'


def test_complex_nondefeasible_proposition():
    """
    Cf. `test_propositional_tableau.py`
    """
    tableau = Tableau(
        question=parse('(p ∨ (q ∧ r)) → ((p ∨ q) ∧ (p ∨ r))')
    )
    _, (pro, contra) = tableau.evaluate()
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
    _, (pro, contra) = tableau.evaluate()
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
    _, (pro, contra) = tableau.evaluate()
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
    _, (pro, contra) = tableau.evaluate()
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
        question=parse('s')
    )
    _, (pro, contra) = tableau.evaluate()
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
        question=parse('q')
    )
    _, (pro, contra) = tableau.evaluate()
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
    _, (pro, contra) = tableau.evaluate()
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
        question=parse('¬CanMakeRequestForChange')
    )
    preference = [
        (1, 0),  # R2 > R1
        (2, 0),  # R3 > R1
        (3, 0),  # R4 > R1
    ]
    _, (pro, contra) = tableau.evaluate()
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
        ]
    )
    preference = [
        (1, 0),  # R2 > R1
        (2, 0),  # R3 > R1
        (3, 0),  # R4 > R1
        (5, 2),
        (5, 3),

    ]
    pro, contra = tableau.evaluate()
    print(pro)
    print(contra)
    assert str_list(pro) == [
        '({{Employed}, Employed ~> CanMakeRequestForChange)} CanMakeRequestForChange ~> LEGAL_RequestedChangeWorkingHours)'
    ]
    assert str_list(contra) == []

# Information from open branches

@skip
def test_unknown_information():
    tableau = Tableau(
        question=parse('b'),
        initial_information=[
            parse('a -> b')
        ]
    )
    assert tableau.get_undecided_propositions() == {
        frozenset({'a', 'b'})
    }

    tableau = Tableau(
        question=parse('c'),
        initial_information=[
            parse('(a and b) -> c')
        ]
    )
    assert tableau.get_undecided_propositions() == {
        frozenset({'a', 'c'}),
        frozenset({'b', 'c'})
    }

    tableau = Tableau(
        question=parse('c'),
        initial_information=[
            parse('(a or b) -> c')
        ]
    )
    assert tableau.get_undecided_propositions() == {
        frozenset({'a', 'b', 'c'})
    }

    tableau = Tableau(
        question=parse('d'),
        initial_information=[
            parse('((a or b) and c) -> d')
        ]
    )
    assert tableau.get_undecided_propositions() == {
        frozenset({'a', 'b', 'd'}),
        frozenset({'c', 'd'})
    }

    tableau = Tableau(
        question=parse('d'),
        initial_information=[
            parse('((a or b) and c) -> d'),
            parse('e -> f')
        ]
    )
    assert tableau.get_undecided_propositions() == {
        frozenset({'a', 'b', 'e', 'd'}),
        frozenset({'a', 'b', 'f', 'd'}),
        frozenset({'c', 'e', 'd'}),
        frozenset({'c', 'f', 'd'})
    }

    tableau = Tableau(
        question=parse('d'),
        initial_information=[
            parse('((a or b) and c) -> d'),
            parse('x -> ((a and b) and c)')
        ]
    )
    assert tableau.get_undecided_propositions() == {
        frozenset({'a', 'b', 'x', 'd'}),
        frozenset({'c', 'x', 'd'})
    }

'''
##British Nationality Act
def test_british_nationality_act():
    tableau = Tableau(
        question=
        initial_information=[

        ],
        rules =[
            #Section 1.1
            Rule(
                parse('BornInUK & BornAfterCommencement & PartentBritishCitizen'),
                parse('BritishCitizen')
            ),
            #Section 1.2
            Rule(
                parse('FoundAsNewbornInUK & FoundAfterCommencement & ¬KnownToBeBornInNotUK & ¬ParentKnownNotBritish'),
                parse('BritishCitizen')
            )
            #Section 1.3
            Rule(
                parse('BornInUK & IsMinor & EntitledToBeRegistered & ApplicationToBeRegistered'),
                parse('BritishCitizen')
            )
            Rule(
                parse('ParentBritishCitizen'),
                parse('EntitledToBeRegistered')
            )
            Rule(
                parse('ParentSettledInUnitedKingdom'),
                parse('EntitledToBeRegistered')
            )
            Rule(
                parse('ParentInArmedForces'),
                parse('EntitledToBeRegistered')
            )
        ]
    ) '''