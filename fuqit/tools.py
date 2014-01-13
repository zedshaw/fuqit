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

import importlib
import mimetypes
import cgi
import os

mimetypes.init()

def module(name, app_name=None):
    if app_name:
        themodule = importlib.import_module("." + name, package=app_name)
    else:
        themodule = importlib.import_module(name)

    reload(themodule)
    return themodule


def build_context(params, handler):
    return {'params': params,
              'headers': handler.headers,
              'path': handler.path,
              'method': handler.command,
              'client_address': handler.client_address,
              'request_version': handler.request_version,
            }

def parse_request(path, request_body):
    request_params = {}

    if '?' in path:
        path, params = path.split('?', 1)
        params = cgi.parse_qsl(params)
        request_params.update(params)

    if request_body:
        params = cgi.parse_qsl(request_body)
        request_params.update(params)

    return path, request_params


def make_ctype(ext, default_mtype):
    mtype = mimetypes.types_map.get(ext, default_mtype)
    return {'Content-Type': mtype}



def find_longest_module(app, name, variables):
    base = name[1:]

    # need to limit the max we'll try to 20 for safety
    for i in xrange(0, 20):
        # go until we hit the /
        if base == '/' or base == '':
            return None, None

        modname = base.replace('/', '.')

        try:
            return base, module(modname, app)
        except ImportError, e:
            # split off the next chunk to try to load
            print "ERROR", e 
            base, tail = os.path.split(base)

    # exhausted the path limit
    return None, None


