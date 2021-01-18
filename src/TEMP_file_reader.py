from propositional_parser import toProposition
from reasoning_elements.rule import Rule
import re
import json


"""eventually the helper classes can be passed as argumennts to the configuration or vv"""

class Configuration:

    def read_file(self,filename):
        with open(filename, 'r') as reader:
            for line in reader:
                print(line)

    def parse_json(self,filename):
        rules = []
        facts = []

        with open(filename, encoding='utf-8') as json_file:
            data = json.load(json_file)

            for set in data:

                rules_data = data[set]["rules"]
                facts_data = data[set]["facts"]

                test = rules_data["1.1"]["antecedence"]
                test1 = rules_data["1.1"]["consequence"]
                test2 = Rule(toProposition(test), toProposition(test1))

                rules = [Rule(toProposition(rules_data[rule]["antecedence"].encode('utf-8').decode('utf-8')), toProposition(rules_data[rule]["consequence"].encode('utf-8').decode('utf-8'))) for rule in rules_data]

                for fact_data in facts_data:
                    facts.append(toProposition(fact_data))

                facts = [toProposition(fact_data) for fact_data in facts_data]

        return rules, facts

config = Configuration()
a, b = config.parse_json("./sample_rule_sets/british_national_act.json")