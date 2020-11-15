from defeasible_tableau import *
from propositional_parser import *
from scenery_test_set import *

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

    for example in [
        logic_example_1,
        logic_example_2,
        scenery_example_2
    ]:
        tableau = Tableau(
            example['initial_information'],
            example['rules'],
            example['final_conclusion']
        )
        pro, contra = tableau.evaluate()
        print('Pro:')
        for a in pro:
            print(a)
        print('Contra:')
        for a in contra:
            print(a)
