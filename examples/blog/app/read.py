
def run(web):
    post_id = int(web.sub_path[1:])

    web.post = web.db.get('post', by_id=post_id)

    if not web.post:
        return web.app.render_error(404, "Not Found")
    else:
        return web.app.render('show_post.html', web)
