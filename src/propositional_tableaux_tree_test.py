from propositional_logic import *
from propositional_tableaux_tree import *
from textwrap import dedent


def test_or():
    node = Node([(Argument(Support(), Or('A', 'B')), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ∨ B)
                            A
                            
                            B
                        """)


def test_and():
    node = Node([(Argument(Support(), And('A', 'B')), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ∧ B)
                            A
                            B
                        """)


def test_or_and():
    node = Node([(Argument(Support(), Or(And('A', 'B'), 'C')), False)])
    node.expandRecursively()
    assert str(node) == dedent("""\
                        ((A ∧ B) ∨ C)
                            (A ∧ B)
                                A
                                B

                            C
                        """)


def test_and_or():
    node = Node([(Argument(Support(), And(Or('A', 'B'), 'C')), False)])
    node.expandRecursively()
    assert str(node) == dedent("""\
                        ((A ∨ B) ∧ C)
                            (A ∨ B)
                            C
                                A

                                B
                        """)


def test_implies():
    node = Node([(Argument(Support(), Implies('A', 'B')), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A → B)
                            (¬A)

                            B
                        """)


def test_equal():
    node = Node([(Argument(Support(), Equal('A', 'B')), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ↔ B)
                            (A → B)
                            (B → A)
                        """)


def test_complex():
    # Example from Smullyan 1995, p. 16
    node = Node([(Argument(
        Support(),
        Not(
            Implies(
                Or('p', And('q', 'r')),
                And(Or('p', 'q'), Or('p', 'r')))
        )
    ), False)])
    node.expandRecursively()
    # Smullyan's solutions is slightly different, since they expand the nodes in different order.
    # I think this solution is more systematic (though slightly more verbose).
    assert str(node) == dedent("""\
                        (¬((p ∨ (q ∧ r)) → ((p ∨ q) ∧ (p ∨ r))))
                            (p ∨ (q ∧ r))
                            (¬((p ∨ q) ∧ (p ∨ r)))
                                p
                                (¬(p ∨ q))
                                    (¬p)
                                    (¬q)
                                    ❌

                                p
                                (¬(p ∨ r))
                                    (¬p)
                                    (¬r)
                                    ❌

                                (q ∧ r)
                                (¬(p ∨ q))
                                    q
                                    r
                                    (¬p)
                                    (¬q)
                                    ❌

                                (q ∧ r)
                                (¬(p ∨ r))
                                    q
                                    r
                                    (¬p)
                                    (¬r)
                                    ❌
                        """)


def test_expand_nonbranching_first():
    node = Node([
        (Argument(Support(), Or('A', 'B')), False),
        (Argument(Support(), And('C', 'D')), False)
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
