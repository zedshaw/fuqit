# Fuqit Web Framework
# Copyright (C) 2013  Zed A. Shaw
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from fuqit import web, tools

DEFAULT_HEADERS = {
    'Content-type': 'text/plain'
}

class FuqitHandler(BaseHTTPRequestHandler):

    def transform_request(self, request_body=None):
        path, params = tools.parse_request(self.path, request_body)
        context = tools.build_context(params, self)
        body, code, headers = FuqitHandler.app.process(self.command, path, params, context)
        self.generate_response(body, code, headers)

    def do_GET(self):
        self.transform_request()

    def do_POST(self):
        clength = int(self.headers['content-length'])
        request_body = self.rfile.read(clength)
        self.transform_request(request_body)

    def generate_response(self, body, code, headers):
        headers = headers or DEFAULT_HEADERS

        self.send_response(code)

        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()

        self.wfile.write(body)

def run_server(host='127.0.0.1', port=8000, referer='http://', app='app',
               debug=True):

    server_address = (host, port)

    # the fatal flaw of the dumb python webserver design is it makes
    # a new handler for every request even though it's totally not necessary
    FuqitHandler.app = web.App(app, allowed_referer=referer)

    httpd = HTTPServer(server_address, FuqitHandler)
    httpd.serve_forever()

