from fuqit.web import render, redirect
from config import db


def GET(web):
    return render("write_post.html", web)

def POST(web):
    db.insert('post',
              title=web.params['title'],
              content=web.params['content'])


    return redirect("/")
