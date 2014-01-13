from fuqit.web import render, error
from config import db

def run(web):
    post_id = web.sub_path[1:]

    if not post_id: return error(404, "Not Found")

    web.post = db.get('post', by_id=post_id)

    if web.post:
        return render('show_post.html', web)
    else:
        return error(404, "Not Found")

