from defeasible_tableau import *
from propositional_parser import *
import scenery_test_set

# initial_information: List[Proposition] = [
#     parse('Employed'),
#     parse('¬LessThanTenEmployees'),
#     parse('¬ReachedOldAgeInsurance'),
#     parse('MilitaryOfficial'),
#     parse('WorkedForAtLeastTwentySixWeeks'),
# ]
#
# rules : List[Rule] = [
#     Rule(
#         parse('Employed'),
#         parse('CanMakeRequestForChange')
#     ),
#     Rule(
#         parse('Employed & LessThanTenEmployees'),
#         parse('¬CanMakeRequestForChange')
#     ),
#     Rule(
#         parse('Employed & ReachedOldAgeInsurance'),
#         parse('¬CanMakeRequestForChange')
#     ),
#     Rule(
#         parse('Employed & MilitaryOfficial'),
#         parse('¬CanMakeRequestForChange')
#     )
# ]
#
# preference = [
#     (1, 0),  # R2 > R1
#     (2, 0),  # R3 > R1
#     (3, 0),  # R4 > R1
# ]
#
# tableau = Tableau(
#     initial_information,
#     rules,
#     parse('¬CanMakeRequestForChange')
# )
#
# pro, contra = tableau.evaluate()
#
# print('Pro:')
# for a in pro: print(a)
# print('Contra:')
# for a in contra: print(a)

# print(tableau.root)

if __name__ == '__main__':
    example_1 = scenery_test_set.logic_example_1
    tableau = Tableau(
        example_1['initial_information'],
        example_1['rules'],
        parse('¬CanMakeRequestForChange')
    )
    pro, contra = tableau.evaluate()
    print('Pro:')
    for a in pro: print(a)
    print('Contra:')
    for a in contra: print(a)