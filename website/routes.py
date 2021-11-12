from website import app
from flask import render_template, request, flash, redirect, url_for
from website.models import User
from website.forms import RegisterForm, LoginForm
from website import db
from flask_login import login_user,logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about_us', methods=['GET', 'POST'])
@login_required
def about_us_page():
    return render_template('aboutUs.html')

@app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/charts')
@login_required
def charts_page():
    return render_template('charts.html')

@app.route('/tables')
@login_required
def table_page():
    return render_template('tables.html')
@app.route('/login', methods = ['GET','POST'])
def login_page():
    db.create_all()
    # warning very funny error when logging in if passwords are not hashed(check SQlite) it will crash
    # giving an error of Invalid salt Value error
    form = LoginForm()
    if form.validate_on_submit():
        # if user exist and if password is correct
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # checks username for valid user and checks if password is correct
            login_user(attempted_user)
            # 'login_user' is a built in function for flask_login
            flash(f"Success! You are logged in as: {attempted_user.username}", category='success')
            return redirect(url_for('about_us_page'))
        else:
            flash("Username and Password are not matched! Please try again.", category='danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    db.create_all()
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
                              # 'password' = form.password1.data this is entering the hashed
                              # version of the password. Check models.py,
                              # @password.setter hashes the passwords
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        return redirect(url_for('about_us_page'))
    if form.errors != {}: #If there are not errors from the validations
        errors = []
        for err_msg in form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')

    return render_template('register.html', form=form)



@app.route('/forgot_password')
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/logout')
def logout_page():
    logout_user()
    # to log out the current logged in user
    flash("You have been logged out!", category='info')
    # the category for flash will decide the color of the flashed message
    # for instance 'info' is blue, 'danger' is red, 'success' is green.
    return redirect(url_for("home_page"))
    # redirects user to home page after they are logged out.
