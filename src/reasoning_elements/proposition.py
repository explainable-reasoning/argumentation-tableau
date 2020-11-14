from abc import abstractmethod
class Proposition:
    truth_value = False

    def __init__(self, truth_value):
        self.truth_value = truth_value

    def __str__(self):
        return "to string method not yet implemented for propositions"

    def decompose(self):
        return None

class old_Proposition:
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