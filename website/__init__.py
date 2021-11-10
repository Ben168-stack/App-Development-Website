from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from os import path

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # if database.db does not exist in this path it creates a database
        db.create_all(app=app)
        print('Created Database! ')

app = Flask(__name__)
DB_NAME = 'database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
# create location/path for database
app.config['SECRET_KEY']= '8fc3212d5891a594defe7d20'
db = SQLAlchemy(app)
# enables the database
create_database(app)

bcrypt = Bcrypt(app)
# hashes the passwords 'utf-8' is used check 'models.py'


login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
# makes the message flashed blue when user is not authorised/logged in.
from website import routes

