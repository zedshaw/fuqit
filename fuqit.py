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

    def render_template(self, path):
        template = ENV.get_template(path)
        variables = self.make_vars()
        self.wfile.write(template.render(**variables))

    def render_module(self, name):
        # OH MAN THE HACKING THIS CAN ALLOW!
        base, ext = os.path.splitext(name[1:])
        base = base.replace('/', '.')
        target = module(base)
        variables = self.make_vars()
        result = target.run(variables)
        self.wfile.write(result)

    def knife_or_banana(self, path):
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
        else: 
            # otherwise it's a module, tack on .py and load or fail
            return self.render_module(path + '.py')


httpd = HTTPServer(SERVER_ADDRESS, FuqitHandler)
httpd.serve_forever()

