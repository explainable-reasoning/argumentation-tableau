from typing import *
from defeasible_tableau import *
from reasoning_elements import *
from propositional_parser import *

logic_example_1 = {
    'initial_information':
    [
        parse('p ∨ q'),
        parse('¬q'),
    ],
    'rules': [
        Rule(
            parse('p'),
            parse('r')
        ),
        Rule(
            parse('r'),
            parse('s')
        )
    ],
    'final_conclusion': 's',
    'preference':
    [
        (1, 0),  # R2 > R1
        (2, 0),  # R3 > R1
        (3, 0),  # R4 > R1
    ]
}


logic_example_2 = {
    'initial_information':
    [
        parse('¬(p & q)'),
        parse('r ∨ s'),
        parse('t'),
    ],
    'rules': [
        Rule(
            parse('r'),
            parse('p')
        ),
        Rule(
            parse('t'),
            parse('q')
        )
    ],
    'final_conclusion': 's',
    'preference':
    [
        (1, 0),  # R2 > R1
        (2, 0),  # R3 > R1
        (3, 0),  # R4 > R1
    ]
}

scenery_example_2 = {
    'initial_information':
    [
        parse('Employed'),
        parse('¬LessThanTenEmployees'),
        parse('¬ReachedOldAgeInsurance'),
        parse('MilitaryOfficial'),
        parse('WorkedForAtLeastTwentySixWeeks'),
    ],
    'rules': [
        Rule(
            parse('Employed'),
            parse('CanMakeRequestForChange')
        ),
        Rule(
            parse('Employed & LessThanTenEmployees'),
            parse('¬CanMakeRequestForChange')
        ),
        Rule(
            parse('Employed & ReachedOldAgeInsurance'),
            parse('¬CanMakeRequestForChange')
        ),
        Rule(
            parse('Employed & MilitaryOfficial'),
            parse('¬CanMakeRequestForChange')
        )
    ],
    'final_conclusion': '¬CanMakeRequestForChange',
    'preference':
    [
        (1, 0),  # R2 > R1
        (2, 0),  # R3 > R1
        (3, 0),  # R4 > R1
    ]
}
