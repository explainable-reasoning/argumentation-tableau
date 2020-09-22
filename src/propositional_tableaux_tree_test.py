from propositional_logic import *
from propositional_tableaux_tree import *
from textwrap import dedent


def test_or():
    node = Node([(Or('A', 'B'), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ∨ B)
                            A
                            
                            B
                        """)


def test_and():
    node = Node([(And('A', 'B'), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ∧ B)
                            A
                            B
                        """)


def test_or_and():
    node = Node([(Or(And('A', 'B'), 'C'), False)])
    node.expandRecursively()
    assert str(node) == dedent("""\
                        ((A ∧ B) ∨ C)
                            (A ∧ B)
                                A
                                B

                            C
                        """)


def test_and_or():
    node = Node([(And(Or('A', 'B'), 'C'), False)])
    node.expandRecursively()
    assert str(node) == dedent("""\
                        ((A ∨ B) ∧ C)
                            (A ∨ B)
                            C
                                A

                                B
                        """)


def test_implies():
    node = Node([(Implies('A', 'B'), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A → B)
                            (¬A)

                            B
                        """)


def test_equal():
    node = Node([(Equal('A', 'B'), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ↔ B)
                            (A → B)
                            (B → A)
                        """)


def test_complex():
    # Example from Smullyan 1995, p. 16
    node = Node([(
        Not(
            Implies(
                Or('p', And('q', 'r')),
                And(Or('p', 'q'), Or('p', 'r')))

        ),
        False)])
    node.expandRecursively()
    assert str(node) == dedent("""\
                        (¬((p ∨ (q ∧ r)) → ((p ∨ q) ∧ (p ∨ r))))
                            (p ∨ (q ∧ r))
                            (¬((p ∨ q) ∧ (p ∨ r)))
                                p
                                    (¬(p ∨ q))
                                        (¬p)
                                        (¬q)
                                        ❌

                                    (¬(p ∨ r))
                                        (¬p)
                                        (¬r)
                                        ❌

                                (q ∧ r)
                                    q
                                    r
                                        (¬(p ∨ q))
                                            (¬p)
                                            (¬q)
                                            ❌

                                        (¬(p ∨ r))
                                            (¬p)
                                            (¬r)
                                            ❌
                        """)


def test_expand_nonbranching_first():
    node = Node([
        (Or('A', 'B'), False),
        (And('C', 'D'), False)
    ])
    node.expandRecursively()
    assert str(node) == dedent("""\
                        (A ∨ B)
                        (C ∧ D)
                            C
                            D
                                A

                                B
                        """)
