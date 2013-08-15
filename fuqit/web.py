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
from fuqit import tools

class App(object):

    def __init__(self, app, default_mtype=None, static_dir=None):
        self.app_path = os.path.realpath(app)
        self.app = app
        self.static_dir = os.path.realpath(self.app_path +
                                           (static_dir or '/static/'))
        self.default_mtype = default_mtype or 'text/html'
        self.env = Environment(loader=PackageLoader(self.app, '.'))

    def process(self, method, path, params, context):
        try:
            return self.knife_or_banana(path, context)
        except TemplateNotFound:
            return "", 404, {}
        #except Exception as e:
        #    # TODO: log the exception here
        #    return str(e), 500, {}

    def render_template(self, ext, path, variables):
        headers = tools.make_ctype(ext, self.default_mtype)
        template = self.env.get_template(path)
        return template.render(**variables), 200, headers

    def render_module(self, name, variables):
        base, ext = os.path.splitext(name[1:])
        base = base.replace('/', '.')
        target = tools.module(base)
        result = target.run(variables)

        if isinstance(result, tuple):
            return result
        else:
            return result, 200, {'Content-Type': self.default_mtype}

    def render_static(self, ext, path):
        # stupid inefficient, but that's what you get
        headers = tools.make_ctype(ext, self.default_mtype)
        return open(path).read(), 200, headers

    def knife_or_banana(self, path, variables):
        root, ext = os.path.splitext(path)
        realpath = os.path.realpath(self.app_path + path)

        if not realpath.startswith(self.app_path):
            # prevent access outside the app dir by comparing path roots
            return "", 404, {}

        elif realpath.startswith(self.static_dir):
            return self.render_static(ext, realpath)

        elif ext:
            # if it has an extension it's a template
            return self.render_template(ext, path, variables)

        elif path.endswith('/'):
            # if it ends in /, it's a /index.html or /index.py
            base = os.path.join(path, 'index')
            print "BASE", base

            #! this will be hackable if you get rid of the realpath check at top
            if os.path.exists(self.app_path + base + '.html'):
                return self.render_template('.html', base + '.html', variables)
            elif os.path.exists(self.app + base + '.py'):
                return self.render_module(base + '.py', variables)

        elif os.path.isdir(realpath):
            return "", 301, {'Location': path + '/'}

        else:
            # otherwise it's a module, tack on .py and load or fail
            return self.render_module(path + '.py', variables)



