
def GET(web):
    """
    This shows how to do a simple database setup. You can also just
    import the db inside the .html file if you want and don't need
    to go to a handler first.
    """
    if web.sub_path == '/delete':
        web.db.delete('test', where='id = $id', vars=web.params)

    return web.app.render("showdb.html", web)

def POST(web):
    web.db.insert('test', title=web.params['title'])
    return web.app.redirect("/dbtest")

