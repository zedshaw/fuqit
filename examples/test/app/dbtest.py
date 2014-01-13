from fuqit.web import render, redirect
from config import db

def GET(web):
    """
    This shows how to do a simple database setup. You can also just
    import the db inside the .html file if you want and don't need
    to go to a handler first.
    """
    if web.sub_path == '/delete':
        db.delete('test', where='id = $id', vars=web.params)

    return render("showdb.html", web)

def POST(web):
    db.insert('test', title=web.params['title'])
    return redirect("/dbtest")

