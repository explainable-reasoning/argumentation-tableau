from typing import *
import itertools


class AtomicProposition:
    """
    Atomic proposition (just one variable) to build up complex propositions.
    """

    def __init__(self, a: str):
        self.name = a

    def __str__(self):
        return self.name

    def eval(self, model):
        if self.name in model:
            return model[self.name]
        else:
            raise KeyError(
                'The specified model does not include a value for variable '
                + self.name + ': ' + str(model))

    def variables(self):
        return [self.name]


class ComplexProposition:
    """
    Proposition consisting of one or more other complex or atomic propositions, and an operator on them.
    """

    children: List[Union['ComplexProposition', AtomicProposition]]

    def __init__(self, *args):
        self.children = []
        for arg in args:
            if type(arg) is str:
                child = AtomicProposition(arg)
            elif type(arg) is ComplexProposition:
                child = arg
            self.children.append(child)

    def __str__(self):
        children = self.children
        op = self.operator_symbol
        if len(children) == 1:
            s = op + str(children[0])
        elif len(children) == 2:
            s = str(children[0]) + op + str(children[1])
        else:
            s = op + '(' + [str(child) for child in children].join(', ') + ')'
        return '(' + s + ')'

    def eval(self, model: Dict[str, bool]) -> bool:
        evaluatedChildren = [child.eval(model) for child in self.children]
        return self.operator(*evaluatedChildren)

    def variables(self) -> List[str]:
        return sorted(list(set(flat([child.variables() for child in self.children]))))

    def truthtable(self) -> List[Tuple[Dict[str, bool], bool]]:
        variables = self.variables()
        rows = itertools.product([True, False], repeat=len(variables))
        table = []
        for row in rows:
            model = dict(zip(variables, row))
            table.append((model, self.eval(model)))
        return table

    def print_truthtable(self):
        for row in self.truthtable():
            print(row)

    def operator(self, *args: bool) -> bool:
        raise NotImplementedError


class And(ComplexProposition):
    operator_symbol = '∧'
    def operator(self, a, b): return a and b


class Or(ComplexProposition):
    operator_symbol = '∨'
    def operator(self, a, b): return a or b


class Implies(ComplexProposition):
    operator_symbol = '→'
    def operator(self, a, b): return b or (not a)


class Equal(ComplexProposition):
    operator_symbol = '↔'
    def operator(self, a, b): return a == b


class Not(ComplexProposition):
    operator_symbol = '¬'
    def operator(self, a): return not a

# Helpers


# Flattens a list of lists to a list.
flat = itertools.chain.from_iterable
