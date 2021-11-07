from website import app
from flask import render_template
# from flask_login import login_user, logout_user
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about_us')
def about_us_page():
    return render_template('aboutUs.html')

@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/register')
def register_page():
    return render_template('register.html')
@app.route('/forgot_password')
def forgot_password_page():
    return render_template('forgot_password.html')