from reasoning_elements.proposition import *
from propositional_parser import toProposition
from typing import Tuple, List


def is_valid(proposition) -> bool:
    """
    Checks whether an argument is valid:
    Whether the conclusion holds in every possible situation, given the support.
    """
    tableau = Tableau(Not(toProposition(proposition)))
    return tableau.is_invalid()


def is_satisfiable(proposition) -> bool:
    """
    Checks whether a proposition is satisfiable:
    Whether it is true in at least one possible situation, given the support.
    """
    tableau = Tableau(toProposition(proposition))
    return not tableau.is_invalid()


class Tableau:
    root: 'Node'

    def __init__(self, proposition):
        self.root = Node([toProposition(proposition)])
        self.root.expandRecursively()

    def __str__(self):
        return str(self.root)

    def is_invalid(self) -> bool:
        return self.root.is_invalid()


class Node:
    """
    Node of a propositional tableau.
    Can be expanded, and then it may have child nodes.
    """
    arguments: List[Proposition]

    children: List['Node']

    closed: bool

    def __init__(self, propositions: List[Proposition]):
        self.propositions = propositions
        self.children = []
        self.closed = False

    def __str__(self, indent='', parentPropositions=[]):
        """
        Stringifies a node and its child nodes in the shape of a tree.
        Optional arguments:
        - An indent. For the tree shape, every node will just call the string method of its child nodes, with a bigger indent.
        - The propositions of the parent. These will be ignored for the output string, since they would be redundant.
        Multiple propositions within one node will be printed in consecutive lines.
        Multiple nodes are separated by a blank line.
        """
        propositions = [str(p) for p in self.propositions]
        return (indent
                + ('\n' + indent).join([p for p in propositions
                                        if p not in parentPropositions])
                + '\n'
                + (indent + '❌\n' if self.closed else "")
                + '\n'.join([child.__str__(indent + '    ', propositions) for child in self.children]))

    def expand(self):
        """
        Expands the next unexpanded argument.
        This means roughly that child nodes are added, where the unexpanded propositions will be replaced using the rewriting rules of propositonal tableau.
        One proposition is expanded at a time. If there are propositions whose expansion is non-branching, they will be considered first, to reduce redundancy in the new branches.
        """
        simple: List[Proposition] = \
            [p for p in self.propositions if not p.is_decomposable()]
        # check for incosistencies in the simple propositions:
        for a, b in itertools.product(simple, simple):
            if isinstance(a, Not) and str(a.children[0]) == str(b):
                self.closed = True
                return
        complex: List[Proposition] = \
            [p for p in self.propositions if p.is_decomposable()]
        if len(complex) > 0:
            # sort the unexpanded propositions,
            # so that those propositions that fork a branch are treated last:
            complex_and_forking = \
                [p for p in complex if p.is_forking()]
            complex_and_not_forking = \
                [p for p in complex if not p.is_forking()]
            sorted_complex = complex_and_not_forking + complex_and_forking
            to_be_decomposed = sorted_complex[0]
            for branch_propositions in to_be_decomposed.decompose():
                self.children.append(Node(
                    [p for p in self.propositions if str(
                        p) != str(to_be_decomposed)]
                    + branch_propositions))

    def expandRecursively(self):
        self.expand()
        for child in self.children:
            child.expandRecursively()

    def is_invalid(self):
        self.expandRecursively()
        if len(self.children) > 0:
            return all([child.is_invalid() for child in children])
        else:
            return self.closed
