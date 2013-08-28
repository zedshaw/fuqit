from fuqit.sessions import with_session

@with_session
def GET(variables, session):
    """
    You can either return a full tuple of (body, status, headers),
    or just a string and it's assumed you want 200 and default headers.
    """
    session['count'] = session.get('count', 1) + 1

    # need to do this since headers aren't really a dict
    heads = {}
    for key, values in variables.headers.items():
        heads[key] = values

    variables['headers'] = heads

    return "VARIABLES: %r\n\nSESSION: %r" % (variables, session), 200, {}

