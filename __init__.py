from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_restx import Api
from flask_cors import CORS

api = Api(
    version='1.0',
    title='blog_project',
    prefix='/api',
    contact='',
    contact_emrrn="desc",
)
# .env 파일 auto load
load_dotenv()

migrate = Migrate()
TESTING = False

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})
    api.init_app(app)
    
    
    from blog_backend.routes import routes_list
    routes_list(app)

    return app
