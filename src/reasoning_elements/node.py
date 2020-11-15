from typing import *
from reasoning_elements.proposition import *
from reasoning_elements.rule import *
from reasoning_elements.argument import *
from reasoning_elements.test import *


class Node:

    def __init__(self, arguments: List[Argument]):
        self.arguments = arguments
        self.children: List['Node'] = []

    def __str__(self, indent: str = '', parentArguments: List[Argument] = []):
        return (indent
                + ('\n' + indent).join([str(a) for a in self.arguments
                                        if a not in parentArguments])
                + '\n'
                + '\n'.join([child.__str__(indent + '    ', self.arguments) for child in self.children]))

    def expand(self):
        if len(self.children) == 0:
            simple: List[Argument] = \
                [a for a in self.arguments if not a.conclusion.is_decomposable()]
            # check for incosistencies in the simple propositions:
            found_new_inconsistency = False
            for a, b in itertools.product(simple, simple):
                if isinstance(a.conclusion, Not) and a.conclusion.children[0] == b.conclusion:
                    support = list(set(a.support + b.support))
                    if not Argument(support, F()) in self.arguments:
                        self.children.append(
                            Node(
                                self.arguments +
                                [Argument(support, F())]
                            )
                        )
                        found_new_inconsistency = True
                        break
            if not found_new_inconsistency:
                # TODO apply the attack rule
                complex: List[Argument] = \
                    [a for a in self.arguments if a.conclusion.is_decomposable()]
                if len(complex) > 0:
                    # sort the unexpanded propositions,
                    # so that those propositions that fork a branch are treated last:
                    complex_and_forking = \
                        [p for p in complex if p.conclusion.is_forking()]
                    complex_and_not_forking = \
                        [p for p in complex if not p.conclusion.is_forking()]
                    sorted_complex = complex_and_not_forking + complex_and_forking
                    to_be_decomposed = sorted_complex[0]
                    for branch_propositions in to_be_decomposed.conclusion.decompose():
                        self.children.append(
                            Node(
                                [a for a in self.arguments if a != to_be_decomposed]
                                + [Argument(to_be_decomposed.support, p)
                                   for p in branch_propositions]
                            )
                        )
        for child in self.children:
            child.expand()

    def arguments_for_inconsistency(self):
        """
        Return all arguments for an inconsistency in the node or in any child node.
        """
        if len(self.children) == 0:
            # find arguments where the conclusion is an inconsistency
            # and where the support includes at most one test
            arguments: List[Argument] = []
            for a in self.arguments:
                if a.conclusion == F():
                    tests = [s for s in a.support if isinstance(s, Test)]
                    if len(tests) <= 1:
                        arguments.append(a)
            return arguments
        elif len(self.children) == 1:
            # pass on all arguments from child
            return self.children[0].arguments_for_inconsistency()
        elif len(self.children) == 2:
            # combine the arguments from both branches
            arguments: List[Argument] = []
            for a in self.children[0].arguments_for_inconsistency():
                for b in self.children[1].arguments_for_inconsistency():
                    # keep only unique parts of the support
                    combined_unique_support = list(set(a.support + b.support))
                    # keep only arguments with at most one test in the support
                    tests = [
                        s for s in combined_unique_support if isinstance(s, Test)]
                    if len(tests) <= 1:
                        arguments.append(
                            Argument(combined_unique_support, F()))
            # keep only unique arguments
            return list(set(arguments))

    def arguments_for_and_against(self, p: Proposition):
        """
        Returns all arguments in favour of p.
        """
        arguments_for: List[Argument] = []
        arguments_against: List[Argument] = []
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
        return sorted(arguments_for), sorted(arguments_against)

    def add(self, arguments: List[Argument]):
        self.arguments += arguments
        for child in self.children:
            child.add(arguments)
