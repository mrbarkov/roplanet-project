from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from database import db
import psycopg2

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx'}
# DATABASE_CONNECTION = 'postgresql://roplanet:goodbdaka@database/roplanetdb'
DATABASE_CONNECTION = 'sqlite:///categories.db'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SESSION_COOKIE_SAMESITE'] = None
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Замените на свой секретный ключ
app.secret_key = 'check'
jwt = JWTManager(app)
api = Api(app)
db.init_app(app)
api.init_app(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS