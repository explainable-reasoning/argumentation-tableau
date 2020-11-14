from reasoning_elements.proposition import *

class Node:

    arguments = {'complex': [], 'primitive': []}
    # `primitive` and `complex` refers to the conclusion of the argument
    children = []
    

    def __init__(self, arguments: Tuple[List[Proposition], Proposition]):
        for (support, conclusion) in arguments:
            if conclusion.is_primitive():
                self.arguments.primitive.append((support, conclusion))
            else:
                self.arguments.complex.append((support, conclusion))
        

    def __str__(self):
        return

    def expand(self, new_arguments) -> List[Argument]:
        support_for_closure = []
        child_argument_map = {}
        if len(self.children) == 0:
            support_for_closure.append(check_for_inconsistency(self.arguments.primitive, new_arguments))

            expansion_argument = self.arguments.complex.pop(0)
            #children, child_argument_map = _#apply tableaux rule  

            """
            # get child nodes in accordance with the tableaux rules
            # each child node should have the same arguments as the parent node
            # each child node should have an empty set of children
            # in accordance with the tableaux rules, for each child some new argument gets formulated
            # the new argument consists of the support from the parent node and a new proposition as conclusion
            # Example: 
            #   If there is an argument ({a, b, c}, p & q), the child node will instead contain 2 arguments: 
            #   ({a, b, c}, p) and ({a, b, c}, q)            
            # take a look at `propositional_tableaux_tree.py`, but there it is much too complicated
            # take a look at the paper p. 4, bottom
            # the function should return a list of children, and a dictionary associating the new arguments to the children
            """

        for child in children:
            new_arguments = child_argument_map[child] if len(child_argument_map) > 0 else new_arguments
            support_for_closure.append(child.expand(new_arguments))
            
        return support_for_closure


        support_for_closure.append(self.children.expand(new_arguments))
        return support_for_closure
        
    def check_for_inconsistency(self, arguments, new_arguments):
        support_for_closure = []
        for (support, conclusion) in arguments:
            for (new_support, new_conclusion) in new_arguments:
                if conclusion.is_inconsistent_with(conclusion):
                    support_for_closure.append(list(set(support, new_support)))  
        return support_for_closure # return combined support without duplicates


        return
        """
        expanding a node Γ recursively:
            check all pairs of primitive propositions and check for inconsistencies in the arguments
            if there is no inconsistency to be derived:
                check all pairs of defeasible rules in the conclusions of arguments in the node and try to 
                apply the attack rule (see below)
                if there is no attack rule to be applied:
                    select the first argument (S, c) where the conclusion c is longer than a single literal
                    apply the corresponding rule of the normal propositional tableau
                    this yields one or two branches = one or two sets of child propositions
                    for each set of child propositions P:
                        create a child node Γ' with the same argument set as Γ
                        remove (S, c) from the child node
                        instead add (S, p) for every p ∈ P
                        if Γ'\Γ does not include an argument with the conclusion ⟘
                        (that is, if there is no new argument for a closure):
                            expand p recursively
        """
