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

import datetime
import re
import os

expires_format = "%a, %d-%b-%Y %X GMT"

SESSION_PATTERN = re.compile('FuqitSession\s*=\s*([A-Fa-f0-9]+)')
SESSION_TIMEOUT = 100 # days
SESSION_STORE = {}

def make_random_id():
    return os.urandom(64/8).encode('hex_codec')

def get_session_id(headers):
    cookies = headers.get('cookie', None)

    if cookies:
        sid_match = SESSION_PATTERN.search(cookies)

        if sid_match:
            return sid_match.group(1)
        else:
            return make_random_id()
    else:
        return make_random_id()

def set_session_id(headers, session_id):
    dt = datetime.timedelta(days=SESSION_TIMEOUT)
    diff = datetime.datetime.now() + dt
    stamp = diff.strftime(expires_format)

    cookies = {'Set-Cookie': 'FuqitSession=%s; version=1; path=/; expires=%s' % (session_id, stamp),
                'Cookie': 'FuqitSession=%s; version=1; path=/; expires=%s' % (session_id, stamp)}

    headers.update(cookies)

def load_session(headers):
    session_id = get_session_id(headers)
    return session_id, SESSION_STORE.get(session_id, {})

def save_session(session_id, session, headers):
    set_session_id(headers, session_id)
    SESSION_STORE[session_id] = session


def with_session(handler):

    def sessioned_handler(variables):
        session_id, session = load_session(variables.headers)
        results = handler(variables, session)

        if isinstance(results, tuple):
            resp, code, headers = results
            save_session(session_id, session, headers)
            return resp, code, headers
        else:
            headers = {}
            save_session(session_id, session, headers)
            return results, 200, headers

    return sessioned_handler


