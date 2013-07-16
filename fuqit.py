import sys
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, PackageLoader, TemplateNotFound
from importlib import import_module

def module(name):
    themodule = import_module("." + name, package="app")
    return themodule

TOOLS = {'module' : module}
APP = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])
SERVER_ADDRESS = (HOST, PORT)
ENV = Environment(loader=PackageLoader(APP, '.'))


class FuqitHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.knife_or_banana(self.path)
        except TemplateNotFound:
            self.send_response(404)
        #except Exception as e:
        #    self.send_error(500, str(e))

    def make_vars(self):
        variables = self.__dict__.copy()
        variables.update(TOOLS)
        return variables

    def reply(self, body, code=200, content_type="text/html"):
        """Send a reply properly since the python http server has 0 clues about
        things like headers and HTTP.
        """
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(body)

    def render_template(self, path):
        template = ENV.get_template(path)
        variables = self.make_vars()
        self.reply(template.render(**variables))

    def render_module(self, name):
        # OH MAN THE HACKING THIS CAN ALLOW!
        base, ext = os.path.splitext(name[1:])
        base = base.replace('/', '.')
        target = module(base)
        variables = self.make_vars()
        result = target.run(variables)
        self.reply(result)

    def knife_or_banana(self, path):
        path = path.split('?', 1)[0]
        # THIS AIN'T THAT SECURE, BUT FUQIT
        root, ext = os.path.splitext(path)

        if ext:
            # if it has an extension it's a template
            return self.render_template(path)
        elif path.endswith('/'):
            # if it ends in /, it's a /index.html or /index.py
            base = os.path.join(path, 'index')
            print "BASE", 'app' + base + '.html'

            if os.path.exists('app' + base + '.html'):
                print "FOUND", base + '.html'
                return self.render_template(base + '.html')
            elif os.path.exists('app' + base + '.py'):
                return self.render_module(base + '.py')
        elif os.path.isdir('app' + path):
            # if dir with no trailing /, redirect
            self.send_response(301)
            self.send_header('Location', path + '/')
            self.end_headers()
            return "" 
        else:
            # otherwise it's a module, tack on .py and load or fail
            return self.render_module(path + '.py')


httpd = HTTPServer(SERVER_ADDRESS, FuqitHandler)
httpd.serve_forever()

