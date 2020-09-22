from propositional_logic import *
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

    def __init__(self, proposition: Proposition):
        root = Node([(proposition, False)])

    def is_invalid(self) -> bool:
        return self.root.is_invalid()


class Node:
    """
    Node of a propositional tableau.
    Contains a list of propositions, along with information whether they have already been rewritten by using a rule.
    Can be expanded, and then it may have child nodes.
    """
    arguments: List[Tuple[Proposition, bool]]

    children: List['Node']

    closed: bool

    def __init__(self, propositions: List[Tuple[Proposition, bool]]):
        """
        Make a new node.
        Takes a list of pairs, where each pair consists of:
        - A proposition.
        - A boolean indicating whether the proposition has already been rewritten using one of the rules.
          This information is important, since in propositional tableaux, every rule needs be rewritten only once. (Roos, L4AI, p. 34)
        """
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
        propositions = [str(p) for (p, _) in self.propositions]
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
        unexpanded = [p for (p, alreadyExpanded) in self.propositions
                      if not alreadyExpanded]
        # Sequents:
        non_branching: List[Proposition] = []
        branching: List[List[Proposition]] = []
        # Old arguments with new sequents, where the expansion may be delayed
        delayed_branching: List[Proposition] = []
        # Old arguments without new sequents
        old: List[Proposition] = [p for (p, alreadyExpanded) in self.propositions
                                  if alreadyExpanded]
        for p in unexpanded:
            if isinstance(p, And):
                non_branching += [p.children[0], p.children[1]]
            elif isinstance(p, Or):
                branching.append([p.children[0], p.children[1]])
                delayed_branching.append(p)
            elif isinstance(p, Implies):
                branching.append([Not(p.children[0]), p.children[1]])
                delayed_branching.append(p)
            elif isinstance(p, Equiv):
                non_branching += [Implies(p.children[0], p.children[1]),
                                  Implies(p.children[1], p.children[0])]
            elif isinstance(p, Variable):
                if any([isinstance(x, Not)
                        and isinstance(x.children[0], Variable)
                        and p.name == x.children[0].name
                        for (x, _) in self.propositions]):
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
                elif isinstance(q, Equiv):
                    branching.append([Not(Implies(q.children[0], q.children[1])),
                                      Not(Implies(q.children[1], q.children[0]))])
                    delayed_branching.append(p)
                elif isinstance(q, Not):
                    non_branching += [q.children[0]]
                elif isinstance(q, Variable):
                    if any([isinstance(x, Variable)
                            and q.name == x.name
                            for (x, _) in self.propositions]):
                        self.closed = True
                    else:
                        old.append(p)
                else:
                    old.append(p)
            else:
                old.append(p)
        old_ = [(p, True) for p in old]
        if len(non_branching) > 0:
            new = [(proposition, False) for proposition
                   in non_branching + delayed_branching]
            self.children.append(Node(old_ + new))
        elif len(branching) > 0:
            for branch in branching[0]:
                new = [(proposition, False) for proposition
                       in [branch] + delayed_branching[1:]]
                self.children.append(Node(old_ + new))

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
