from typing import *
from reasoning_elements.proposition import *
from reasoning_elements.rule import *
from reasoning_elements.test import *
import functools


@functools.total_ordering
class Argument:
    def __init__(self, support: List[Union['Argument', Proposition, Test]], conclusion: Union[Proposition, Rule]):
        self.support = support
        self.conclusion = conclusion

    def __str__(self):
        return '({' + ', '.join(sorted([str(p) for p in self.support])) + '}, ' + str(self.conclusion) + ')'

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return hash(str(self))
