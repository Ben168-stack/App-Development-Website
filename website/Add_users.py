from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path
from website import db, DB_NAME,bcrypt
from website.models import User
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # if database.db does not exist in this path it creates a database
        db.create_all(app=app)
        print('Created Database! ')

db.create_all()
app = Flask(__name__)
admin = User(username='gay', email_address='gay@example.com',password='1234567')
db.session.add(admin)
db.session.commit()