from fuqit.sessions import with_session

@with_session
def GET(variables, session):
    """
    You can either return a full tuple of (body, status, headers),
    or just a string and it's assumed you want 200 and default headers.
    """
    session['count'] = session.get('count', 1) + 1

    response = "COUNT: %d" % session['count']

    for k,v in variables.headers.items():
        response += "\n%r: %r" % (k,v)

    return "HEADERS: %s" % response, 200, {}

