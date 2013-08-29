The FuqIt Web Framework
=======================

I'm kind of tired of following the stupid rules of MVC and want to just
try out making something where I shit files into a directory and they
just work.  This Python web framework (if you can call it that) is my
first crack at something like that.  I basically did this on a Saturday
morning because I was bored.  If you don't like it, then oh well, life
goes on.

How It Works
============

1. mkdir app
2. touch app/__init__.py
4. mkdir app/static
4. python fuqit.py app 0.0.0.0 8080
5. Put .py files or "anything else" into app.
6. The .py files need a run function.  It gets variables.
7. Anything else is a jinja2 template.

That's it.  Look in this project's app/ directory to see me
doing stupid crap with it to see if it works.

Resolution Order
================

Easy, and oh so hackable so don't run this crap on any computer you
care about.

0. If it's in /static/ it's a static file.
1. If it has an extension it's a template.
2. If it ends in / it's either /index.html or a module.
3. Otherwise it's a module named after the path with / changed to .
unless there is a directory with the same path, then this will produce a redirect.
4. Modules are found by trying to import longest to shortest paths.

Examples:

* / -> /index.html or /index.py
* /the/stupid/place/stuff.txt -> jinja template same path
* /the/other/place/index.html -> same thing
* /mystuff/cool -> a module named app.mystuff.cool
* /dir/that/exists -> redirect to /dir/that/exists/
* /mymodule/the/path/after/that -> import mymodule.py give it sub_path=/the/path/after/that

It uses the python mimetypes module to figure out mimetypes by extension. No, I don't
know how to add new extensions to it.

Sessions
========

It has ephemeral sessions based on cookies, which means that they go away when you reboot the
process.  To use sessions you can either use them raw from fuqit/sessions.py or just do this:

    from fuqit.sessions import with_session 

    @with_session
    def GET(variables, session):
        session['count'] = session.get('count', 1) + 1
        return "COUNT: %d" % session['count']


Using It
========

You can play with the example by doing this::

    ./bin/fuqit run -chroot examples -app app

Then go to http://127.0.0.1:8000/ and you'll get my little demo testing app.
It's in the app directory and just has some files for testing the rendering.

You can get help for run with:

    ./bin/fuqit help -for run


Writing A .html Handler
=======================

Here's how you do it:

1. Make a .html file in the app directory.
2. Put jinja2 syntax stuff in it.
3. You get a web variable to play with that has all the gear, including sessions, headers, response\_headers, and a module function for easily loading code.
4. Hit it with a browser.  That's it.


Writing A Module Handler
========================

Here's how you do it:

1. Make a .py file with the name you want.
2. Put either a run, GET, or POST method in it.  run handles every possible request, GET or POST handles just those.
3. Your method will get one parameter, web, which has .session, .headers, .app, and everything.
4. Return a string for the body; a body, code, headers tuple; or just call web.app.render("somefuqitpath.html", web)

Remember that if you have say /myapp.py and you get a URL of /myapp/stuff/things, then this module will run and it'll get
a web.sub\_path == '/stuff/things'.

Static Files
============

Here's how you do it:

1. mkdir app/static
2. Put the static crap in there.
3. Any URL with /static/ in front serves out of there.

If you actually host it you should have your fronting web server serve them straight out of there.

Databasing
==========

FuqIt took the public domain web.py database module and uses that.  The best docs for it is currently from
the Web.py folks over at <http://webpy.org/docs/0.3/tutorial#databasing>.

Keep in mind that it's not too usable right now as you can really only get at the database by using the
raw API and doing it in modules.  Later versions will make that easier.


But That's Magic!
=================

I will refer you to our official Mascot:

![Magic Is Awesome](https://raw.github.com/zedshaw/fuqit/master/examples/app/static/mascot.gif)

Investor Statement
==================

Do you have a load of money and are you looking for the next Meteor to waste it
on?  Well this project is currently looking for funding and it's already been
on the top of HackerNews!

![HN Too Easy](https://raw.github.com/zedshaw/fuqit/master/examples/app/static/hn_win.png)

Act fast because pretty soon I'll have a spare Sunday and FuqIt will become
more secure than both Meteor and Ruby On Rails and then you'll miss out on
investing in the next hottest thing.  You'll have to go buy some Gucci hand
bags or a DVF dress to be in-fashion instead.  Can't have that now.


