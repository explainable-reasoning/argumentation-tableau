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
    A node is a list of arguments, and a list of child nodes.
    """

    def __init__(self, arguments: List[Argument]):
        self.arguments = arguments
        self.children: List['Node'] = []

    def __str__(self, indent: str = '', parentArguments: List[Argument] = []):
        """
        Does some fancy recursive indented printing. 
        See `__str__` in `propositional_tableau.py` for an explanation how it works.
        """
        return (indent
                + ('\n' + indent).join([str(a) for a in self.arguments
                                        if a not in parentArguments])
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
            simple: List[Argument] = \
                [a for a in self.arguments if not a.conclusion.is_decomposable()]
            # 1.:
            found_new_inconsistency = False
            # Check out all pairs:
            for a in simple:
                for b in simple:
                    # Check whether they are inconsistent:
                    if isinstance(a.conclusion, Not) and a.conclusion.children[0] == b.conclusion:
                        # Create an argument for the inconsistency
                        # by merging the supports of the arguments leading to it:
                        support = list(set(a.support + b.support))
                        if not Argument(support, F()) in self.arguments:
                            self.children.append(
                                Node(
                                    self.arguments +
                                    [Argument(support, F())]
                                )
                            )
                            # We have already created a child, that's enough for now:
                            found_new_inconsistency = True
                            break
            # 2.
            if not found_new_inconsistency:
                # `Complex` refers to arguments with a decomposable conclusion
                # (that is, we can apply a tableau rule there).
                complex: List[Argument] = \
                    [a for a in self.arguments if a.conclusion.is_decomposable()]
                if len(complex) > 0:
                    # We sort the unexpanded propositions,
                    # so that we preferably first decompose those arguments
                    # where this does not lead to forking (=branching).
                    complex_and_forking = \
                        [p for p in complex if p.conclusion.is_forking()]
                    complex_and_not_forking = \
                        [p for p in complex if not p.conclusion.is_forking()]
                    sorted_complex = complex_and_not_forking + complex_and_forking
                    # We only decompose the first one of this list for now.
                    to_be_decomposed = sorted_complex[0]
                    # This creates a list of one or two lists (branches) of lists of arguments.
                    for branch in to_be_decomposed.conclusion.decompose():
                        self.children.append(
                            Node(
                                # We remove the decomposed argument in the child node,
                                # because we don't want to consider it again:
                                [a for a in self.arguments if a != to_be_decomposed]
                                # And we add the new arguments for the respective branch:
                                + [Argument(to_be_decomposed.support, argument)
                                   for argument in branch]
                            )
                        )
        # 3.
        for child in self.children:
            child.expand()

    def arguments_for_inconsistency(self) -> List[Argument]:
        """
        Return all arguments for an inconsistency in the node or in any child node.
        We do this by considering the inconsistencies in the leaf nodes and then merging them together
        in an intricate way on our way back up to the node.
        At each step, we eliminate incosistencies where there are multiple tests in the support, 
        because we won't be able to convert hese inconsistencies into useful constructive arguments later.
        Inconsistencies are arguments with `F()` ("false", or ⟘) in their support.
        """
        arguments: List[Argument] = []
        if len(self.children) == 0:
            # Here we are at a leaf node.
            # We find and return arguments where the conclusion is an inconsistency
            # and where the support includes at most one test.
            
            for a in self.arguments:
                if a.conclusion == F():
                    tests = [s for s in a.support if isinstance(s, Test)]
                    if len(tests) <= 1:
                        arguments.append(a)
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
                    # We merge the combination and eliminate duplicates.
                    merged = list(set(left.support + right.support))
                    # We keep only arguments with at most one test in the support.
                    tests = [s for s in merged if isinstance(s, Test)]
                    if len(tests) <= 1:
                        # And from the merged support we create 
                        # another argument for an inconsistency:
                        arguments.append(Argument(merged, F()))
        # Keep only unique arguments.
        return list(set(arguments))

    def arguments_for_and_against(self, p: Proposition):
        """
        Returns all arguments related to p:
        Those in favour of p, those opposing p.
        The argumentation framework will need to take care of them later.
        """
        arguments_for: List[Argument] = []
        arguments_against: List[Argument] = []
        # `negated` is `Not(p)`, while avoiding a double negation.
        negated = p.children[0] if isinstance(p, Not) else Not(p)
        for a in self.arguments:
            if (a.conclusion == p
                or (isinstance(a.conclusion, Rule)
                    and a.conclusion.consequence == p)):
                arguments_for.append(a)
            elif (a.conclusion == negated
                  or (isinstance(a.conclusion, Rule)
                      and a.conclusion.consequence == negated)):
                arguments_against.append(a)
        return arguments_for, arguments_against

    def add(self, arguments: List[Argument]):
        """
        Adds a list of arguments to the node and all its child nodes.
        """
        self.arguments += arguments
        for child in self.children:
            child.add(arguments)
