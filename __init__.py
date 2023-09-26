from flask import Flask
from flask_restful import Api

from database import db
import psycopg2

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'xls', 'xlsx'}
DATABASE_CONNECTION = 'postgresql://roplanet:goodbdaka@database/roplanetdb'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SESSION_COOKIE_SAMESITE'] = None
app.secret_key = 'check'
api = Api(app)
db.init_app(app)
api.init_app(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS