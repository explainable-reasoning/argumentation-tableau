from propositional_logic import *
from propositional_tableaux_tree import *
from textwrap import dedent


def test_or():
    node = Node([(Argument(Support(), Or('A', 'B')), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ∨ B)
                            (A ∨ B)
                            A
                            
                            (A ∨ B)
                            B
                        """)


def test_and():
    node = Node([(Argument(Support(), And('A', 'B')), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ∧ B)
                            (A ∧ B)
                            A
                            B
                        """)


def test_or_and():
    node = Node([(Argument(Support(), Or(And('A', 'B'), 'C')), False)])
    node.expandRecursively()
    assert str(node) == dedent("""\
                        ((A ∧ B) ∨ C)
                            ((A ∧ B) ∨ C)
                            (A ∧ B)
                                ((A ∧ B) ∨ C)
                                (A ∧ B)
                                A
                                B

                            ((A ∧ B) ∨ C)
                            C
                        """)


def test_and_or():
    node = Node([(Argument(Support(), And(Or('A', 'B'), 'C')), False)])
    node.expandRecursively()
    assert str(node) == dedent("""\
                        ((A ∨ B) ∧ C)
                            ((A ∨ B) ∧ C)
                            (A ∨ B)
                            C
                                ((A ∨ B) ∧ C)
                                (A ∨ B)
                                C
                                A

                                ((A ∨ B) ∧ C)
                                (A ∨ B)
                                C
                                B
                        """)


def test_implies():
    node = Node([(Argument(Support(), Implies('A', 'B')), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A → B)
                            (A → B)
                            (¬A)

                            (A → B)
                            B
                        """)


def test_equal():
    node = Node([(Argument(Support(), Equal('A', 'B')), False)])
    node.expand()
    assert str(node) == dedent("""\
                        (A ↔ B)
                            (A ↔ B)
                            (A → B)

                            (A ↔ B)
                            (B → A)
                        """)
