from blog_backend import api
from blog_backend.controllers.post_controller import ROUTER

def routes_list(app):
    api.add_namespace(ROUTER)
    return app
