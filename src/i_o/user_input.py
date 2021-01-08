from reasoning_elements.proposition import *

class UserInput:

    def ask(self, p: Proposition):
        answer = input("Is '" + str(p) + "' true?")
        if (answer=='yes'):
            return True
        else:
            return False

#a = UserInput()
#print(a.ask('a'))