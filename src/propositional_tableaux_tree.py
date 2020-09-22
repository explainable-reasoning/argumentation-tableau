from propositional_logic import *
from typing import Tuple, List


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
    return not tableau.is_invalid()


class Tableau:
    root: 'Node'

    def __init__(self, argument: Argument):
        root = Node([(argument, False)])

    def is_invalid(self) -> bool:
        return self.root.is_invalid()


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
        Expands the next unexpanded argument.
        This means roughly that child nodes are added, where the unexpanded arguments will be replaced using the rewriting rules of propositonal tableau.
        One proposition is expanded at a time. If there are propositions whose expansion is non-branching, they will be considered first, to reduce redundancy in the new branches.
        """
        unexpanded = [arg
                      for (arg, alreadyExpanded)
                      in self.arguments
                      if not alreadyExpanded]
        # Sequents:
        non_branching: List[Proposition] = []
        branching: List[List[Proposition]] = []
        # Old arguments with new sequents, where the expansion may be delayed
        delayed_branching: List[Proposition] = []
        # Old arguments without new sequents
        old: List[Proposition] = [arg.conclusion
                                  for (arg, alreadyExpanded)
                                  in self.arguments
                                  if alreadyExpanded]
        for argument in unexpanded:
            p = argument.conclusion
            if isinstance(p, And):
                non_branching += [p.children[0], p.children[1]]
            elif isinstance(p, Or):
                branching.append([p.children[0], p.children[1]])
                delayed_branching.append(p)
            elif isinstance(p, Implies):
                branching.append([Not(p.children[0]), p.children[1]])
                delayed_branching.append(p)
            elif isinstance(p, Equal):
                non_branching += [Implies(p.children[0], p.children[1]),
                                  Implies(p.children[1], p.children[0])]
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
                    branching.append([Not(q.children[0]), Not(q.children[1])])
                    delayed_branching.append(p)
                elif isinstance(q, Or):
                    non_branching += [Not(q.children[0]), Not(q.children[1])]
                elif isinstance(q, Implies):
                    non_branching += [q.children[0], Not(q.children[1])]
                elif isinstance(q, Equal):
                    branching.append([Not(Implies(q.children[0], q.children[1])),
                                      Not(Implies(q.children[1], q.children[0]))])
                    delayed_branching.append(p)
                elif isinstance(q, Not):
                    non_branching += [q.children[0]]
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
        old_arguments = [(Argument(Support(), proposition), True)
                         for proposition in old]
        if len(non_branching) > 0:
            new_arguments = [(Argument(Support(), proposition), False)
                             for proposition in non_branching + delayed_branching]
            all_arguments = old_arguments + new_arguments
            self.children.append(Node(all_arguments))
        elif len(branching) > 0:
            for branch in branching[0]:
                new_arguments = ([(Argument(Support(), branch), False)] +
                                 [(Argument(Support(), proposition), False)
                                  for proposition in delayed_branching[1:]])
                all_arguments = old_arguments + new_arguments
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
