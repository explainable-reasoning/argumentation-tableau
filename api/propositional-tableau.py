from http.server import BaseHTTPRequestHandler
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from propositional_tableau import Tableau

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        t = Tableau(body)
        self.wfile.write(str(t).encode('utf-8'))
