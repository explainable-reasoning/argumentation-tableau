from propositional_logic import *

# B or not B
shakespeare = Or('B', Not('B'))
print(shakespeare)
shakespeare.print_truthtable()

# A implies B
impl = Implies('A', 'B')
print(impl)
impl.print_truthtable()

# A and B and C
conj = And('A', And('B', 'C'))
print(conj)
conj.print_truthtable()
