from website import app
from flask import render_template, request, flash, redirect, url_for
from website.models import User
from website.forms import RegisterForm, LoginForm
from website import db, bcrypt
from flask_login import login_user,logout_user, login_required

def updateUser(id):
    userID = User.query.filter_by(id = id).first()
    userID.username = 'newadminuser'
    db.session.commit()
    # Get ID of specific user
    # userID = User.query.filter_by(id=id).first()
    # For password
    # userID.password_hash = bcrypt.generate_password_hash('1234567').decode('utf-8')
    # For Email
    # userID.email_address = 'newemail@gmail.com'
    # For Username
    # userID.username = 'newusername'
    # For Budget
    # userID.budget = 20000
    return userID.username




print(updateUser(5))