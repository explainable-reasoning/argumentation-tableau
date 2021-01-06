from reasoning_elements.proposition import *

class UserInput:

    def ask(self, p: Proposition):
        answer = input("Is '" + p + "' true?")
        if (answer=='yes'):
            return True
        else:
            return False

a = UserInput()
print(a.ask('a'))