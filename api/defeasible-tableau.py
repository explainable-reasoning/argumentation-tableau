from http.server import BaseHTTPRequestHandler
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from defeasible_tableau import Tableau
from propositional_parser import parse
from reasoning_elements.rule import Rule
from decision_support_system import DecisionSupportSystem

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        input = json.loads(body)
        t = Tableau(
            question=parse(input['question']),
            initial_information={parse(p) for p
                                 in input['initial_information']},
            rules={Rule(parse(a), parse(b)) for (a, b)
                   in input['rules']}
        )
        flag, result = t.evaluate()
        if flag == 'known':
            pro, contra = result
            output = json.dumps({'flag': 'known',
                                 'result': [[str(p) for p in pro],
                                          [str(p) for p in contra]]})
        if flag == 'unknown':
            question = DecisionSupportSystem(
                question=parse(input['question']),
                initial_information={parse(p) for p
                                     in input['initial_information']},
                rules={Rule(parse(a), parse(b)) for (a, b)
                       in input['rules']}
            ).get_promising_tests(result)
            output = json.dumps({'flag': 'unknown',
                                 'result': list(question)})
        print(output.encode('utf-8'))
        self.wfile.write(output.encode('utf-8'))

