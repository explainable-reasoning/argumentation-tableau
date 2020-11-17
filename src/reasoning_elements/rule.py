import functools
from reasoning_elements.proposition import *


@functools.total_ordering
class Rule:

    def __init__(self, antecedence: Proposition, consequence: Proposition, default_defeasible_level=5):
        self.defeasible_level = default_defeasible_level
        self.antecedence = antecedence
        self.consequence = consequence

    def __str__(self):
        return str(self.antecedence) + ' ~> ' + str(self.consequence)

    def is_decomposable(self) -> bool:
        return self.consequence.is_decomposable()

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return hash(str(self))
