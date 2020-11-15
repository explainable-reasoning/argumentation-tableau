from typing import *
from reasoning_elements.proposition import *
from reasoning_elements.rule import *


class Argument:
    def __init__(self, support: List[Union['Argument', Proposition]], conclusion: Union[Proposition, Rule]):
        self.support = support
        self.conclusion = conclusion

    def __str__(self):
        return '({' + ', '.join([str(p) for p in self.support]) + '}, ' + str(self.conclusion) + ')'
