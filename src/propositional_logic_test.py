# this uses pytest https://docs.pytest.org/en/latest/

from propositional_logic import *


def test():
    # B or not B
    shakespeare = Or('B', Not('B'))
    assert str(shakespeare) == '(B ∨ (¬B))'
    assert shakespeare.truthtable() == [({'B': True}, True),
                                        ({'B': False}, True)]

    # A or B
    aorb = Or('A', 'B')
    assert str(aorb) == '(A ∨ B)'
    assert aorb.truthtable() == [({'A': True, 'B': True}, True),
                                 ({'A': True, 'B': False}, True),
                                 ({'A': False, 'B': True}, True),
                                 ({'A': False, 'B': False}, False)]

    # A or not B
    aornb = Or('A', Not('B'))
    assert str(aornb) == '(A ∨ (¬B))'
    assert aornb.truthtable() == [({'A': True, 'B': True}, True),
                                 ({'A': True, 'B': False}, True),
                                 ({'A': False, 'B': True}, False),
                                 ({'A': False, 'B': False}, True)]

    # not A or B
    naorb = Or(Not('A'), 'B')
    assert str(naorb) == '((¬A) ∨ B)'
    assert naorb.truthtable() == [({'A': True, 'B': True}, True),
                                  ({'A': True, 'B': False}, False),
                                  ({'A': False, 'B': True}, True),
                                  ({'A': False, 'B': False}, True)]

    # not A or not B
    naornb = Or(Not('A'), Not('B'))
    assert str(naornb) == '((¬A) ∨ (¬B))'
    assert naornb.truthtable() == [({'A': True, 'B': True}, False),
                                 ({'A': True, 'B': False}, True),
                                 ({'A': False, 'B': True}, True),
                                 ({'A': False, 'B': False}, True)]

    # A implies B
    impl = Implies('A', 'B')
    assert str(impl) == '(A → B)'
    assert impl.truthtable() == [({'A': True, 'B': True}, True),
                                 ({'A': True, 'B': False}, False),
                                 ({'A': False, 'B': True}, True),
                                 ({'A': False, 'B': False}, True)]

    # A implies not B
    implnb = Implies('A', Not('B'))
    assert str(implnb) == '(A → (¬B))'
    assert implnb.truthtable() == [({'A': True, 'B': True}, False),
                                 ({'A': True, 'B': False}, True),
                                 ({'A': False, 'B': True}, True),
                                 ({'A': False, 'B': False}, True)]

    # A and B and C
    multiconj = And('A', And('B', 'C'))
    assert str(multiconj) == '(A ∧ (B ∧ C))'
    assert multiconj.truthtable() == [({'A': True, 'B': True, 'C': True}, True),
                                      ({'A': True, 'B': True, 'C': False}, False),
                                      ({'A': True, 'B': False, 'C': True}, False),
                                      ({'A': True, 'B': False, 'C': False}, False),
                                      ({'A': False, 'B': True, 'C': True}, False),
                                      ({'A': False, 'B': True, 'C': False}, False),
                                      ({'A': False, 'B': False, 'C': True}, False),
                                      ({'A': False, 'B': False, 'C': False}, False)]

    # A and not B and C
    multiconjnb = And('A', And(Not('B'), 'C'))
    assert str(multiconjnb) == '(A ∧ ((¬B) ∧ C))'
    assert multiconjnb.truthtable() == [({'A': True, 'B': True, 'C': True}, False),
                                      ({'A': True, 'B': True, 'C': False}, False),
                                      ({'A': True, 'B': False, 'C': True}, True),
                                      ({'A': True, 'B': False, 'C': False}, False),
                                      ({'A': False, 'B': True, 'C': True}, False),
                                      ({'A': False, 'B': True, 'C': False}, False),
                                      ({'A': False, 'B': False, 'C': True}, False),
                                      ({'A': False, 'B': False, 'C': False}, False)]

    # (A and B) imply C
    abimplyc = Implies(And('A','B'), 'C')
    assert str(abimplyc) == '((A ∧ B) → C)'
    assert abimplyc.truthtable() == [({'A': True, 'B': True, 'C': True}, True),
                                      ({'A': True, 'B': True, 'C': False}, False),
                                      ({'A': True, 'B': False, 'C': True}, True),
                                      ({'A': True, 'B': False, 'C': False}, True),
                                      ({'A': False, 'B': True, 'C': True}, True),
                                      ({'A': False, 'B': True, 'C': False}, True),
                                      ({'A': False, 'B': False, 'C': True}, True),
                                      ({'A': False, 'B': False, 'C': False}, True)]

    # (A or B) and C
    orand = And(Or('A','B'),'C')
    assert str(orand) == '((A ∨ B) ∧ C)'
    assert orand.truthtable() == [({'A': True, 'B': True, 'C': True}, True),
                                      ({'A': True, 'B': True, 'C': False}, False),
                                      ({'A': True, 'B': False, 'C': True}, True),
                                      ({'A': True, 'B': False, 'C': False}, False),
                                      ({'A': False, 'B': True, 'C': True}, True),
                                      ({'A': False, 'B': True, 'C': False}, False),
                                      ({'A': False, 'B': False, 'C': True}, False),
                                      ({'A': False, 'B': False, 'C': False}, False)]

    # (A and B) or C
    andor = Or(And('A', 'B'), 'C')
    assert str(andor) == '((A ∧ B) ∨ C)'
    assert andor.truthtable() == [({'A': True, 'B': True, 'C': True}, True),
                                      ({'A': True, 'B': True, 'C': False}, True),
                                      ({'A': True, 'B': False, 'C': True}, True),
                                      ({'A': True, 'B': False, 'C': False}, False),
                                      ({'A': False, 'B': True, 'C': True}, True),
                                      ({'A': False, 'B': True, 'C': False}, False),
                                      ({'A': False, 'B': False, 'C': True}, True),
                                      ({'A': False, 'B': False, 'C': False}, False)]

    # A equals B
    equal = Equal('A','B')
    assert str(equal) == '(A ↔ B)'
    assert equal.truthtable() == [({'A': True, 'B': True}, True),
                                 ({'A': True, 'B': False}, False),
                                 ({'A': False, 'B': True}, False),
                                 ({'A': False, 'B': False}, True)]

    # True implies X
    impl2 = Implies(T(), 'X')
    assert str(impl2) == '(True → X)'
    assert impl2.truthtable() == [({'X': True}, True), ({'X': False}, False)]

    # False implies Y
    impl3 = Implies(F(), 'Y')
    assert str(impl3) == '(False → Y)'
    assert impl3.truthtable() == [({'Y': True}, True), ({'Y': False}, True)]


    # True
    t = T()
    assert str(t) == 'True'
    assert t.truthtable() == [({}, True)]

    # False
    f = F()
    assert str(f) == 'False'
    assert f.truthtable() == [({}, False)]
