from propositional_parser import toProposition
from reasoning_elements.rule import Rule
import json


class Configuration:
    """Configuration file for the file reader, give a more sensible name"""

    def __init__(self, Rule, toProposition):
        self.Rule = Rule
        self.toProposition = toProposition

    def read_file(self, filename):
        with open(filename, 'r') as reader:
            for line in reader:
                print(line)

    def parse_json(self, filename):
        rules = []
        facts = []

        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)

            for set in data:

                rules_data = data[set]["rules"]
                facts_data = data[set]["facts"]

                rules = [self.Rule(self.toProposition(rules_data[rule]["antecedence"].encode('utf-8').decode('utf-8')),
                                   self.toProposition(rules_data[rule]["consequence"].encode('utf-8').decode('utf-8'))) for rule in rules_data]

                for fact_data in facts_data:
                    facts.append(self.toProposition(fact_data))

                facts = [self.toProposition(fact_data)
                         for fact_data in facts_data]

        return rules, facts
