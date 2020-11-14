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

    def __init__(self, proposition):
        self.root = Node([(toProposition(proposition), False)])
        self.root.expandRecursively()

    def __str__(self):
        return str(self.root)

    def is_invalid(self) -> bool:
        return self.root.is_invalid()


class Node:
    """
    Node of a propositional tableau.
    Contains a list of propositions, along with information whether they have already been rewritten by using a rule.
    Can be expanded, and then it may have child nodes.
    """
    arguments: List[Tuple[Proposition, bool]]

    root: List # list with rules, list with propositions, list of tests?
    support: List
    atomic_propositions: List
    rules: List
    #critical tests??

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

    """
    Arguments: composed of sub arguments (can alternate between rules and propositions)
            evaluate subarguments in order ??

    rules:  check conditions
            apply to all child nodes

    propositions: check for decomposition
            evaluate if atomic

    tests:  check conditions #what happens if a failing test does not lead to contradiction
            create tests for all atomic propositions in root; evaluate in all children

    => all can be in one node

    what happens in a node? -> 1) evaluate propositions
                            2) evaluate test
                            3) apply rules

    if there are contradictions in a branch, do ... ??

    if nothing is left to do in one branch, check if it is closed
        -> if so, return all the arguments leading to the closure



    Node(
        - root propositions, tests, rules
        - current support ("activated" propositions and rules)
        - currently evaluated atomic propositions
    )

    tableau: Arguments
A1 |- A2 |- A3 |- A4
A1 -> add everything to root -> evaluate, apply rules and tests etc.
A2 -> add everything to same root -> evaluate...
.
.
.

    """



    def expand(self):
        evaluate_propositions(propositions)

        evaluate_tests()

        apply_rules()


        return

    def evaluate_propositions(propositions, complex_propositions):
        for proposition in propositions:
            decomposed_basic, decomposed_complex = proposition.decompose(complex_propositions)
            # we might add the branching rules to some rule object which is included in the complex propositions
            basic_propositions.append(decomposed_basic)
            complex_propositions.append(decomposed_complex)

        return

    def evaluate_tests(tests, current_support):
        for test in tests:
            # check if the test for any basic proposition has been evalueated yet in this branch
            # and if the support allows for any untested tests
            # is the current support sufficient to sufficiently evlauate tests?

            tested_proposition = test.check(basic_propositions)
            if len(tested_proposition) > 0:
                # should we also remember the original complex propositions from where the basic proposition was derived
                # and add it to the current support in case all the atomic propositions are tested accordingly?
                current_support.append(tested_proposition)
        return

    def apply_rules(rules, current_support):
        #FIXME somehow avoid circularity for the application of rules!!
        for rule in rules:
            if rule.check_antecedence(current_support):
                evaluate_propositions(rule.consequence, complex_propositions)
                evaluate_tests(tests, current_support)
                # maybe a call to expand(self) function does exactly what needs to be done here,
                # but it might not be warranted here to create new branches and such in the same step as we evaluate the rules


        return

    def expand_old(self):
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

