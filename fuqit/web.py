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

import os
from jinja2 import Environment, PackageLoader, TemplateNotFound
from fuqit import tools, sessions
import re
import traceback

class RequestDict(dict):
    __getattr__ = dict.__getitem__

class App(object):

    def __init__(self, app, default_mtype=None, static_dir=None,
                 allowed_referer="*"):
        self.app_path = os.path.realpath(app)
        self.app = app
        self.static_dir = os.path.realpath(self.app_path +
                                           (static_dir or '/static/'))
        self.errors_dir = self.app_path + '/errors/'
        self.default_mtype = default_mtype or 'text/html'
        self.env = Environment(loader=PackageLoader(self.app, '.'))
        self.allowed_referer = re.compile(allowed_referer)

    def render_error(self, code, message="", variables=None):
        try:
            return self.render_template(self.errors_dir + '%d.html' %
                                        code, variables or {}, ext='.html')
        except TemplateNotFound:
            return message, code, {}

    def csrf_check(self, context):
        referer = context['headers'].get('referer', '')

        if referer:
            return self.allowed_referer.match(referer)
        else:
            return True

    def process(self, method, path, params, context):
        if not self.csrf_check(context):
            return self.render_error(404, "Not Found")

        try:
            return self.render(path, context)
        except TemplateNotFound:
            return self.render_error(404, "Not Found")
        except Exception as e:
            traceback.print_exc()
            return self.render_error(500, str(e))

    def render_template(self, path, variables, ext=None):
        ext = ext or os.path.splitext(path)[1]
        headers = tools.make_ctype(ext, self.default_mtype)

        if 'headers' in variables:
            sessions.load_session(variables)

        context = {'web': variables,
                   'module': tools.module,
                   'response_headers': headers
                  }

        template = self.env.get_template(path)
        result = template.render(**context)

        if 'headers' in variables:
            sessions.save_session(variables, headers)

        return result, 200, headers

    def find_longest_module(self, name, variables):
        base = name[1:]

        # need to limit the max we'll try to 20 for safety
        for i in xrange(0, 20):
            # go until we hit the /
            if base == '/': return None

            modname = base.replace('/', '.')

            try:
                return base, tools.module(modname, self.app)
            except ImportError:
                # split off the next chunk to try to load
                base, tail = os.path.split(base)

        # exhausted the path limit
        return None

    def render_module(self, name, variables):
        base, target = self.find_longest_module(name, variables)
        variables['base_path'] = base
        variables['sub_path'] = name[len(base)+1:]
        sessions.load_session(variables)

        context = RequestDict(variables)

        if target:
            try:
                actions = target.__dict__
                func = actions.get(context.method, None) or actions['run']
            except KeyError:
                return self.render_error(500, 'No run method or %s method.' %
                                         context.method)
            result = func(context)

            session_headers = {}
            sessions.save_session(variables, session_headers)

            if isinstance(result, tuple):
                body, code, headers = result
                headers.update(session_headers)
                return body, code, headers
            else:
                session_headers['Content-type'] = self.default_mtype
                return result, 200, session_headers
        else:
            return self.render_error(404, "Not Found", variables=variables)

    def render_static(self, ext, path):
        # stupid inefficient, but that's what you get
        headers = tools.make_ctype(ext, self.default_mtype)
        return open(path).read(), 200, headers

    def render(self, path, variables):
        root, ext = os.path.splitext(path)
        realpath = os.path.realpath(self.app_path + path)

        if not realpath.startswith(self.app_path):
            # prevent access outside the app dir by comparing path roots
            return self.render_error(404, "Not Found", variables=variables)

        elif realpath.startswith(self.static_dir):
            return self.render_static(ext, realpath)

        elif ext:
            # if it has an extension it's a template
            return self.render_template(path, variables, ext=ext)

        elif path.endswith('/'):
            # if it ends in /, it's a /index.html or /index.py
            base = os.path.join(path, 'index')

            #! this will be hackable if you get rid of the realpath check at top
            if os.path.exists(self.app_path + base + '.html'):
                return self.render_template(base + '.html', variables, ext='.html')
            else:
                return self.render_module(path[:-1], variables)

        elif os.path.isdir(realpath):
            return "", 301, {'Location': path + '/'}

        else:
            # otherwise it's a module, tack on .py and load or fail
            return self.render_module(path, variables)


