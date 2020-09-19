from propositional_logic import *
from typing import Tuple, List


class Support:
    def __init__(self, *args):
        pass


class Argument:
    support: Support
    conclusion: Proposition

    def __init__(self, support: Support, conclusion: Proposition):
        self.support = support
        self.conclusion = conclusion


def is_valid(argument: Argument) -> bool:
    """
    Checks whether a proposition is valid: It is true in every possible situation.
    """
    raise NotImplementedError


def is_satisfiable(argument: Argument) -> bool:
    """
    Checks whether a proposition is satisfiable: It is true in at least one possible situation.
    """
    raise NotImplementedError


class Tableau:
    root: 'Node'

    def __init__(self, argument: Argument):
        root = Node([(argument, False)])


class Node:
    # The bool value in the tuple indicates whether the proposition has already been rewritten;
    # since in propositional tableaux, every rule needs be rewritten only once. (Roos, L4AI, p. 34)
    arguments: List[Tuple[Argument, bool]]

    children: List['Node']

    def __init__(self, arguments: List[Tuple[Argument, bool]]):
        """
        arguments: List of tuples of arguments and bools whether already expanded.
        """
        self.arguments = arguments
        self.children = []

    def __str__(self, pad=''):
        return (pad + ('\n'+pad).join([str(arg.conclusion) for (arg, _) in self.arguments]) + '\n'
                + '\n'.join([child.__str__(pad+'    ') for child in self.children]))

    def expand(self):
        for (argument, alreadyRewritten) in self.arguments:
            if not alreadyRewritten:
                s = argument.support
                p = argument.conclusion
                arguments = [
                    (arg, True) if arg == argument
                    else (arg, val)
                    for (arg, val)
                    in self.arguments]
                if isinstance(p, And):
                    self.children.append(
                        Node(arguments + [(Argument(s, child), False) for child in p.children]))
                elif isinstance(p, Or):
                    for child in p.children:
                        self.children.append(
                            Node(arguments + [(Argument(s, child), False)]))
                elif isinstance(p, Implies):
                    self.children.append(
                        Node(arguments + [(Argument(s, Not(p.children[0])), False)]))
                    self.children.append(
                        Node(arguments + [(Argument(s, p.children[1]), False)]))
                elif isinstance(p, Equal):
                    self.children.append(
                        Node(arguments + [(Argument(s, Implies(p.children[0], p.children[1])), False)]))
                    self.children.append(
                        Node(arguments + [(Argument(s, Implies(p.children[1], p.children[0])), False)]))

    def expandRecursively(self):
        self.expand()
        for child in self.children:
            child.expand()
