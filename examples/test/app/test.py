from fuqit import forms


def GET(web):
    """
    Demonstrates using the session and also how to then render another
    thing seamlessly.  Just call web.app.render() and it'll do all the
    resolving gear again, so one method works on statics, modules, jinja2
    just like you accessed it from a browser.
    """
    web.form = forms.read(web.params, reset=False)

    if web.form.reset:
        web.session['count'] = 1
    else:
        web.session['count'] = web.session.get('count', 1) + 1

    return web.app.render('renderme.html', web)
