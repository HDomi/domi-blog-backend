from blog_backend import api
from blog_backend.controllers.post_controller import post

def routes_list(app):
    api.add_namespace(post)
    return app