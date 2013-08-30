
def GET(web):
    return web.app.render("write_post.html", web)

def POST(web):
    web.db.insert('post',
              title=web.params['title'],
              content=web.params['content'])


    return web.app.redirect("/")
