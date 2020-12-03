from typing import *
from reasoning_elements.proposition import *
from reasoning_elements.rule import *
from reasoning_elements.argument import *
from reasoning_elements.test import *

"""
This file includes much of the logic for the defeasible tableau. 
Note that the propositional tableau currently uses its own Node structure (found inside `propositional_tableau.py`).
"""


class Node:
    """
    A node is a set of arguments, and a list of child nodes.
    """

    def __init__(self, arguments: Set[Argument]):
        self.arguments = arguments
        self.children: List['Node'] = []
        self.processed_information = set()

    def __str__(self, indent: str = '', parentArguments: Set[Argument] = set()):
        """
        Does some fancy recursive indented printing. 
        See `__str__` in `propositional_tableau.py` for an explanation how it works.
        """
        return (indent
                + ('\n' + indent).join({str(a) for a in self.arguments
                                        if a not in parentArguments})
                + '\n'
                + '\n'.join([child.__str__(indent + '    ', self.arguments) for child in self.children]))

    def expand(self):
        """
        If there are no child nodes, tries to create child nodes. 
        Two things will be tried:
            1. It tries to find an inconsistency between any two arguments in the node.
               (This is the last semantic tableau rule, and the only one involving multiple arguments.)
            2. If there are no inconsistencies, just apply the normal semantic tableau rule 
               to the first decomposable argument in the node.
        Either of these two operations will create a child node. 
            3. These child nodes (or the already existing child nodes) will also be expanded subsequently.
        """
        if len(self.children) == 0:
            # `Simple` refers to arguments with atomic propositions, or with negated atomic propositions.
            # We might find inconsistencies between these types of arguments.
            simple: Set[Argument] = \
                {a for a in self.arguments if not a.conclusion.is_decomposable()}
            # 1.:
            found_new_inconsistency = False
            # Check out all pairs:
            for a in simple:
                for b in simple:
                    # Check whether they are inconsistent:
                    if not consistent([a, b]):
                        # Create an argument for the inconsistency
                        # by merging the supports of the arguments leading to it:
                        support = a.support.union(b.support)
                        new_inconsistency = Argument(support, F(), -1)
                        if not new_inconsistency in self.arguments:
                            self.children.append(
                                Node(self.arguments | set([new_inconsistency]))
                            )
                            # We have already created a child, that's enough for now:
                            found_new_inconsistency = True
                            break
            # 2.
            if not found_new_inconsistency:
                # `Complex` refers to arguments with a decomposable conclusion
                # (that is, we can apply a tableau rule there).
                complex: Set[Argument] = self.arguments - simple
                if len(complex) > 0:
                    # We sort the unexpanded propositions,
                    # so that we preferably first decompose those arguments
                    # where this does not lead to forking (=branching).
                    complex_and_forking = \
                        {p for p in complex if p.conclusion.is_forking()}
                    complex_and_not_forking = \
                        {p for p in complex if not p.conclusion.is_forking()}
                    sorted_complex = list(
                        complex_and_not_forking) + list(complex_and_forking)
                    # We only decompose the first one of this list for now.
                    to_be_decomposed = sorted_complex[0]
                    # This creates a list of one or two lists (branches) of lists of arguments.
                    for branch in to_be_decomposed.conclusion.decompose():
                        self.children.append(
                            Node(
                                # We remove the decomposed argument in the child node,
                                # because we don't want to consider it again:
                                {a for a in self.arguments if a != to_be_decomposed}
                                # And we add the new arguments for the respective branch:
                                | {Argument(to_be_decomposed.support, argument, -1)
                                   for argument in branch}
                            )
                        )
        # 3.
        for child in self.children:
            child.expand()

    def arguments_for_inconsistency(self) -> Set[Argument]:
        """
        Return all arguments for an inconsistency in the node or in any child node.
        We do this by considering the inconsistencies in the leaf nodes and then merging them together
        in an intricate way on our way back up to the node.
        At each step, we eliminate incosistencies where there are multiple tests in the support, 
        because we won't be able to convert hese inconsistencies into useful constructive arguments later.
        Inconsistencies are arguments with `F()` ("false", or ⟘) in their support.
        """
        arguments: Set[Argument] = set()
        if len(self.children) == 0:
            # Here we are at a leaf node.
            # We find and return arguments where the conclusion is an inconsistency
            # and where the support includes at most one test.

            for a in self.arguments:
                if a.conclusion == F():
                    tests = {s for s in a.support if isinstance(s, Test)}
                    if len(tests) <= 1:
                        arguments.add(a)
        elif len(self.children) == 1:
            # Here we are in a straight branch.
            # We just pass upwards all the inconsistencies from the only child.
            arguments = self.children[0].arguments_for_inconsistency()
        elif len(self.children) == 2:
            # Here we are at a fork between two branches. This is the most complicated position.
            # The support for the closure of the node is the union of the support for the closure of the children.
            # But: There may be multiple such supports per child!
            # So, we check all combinations of supports from the left and supports from the right:
            for left in self.children[0].arguments_for_inconsistency():
                for right in self.children[1].arguments_for_inconsistency():
                    # We merge the combination.
                    merged = left.support.union(right.support)
                    # We keep only arguments with at most one test in the support.
                    tests = {s for s in merged if isinstance(s, Test)}
                    if len(tests) <= 1:
                        if consistent(merged - tests):
                            arguments.add(Argument(merged, F(), -1))

        return arguments

    def arguments_for_and_against(self, p: Proposition) -> Tuple[Set[Argument], Set[Argument]]:
        """
        Returns all arguments related to p:
        Those in favour of p, those opposing p.
        The argumentation framework will need to take care of them later.
        """
        arguments_for: Set[Argument] = set()
        arguments_against: Set[Argument] = set()
        under_cutting_argument: List[Rule]
        # `negated` is `Not(p)`, while avoiding a double negation.
        negated = p.children[0] if isinstance(p, Not) else Not(p)
        for a in self.arguments:
            tests = {p for p in a.support if isinstance(p, Test)}
            if len(tests) == 0:
                if to_proposition(a) == p:
                    arguments_for.add(a)
                elif to_proposition(a) == negated:
                    arguments_against.add(a)

        return arguments_for, arguments_against

    def add(self, arguments: Set[Argument]):
        """
        Adds a list of arguments to the node and all its child nodes.
        """
        self.arguments.update(arguments)
        for child in self.children:
            child.add(arguments)


def to_proposition(a: Union[Argument, Test, Proposition]) -> Proposition:
    if isinstance(a, Test):
        return a.content
    elif isinstance(a, Argument):
        if isinstance(a.conclusion, Rule):
            return a.conclusion.consequence
        else:
            return a.conclusion
    else:
        return a


def consistent(l):
    for a in l:
        for b in l:
            if (isinstance(to_proposition(a), Not)
                    and (to_proposition(a).children[0] == to_proposition(b)
                         or to_proposition(a).children[0] == T())):
                return False
    return True
