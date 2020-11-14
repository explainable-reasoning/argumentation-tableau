from typing import *
from abc import abstractmethod
import itertools

class Proposition:
    """
    Each proposition is either a truth value, a variable, or a complex (=composite) proposition, made up of some other propositions and an operator connecting them. This abstract class defines some common methods for all of them.
    """

    @abstractmethod
    def eval(self, model) -> bool:
        """
        Returns the truth value of the proposition given a model assigning a truth value to each variable.
        """

    @abstractmethod
    def variables(self) -> List[str]:
        """
        Returns a unique list of all variable names occuring in the proposition.
        """

    def truthtable(self) -> List[Tuple[Dict[str, bool], bool]]:
        """
        Returns a list of all the possible models with regard to the variables in the proposition, and the respective truth value of the whole proposition given the respective model.
        """
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


class Variable(Proposition):
    """
    An atomic proposition consisting of just a propositional variable.
    """

    def __init__(self, a: str):
        self.name = a

    def __str__(self):
        return self.name

    def eval(self, model: Dict[str, bool]) -> bool:
        if self.name in model:
            return model[self.name]
        else:
            raise KeyError(
                'The specified model does not include a value for variable '
                + self.name + ': ' + str(model))

    def variables(self) -> List[str]:
        return [self.name]


class TruthValue(Proposition):
    """
    An atomic proposition consisting of just a fixed truth value (true or false).
    """
    value: bool

    def __str__(self):
        return str(self.value)

    def eval(self, _) -> bool:
        return self.value

    def variables(self) -> List[str]:
        return []


class T(TruthValue):
    def __init__(self):
        self.value = True


class F(TruthValue):
    def __init__(self):
        self.value = False


class ComplexProposition(Proposition):
    """
    Proposition consisting of one or more other complex or atomic propositions, and an operator on them.
    """

    children: List[Proposition]

    def __init__(self, *args):
        self.children = []
        for arg in args:
            if type(arg) is str:
                # Shortcut for creating an atomic proposition without needing to call `AtomicProposition()` explicitly.
                child = Variable(arg)
            elif isinstance(arg, Proposition):
                child = arg
            else:
                raise Exception(
                    'Wrong type of child expression: ' + str(type(arg)))
            self.children.append(child)

    def __str__(self):
        children = self.children
        op = self.operator_symbol

        def brackets(a):
            if isinstance(a, ComplexProposition) and not isinstance(a, Not):
                return "(" + str(a) + ")"
            else:
                return str(a)
        if len(children) == 1:
            s = op + brackets(children[0])
        elif len(children) == 2:
            s = brackets(children[0]) + ' ' + op + ' ' + brackets(children[1])
        return s

    def eval(self, model: Dict[str, bool]) -> bool:
        evaluatedChildren = [child.eval(model) for child in self.children]
        return self.operator(*evaluatedChildren)

    def variables(self) -> List[str]:
        return sorted(list(set(flat([child.variables() for child in self.children]))))

    """Text symbol of the logical operator connecting the child propositions of the proposition."""
    operator_symbol: str

    @abstractmethod
    def operator(self, *args: bool) -> bool:
        """
        Implementation of the logical operator connecting the child propositions of the proposition.
        """


class And(ComplexProposition):
    operator_symbol = '∧'
    def operator(self, a, b): return a and b


class Or(ComplexProposition):
    operator_symbol = '∨'
    def operator(self, a, b): return a or b


class Implies(ComplexProposition):
    operator_symbol = '→'
    def operator(self, a, b): return b or (not a)


class Equiv(ComplexProposition):
    operator_symbol = '↔'
    def operator(self, a, b): return a == b


class Not(ComplexProposition):
    operator_symbol = '¬'
    def operator(self, a): return not a


# Helpers

# Flattens a list of lists to a list.
flat = itertools.chain.from_iterable
