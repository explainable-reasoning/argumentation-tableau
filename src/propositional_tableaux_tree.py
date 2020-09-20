from propositional_logic import *
from typing import Tuple, List
from itertools import product


class Support:
    """
    Support for an argument. This doesn't do anything. The `Tableau` works on `Argument`s, so we will just always use an empty `Support` to create an `Argument`.
    """

    def __init__(self, *args):
        pass

    @staticmethod
    def union(self, support1, support2):
        pass


class Argument:
    """
    Argument, consisting of a support (which is not yet used) and a conclusion (which is a proposition).
    """
    support: Support
    conclusion: Proposition

    def __init__(self, support: Support, conclusion: Proposition):
        self.support = support
        self.conclusion = conclusion


def is_valid(argument: Argument) -> bool:
    """
    Checks whether an argument is valid:
    Whether the conclusion holds in every possible situation, given the support.
    (The support is ignored at the moment.)
    """
    tableau = Tableau(Argument(argument.support, Not(argument.conclusion)))
    return tableau.is_invalid()


def is_satisfiable(argument: Argument) -> bool:
    """
    Checks whether a proposition is satisfiable:
    Whether it is true in at least one possible situation, given the support.
    (The support is ignored at the moment.)
    """
    tableau = Tableau(argument)
    return tableau.is_satisfiable()


class Tableau:
    root: 'Node'

    def __init__(self, argument: Argument):
        root = Node([(argument, False)])

    def is_invalid(self) -> bool:
        return self.root.is_invalid()

    def is_satisfiable(self) -> bool:
        return self.root.is_satisfiable()


class Node:
    """
    Node of a propositional tableau.
    Contains a list of arguments, along with information whether they have already been rewritten by using a rule.
    Can be expanded, and then it may have child nodes.
    """
    arguments: List[Tuple[Argument, bool]]

    children: List['Node']

    closed: bool

    def __init__(self, arguments: List[Tuple[Argument, bool]]):
        """
        Make a new node.
        Takes a list of pairs, where each pair consists of:
        - An argument.
        - A boolean indicating whether the argument has already been rewritten using one of the rules.
          This information is important, since in propositional tableaux, every rule needs be rewritten only once. (Roos, L4AI, p. 34)
        """
        self.arguments = arguments
        self.children = []
        self.closed = False

    def __str__(self, indent='', parentConclusions=[]):
        """
        Stringifies a node and its child nodes in the shape of a tree.
        Optional arguments:
        - An indent. For the tree shape, every node will just call the string method of its child nodes, with a bigger indent.
        - The conclusions of the parent. These will be ignored for the output string, since they would be redundant.
        Multiple propositions within one node will be printed in consecutive lines.
        Multiple nodes are separated by a blank line.
        """
        conclusions = [str(arg.conclusion) for (arg, _) in self.arguments]
        return (indent
                + ('\n' + indent).join([c for c in conclusions
                                        if c not in parentConclusions])
                + '\n'
                + (indent + '❌\n' if self.closed else "")
                + '\n'.join([child.__str__(indent + '    ', conclusions) for child in self.children]))

    def expand(self):
        """
        Expands all unexpanded arguments. 
        This means roughly that child nodes are added, where the unexpanded arguments will be replaced using the rewriting rules of propositonal tableau.
        This is slightly complex, since multiple arguments may need to be expanded at the same time, possibly leading to multiple branching.
        This is resolved as follows with the help of the cartesian product:
            The sequents of each unexpanded argument are added to the `layers` list:
            - If the rewriting rule requires no branching, both sequents should be contained in all branches. They are therefore added separately (each inside a singleton list) to the `layers` list.
            - If the rewriting rule requires branching, the sequents should not occur together in any branch. They are therefore added together (inside a list of two elements) to the `layers` list.
            Afterwards, the cartesian product of the list is taken, yielding a list of all branches.
            The already expanded arguments are added to each list, and a child node is created for each list.
        """
        unexpanded = [arg
                      for (arg, alreadyExpanded)
                      in self.arguments
                      if not alreadyExpanded]
        layers: List[List[Proposition]] = []
        old: List[Proposition] = []
        for argument in unexpanded:
            p = argument.conclusion
            if isinstance(p, And):
                layers.append([p.children[0]])
                layers.append([p.children[1]])
            elif isinstance(p, Or):
                layers.append([p.children[0],
                               p.children[1]])
            elif isinstance(p, Implies):
                layers.append([Not(p.children[0]),
                               p.children[1]])
            elif isinstance(p, Equal):
                layers.append([Implies(p.children[0], p.children[1])])
                layers.append([Implies(p.children[1], p.children[0])])
            elif isinstance(p, Variable):
                if any([isinstance(arg.conclusion, Not)
                        and isinstance(arg.conclusion.children[0], Variable)
                        and p.name == arg.conclusion.children[0].name
                        for (arg, _) in self.arguments]):
                    self.closed = True
                else:
                    old.append(p)
            elif isinstance(p, Not):
                q = p.children[0]
                if isinstance(q, And):
                    layers.append([Not(q.children[0]),
                                   Not(q.children[1])])
                elif isinstance(q, Or):
                    layers.append([Not(q.children[0])])
                    layers.append([Not(q.children[1])])
                elif isinstance(q, Implies):
                    layers.append([q.children[0]])
                    layers.append([Not(q.children[1])])
                elif isinstance(q, Equal):
                    layers.append([Not(Implies(q.children[0], q.children[1])),
                                   Not(Implies(q.children[1], q.children[0]))])
                elif isinstance(q, Not):
                    layers.append([q.children[0]])
                elif isinstance(q, Variable):
                    if any([isinstance(arg.conclusion, Variable)
                            and q.name == arg.conclusion.name
                            for (arg, _) in self.arguments]):
                        self.closed = True
                    else:
                        old.append(p)
                else:
                    old.append(p)
            else:
                old.append(p)
        if len(layers) > 0:
            for branch in product(*layers):
                old_arguments = [
                    (Argument(Support(), arg), True)
                    for arg in old
                ]
                all_arguments = old_arguments + [(Argument(Support(), proposition), False)
                                                 for proposition in branch]
                self.children.append(Node(all_arguments))

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

    def is_satisfiable(self):
        self.expandRecursively()
        if len(self.children) > 0:
            return any([child.is_satisfiable() for child in children])
        else:
            return not self.closed
