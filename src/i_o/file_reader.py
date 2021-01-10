from propositional_parser import toProposition
import json

class Configuration:

    def read_file(filename):
        with open(filename, 'r') as reader:
            for line in reader:
                print(line)

    def parse_json(filename):
        rules = []
        facts = []

        with open(filename) as json_file:
            data = json.load(json_file)

            for set in data:

                rules_data = set["rules"]
                facts_data = set["facts"]

                for rule_data in rules_data:
                    rules.append(toProposition(rule_data))

                rules = [toProposition(rule_data) for rule_data in rules_data]

                for fact_data in facts_data:
                    facts.append(toProposition(fact_data))

                facts = [toProposition(fact_data) for fact_data in facts_data]

        return rules, facts

config = Configuration()
a, b = config.parse_json("../sample_rule_sets/british_national_act.json")