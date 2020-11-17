from reasoning_elements.proposition import *


class Test:
    content: Not

    def __init__(self, content: Not):
        self.content = content

    def __str__(self):
        return str(self.content) + '?'

    def nonnegated_content(self) -> Proposition:
        return self.content.children[0]

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    __test__ = False  # tell pytest that this has nothing to do with testing
