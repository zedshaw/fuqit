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

from importlib import import_module
import mimetypes
import cgi

__all__ = ['module']

mimetypes.init()

def module(name):
    themodule = import_module("." + name, package="app")
    return themodule

def build_context(params, handler):
    variables = {'web': 
                 {'params': params,
                  'headers': handler.headers,
                  'path': handler.path,
                  'method': handler.command,
                  'client_address': handler.client_address,
                  'request_version': handler.request_version,
                 },
                 'module': module,
                }
    return variables

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




