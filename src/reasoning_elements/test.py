from reasoning_elements.proposition import *


class Test:
    content: Not

    def __init__(self, content: Not):
        self.content = content

    def __str__(self):
        return str(self.content) + '?'

    def nonnegated_content(self):
        return self.content.children[0]

    __test__ = False  # tell pytest that this has nothing to do with testing
