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
        body, code, headers = app.process(self.command, path, params, context)
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

if __name__ == '__main__':
    app_path = sys.argv[1]
    app = web.App(app_path)
    host = sys.argv[2]
    port = int(sys.argv[3])
    server_address = (host, port)

    httpd = HTTPServer(server_address, FuqitHandler)
    #TODO: uh...how do i give my server stuff to give the handler?
    httpd.serve_forever()

