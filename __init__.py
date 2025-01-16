from flask import Flask
from flask_migrate import Migrate
import pymysql
from dotenv import load_dotenv
import os
from flask_restx import Api
from flask_cors import CORS

api = Api(
    version='1.0',
    title='blog_project',
    prefix='/api',
    contact='',
    contact_email='email address',
    description="desc",
)
# .env 파일 auto load
load_dotenv()

migrate = Migrate()
TESTING = False
SECRET_KEY = os.getenv('SECRET_KEY')

DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PWD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_NAME = os.getenv('DB_NAME')

db = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8')

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    api.init_app(app)
    
    
    from blog_backend.routes import routes_list
    routes_list(app)

    return app
