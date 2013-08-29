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

from modargs import args
import fuqit
import os
import sys

def help_command(**options):
    """
    Prints out help for the commands. 

    fuqit help

    You can get help for one command with:

    fuqit help -for STR
    """

    if "for" in options:
        help_text = args.help_for_command(fuqit.commands, options['for'])

        if help_text:
            print help_text
        else:
            args.invalid_command_message(fuqit.commands, exit_on_error=True)
    else:
        print "Available commands:\n"
        print ", ".join(args.available_commands(fuqit.commands))
        print "\nUse fuqit help -for <command> to find out more."


def init_command(into=None):
    """
    Initializes a fuqit app, default directory is 'app'.

    fuqit init -into myapp
    """

    if not os.path.exists(into):

        for newdir in ['/', '/app', '/app/static']:
            os.mkdir(into + newdir)

        open(into + '/app/__init__.py', 'w').close()
        with open(into + '/config.py', 'w') as config:
            config.write("from fuqit import data\n\ndb = data.database(dbn='sqlite', db='data.sqlite3')")

        with open(into + '/app/index.html', 'w') as index:
            index.write('Put your crap in %s/app and hit rephresh.' % into)

        print "Your app is ready for hackings in %s" % into

    else:
        print "The app directory already exists. Try:\n\nfuqit init -into [SOMEDIR]"


def run_command(host='127.0.0.1', port=8000, referer='http://', app='app',
                debug=True, chroot="."):
    """
    Runs a fuqit server.

    fuqit run -host 127.0.0.1 -port 8000 -referer http:// -app app -debug True \
            -chroot .

    NOTE: In run mode it's meant for developers, so -chroot just does a cd
    to the directory.  In server mode it actually chroots there.  It also
    adds the chroot path to the python syspath.

    """
    from fuqit import server

    sys.path.append(os.path.realpath(chroot))
    os.chdir(chroot)
    
    server.run_server(host=host,
                            port=port,
                            referer=referer,
                            app=app,
                            debug=debug)


def start_command(host='127.0.0.1', port=8000, referer='http://', app='app',
                   debug=True, chroot="."):
    """
    Runs the fuqit server as a daemon.

    fuqit start -host 127.0.0.1 -port 8000 -referer http:// -app app -debug True
    """

   
def stop_command():
    """
    Stops a running fuqit daemon.

    fuqit stop
    """


def status_command():
    """
    Tells you if a running fuqit service is running or not.

    fuqit status
    """



