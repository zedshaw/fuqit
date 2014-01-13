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
import os

config = None # this gets set by calling configure below

class RequestDict(dict):
    __getattr__ = dict.__getitem__


def render_error(code, message="", variables=None):
    try:
        return render_template(config.errors_dir + '%d.html' %
                                    code, variables or {}, ext='.html')
    except TemplateNotFound:
        return message, code, {}

def csrf_check(context):
    referer = context['headers'].get('referer', '')

    if referer:
        return config.allowed_referer.match(referer)
    else:
        return True

def process(method, path, params, context):
    if not csrf_check(context):
        return render_error(404, "Not Found")

    try:
        return render(path, context)
    except TemplateNotFound:
        print "Jinja2 template missing in path: %r for context %r" % (path, context)
        traceback.print_exc()
        return render_error(404, "Not Found")
    except Exception as e:
        traceback.print_exc()
        return render_error(500, str(e))

def render_template(path, variables, ext=None):
    ext = ext or os.path.splitext(path)[1]
    headers = tools.make_ctype(ext, config.default_mtype)

    if 'headers' in variables:
        sessions.load_session(variables)

    context = {'web': variables,
               'module': tools.module,
               'response_headers': headers,
               'config': config,
               'db': config.db, # it's so common
              }

    template = config.env.get_template(path)
    result = template.render(**context)

    if 'headers' in variables:
        sessions.save_session(variables, headers)

    return result, 200, headers


def render_module(name, variables):
    base, target = tools.find_longest_module(config.app_moudle, name, variables)

    if not (base and target):
        return render_error(404, "Not Found", variables=variables)
        
    variables['base_path'] = base
    variables['sub_path'] = name[len(base)+1:]
    sessions.load_session(variables)

    context = RequestDict(variables)

    if target:
        try:
            actions = target.__dict__
            # TODO: need to white-list context.method
            func = actions.get(context.method, None) or actions['run']
        except KeyError:
            return render_error(500, 'No run method or %s method.' %
                                     context.method)

        result = func(context)

        session_headers = {}
        sessions.save_session(variables, session_headers)

        if isinstance(result, tuple):
            body, code, headers = result
            headers.update(session_headers)
            return body, code, headers
        else:
            session_headers['Content-type'] = config.default_mtype
            return result, 200, session_headers
    else:
        return render_error(404, "Not Found", variables=variables)

def render_static(ext, path):
    # stupid inefficient, but that's what you get
    headers = tools.make_ctype(ext, config.default_mtype)

    try:
        return open(path).read(), 200, headers
    except IOError:
        return render_error(404, "Not Found")

def render(path, variables):
    assert config, "You need to call fuqit.web.configure."

    root, ext = os.path.splitext(path)
    realpath = os.path.realpath(config.app_path + path)

    if not realpath.startswith(config.app_path) or ext == ".py":
        # prevent access outside the app dir by comparing path roots
        return render_error(404, "Not Found", variables=variables)

    elif realpath.startswith(config.static_dir):
        return render_static(ext, realpath)

    elif ext:
        # if it has an extension it's a template
        return render_template(path, variables, ext=ext)

    elif path.endswith('/'):
        # if it ends in /, it's a /index.html or /index.py
        base = os.path.join(path, 'index')

        #! this will be hackable if you get rid of the realpath check at top
        if os.path.exists(config.app_path + base + '.html'):
            return render_template(base + '.html', variables, ext='.html')
        else:
            return render_module(path[:-1], variables)

    elif os.path.isdir(realpath):
        return "", 301, {'Location': path + '/'}

    else:
        # otherwise it's a module, tack on .py and load or fail
        return render_module(path, variables)

def redirect(path):
    """
    Simple redirect function for most of the interaction you need to do.
    """
    return "", 301, {'Location': path}

def error(code, message):
    return render_error(code, message)

def configure(app_module="app", config_module="config"):
    global config

    if not config:
        config = tools.module(config_module)
        config.app_module = app_module
        config.app_path = os.path.realpath(app_module)
        config.errors_dir = config.app_path + '/errors/'
        config.env = Environment(loader=PackageLoader(config.app_module, '.'))
        config.allowed_referer = re.compile(config.allowed_referer)
        config.static_dir = os.path.realpath(config.app_path +
                                           (config.static_dir or '/static/'))


