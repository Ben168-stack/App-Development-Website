from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path
from website import db, DB_NAME,bcrypt
from website.models import User


db.create_all()
app = Flask(__name__)
admin = User(admin=1,username='admin2', email_address='admin2@example.com',password='admin123',gender='Rather not say')
db.session.add(admin)
db.session.commit()