# this uses pytest https://docs.pytest.org/en/latest/

from propositional_logic import *


def test():
    # B or not B
    shakespeare = Or('B', Not('B'))
    assert str(shakespeare) == '(B ∨ (¬B))'
    assert shakespeare.truthtable() == [({'B': True}, True),
                                        ({'B': False}, True)]

    # A implies B
    impl = Implies('A', 'B')
    assert str(impl) == '(A → B)'
    assert impl.truthtable() == [({'A': True, 'B': True}, True),
                                 ({'A': True, 'B': False}, False),
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
