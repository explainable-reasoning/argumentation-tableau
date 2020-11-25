import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from http.server import BaseHTTPRequestHandler
from reasoning_elements.rule import Rule
from propositional_parser import parse
from defeasible_tableau import Tableau


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        input = json.loads(body)
        t = Tableau(
            question=input['question'],
            initial_information=[parse(p) for p
                                 in input['initial_information']],
            rules=[Rule(parse(a), parse(b)) for (a, b)
                   in input['rules']] 
        )
        pro, contra = t.evaluate()
        output = json.dumps([[str(p) for p in pro],
                            [str(p) for p in contra]])
        self.wfile.write(output.encode('utf-8'))
