from website import app
from flask import render_template, request, flash, redirect, url_for
from website.models import User, Partners, Notes
from website.forms import RegisterForm, LoginForm, DepositForm, TransferFunds, CreatePartnerForm, UpdatePartnerForm, Add_Notes, Update_Notes
from website import db
from flask_login import login_user, logout_user, login_required, current_user
from website import admin_user
import shelve
from datetime import datetime
from uuid import uuid4 # Unique key generator


# the '/' route is default route
@app.route('/')
@app.route('/home')
def home_page():
    admin_user()
    return render_template('home.html')


@app.route('/profile')
def profile_page():
    return render_template('profile.html')


@app.route('/landing')
def landing_page():
    return render_template('landingPage.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.route('/about_us', methods=['GET', 'POST'])
@login_required
def about_us_page():
    return render_template('aboutUs.html')


@app.route('/add_partners', methods=['GET', 'POST'])
@login_required
def add_partners_page():
    form = CreatePartnerForm()
    db_shelve = shelve.open('website/databases/partners/partner.db', 'c')
    db_shelve_uniqueID = shelve.open('website/databases/partners/partner_uniqueID.db', 'c')
    partners_dict = {}
    ids = 0
    try:
        if 'PartnerInfo' in db_shelve:
            partners_dict = db_shelve['PartnerInfo']
        else:
            db_shelve['PartnerInfo'] = partners_dict
        if 'ID' in db_shelve_uniqueID:
            ids = db_shelve_uniqueID['ID']
        else:
            db_shelve_uniqueID['ID'] = ids
    except:
        print("Error in retrieving Partner from database")

    if request.method == 'POST':
        if form.validate_on_submit():
            partner = Partners(name=form.name.data,
                               location=form.location.data,
                               email=form.email.data)
            ids+=1
            partner.set_id(ids)
            partners_dict[ids] = partner
            db_shelve['PartnerInfo'] = partners_dict
            db_shelve_uniqueID['ID'] = ids
            flash("Partner Added Successfully",category='success')
            db_shelve.close()
            db_shelve_uniqueID.close()
            return redirect(url_for('partners_page'))
        else:
            flash("An Error Occurred trying to submit Form", category='danger')
            return redirect(url_for('add_partners_page'))
    if form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')

    if request.method == 'GET':
        return render_template('AddPartner.html', form=form)


@app.route('/partners')
@login_required
def partners_page():
    partners_dict = {}
    try:
        db_shelve = shelve.open('website/databases/partners/partner.db', 'r')
        partners_dict = db_shelve['PartnerInfo']
        db_shelve.close()
    except IOError:
        print("Error trying to read file")

    except Exception as e:
        print(f"An unknown error has occurred,{e}")

    partners_list = []
    for key in partners_dict:
        partner = partners_dict.get(key)
        partners_list.append(partner)

    return render_template('Partner.html', count=len(partners_list), partners=partners_list)

@app.route('/deletePartner/<int:id>', methods=['POST'])
def delete_partner(id):
    partner_dict = {}
    db_shelve = shelve.open('website/databases/partners/partner.db', 'w')
    partner_dict = db_shelve['PartnerInfo']
    partner_dict.pop(id)
    db_shelve['PartnerInfo'] = partner_dict
    db_shelve.close()

    return redirect(url_for('partners_page'))

@app.route('/updatePartner/<int:id>', methods=['POST'])
def update_partner(id):
    form = UpdatePartnerForm()
    if request.method == 'POST' and form.validate_on_submit():
        partner_dict = {}
        db_shelve = shelve.open('website/databases/partners/partner.db', 'w')
        partner_dict = db_shelve['PartnerInfo']
        partner = partner_dict.get(id)
        partner.set_name(form.name.data)
        partner.set_location(form.location.data)
        partner.set_email(form.email.data)
        partner.set_date(datetime.now().strftime("%d/%m/%Y"))
        db_shelve['PartnerInfo'] = partner_dict
        db_shelve.close()
        return redirect(url_for('partners_page'))
    else:
        partners_dict = {}
        db_shelve = shelve.open('website/databases/partners/partner.db', 'r')
        partners_dict = db_shelve['PartnerInfo']
        db_shelve.close()
        partner = partners_dict.get(id)
        form.name.data = partner.get_name()
        form.location.data = partner.get_location()
        form.email.data = partner.get_email()

        return render_template('updatePartner.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/charts')
@login_required
def charts_page():
    return render_template('charts.html')


@app.route('/markets')
@login_required
def market_page():
    return render_template('market.html')


@app.route('/transfer_funds')
@login_required
def transfer_funds_page():
    users = User.query.all()
    return render_template('TransferFunds.html', users=users)


@app.route('/transfer_funds_user/<int:id>', methods=['POST'])
@login_required
def transfer_funds_user_page(id):
    userID = User.query.filter_by(id=id).first()
    username = userID.username
    form = TransferFunds()
    if request.method == 'POST':
        if form.validate_on_submit():
            currentuserID = User.query.filter_by(id=current_user.id).first()
            userID.budget += form.transfer.data
            currentuserID.budget -= form.transfer.data
            db.session.commit()
            flash("Amount transferred successfully", category='success')
        return render_template('transferUserFunds.html', form=form, username=username)

    if request.method == 'GET':
        return render_template('transferUserFunds.html', form=form, username=username)


@app.route('/login', methods=['GET', 'POST'])
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
        flash(f"Success! You are logged in as: {user_to_create.username}", category='success')
        return redirect(url_for('about_us_page'))
    if form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')

    return render_template('register.html', form=form)


@app.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    db.create_all()
    form = DepositForm()
    if request.method == 'POST':
        if form.validate_on_submit() and current_user.can_deposit(form.budget.data):
            userID = User.query.filter_by(id=current_user.id).first()
            userID.budget += form.budget.data
            db.session.commit()
            flash("Amount added successfully", category='success')
        else:
            flash("Cannot deposit an amount less or equal to 0!", category='danger')
        return redirect(url_for('deposit'))
    if request.method == 'GET':
        return render_template('Deposit.html', form=form)


@app.route('/forgot_password')
def forgot_password_page():
    return render_template('forgot_password.html')


@app.route('/updateUser', methods=['GET', 'POST'])
def update_User(id):
    return render_template('UpdateUser.html')


@app.route('/logout')
def logout_page():
    logout_user()
    # to log out the current logged in user
    flash("You have been logged out!", category='info')
    # the category for flash will decide the color of the flashed message
    # for instance 'info' is blue, 'danger' is red, 'success' is green.
    return redirect(url_for("login_page"))
    # redirects user to login page after they are logged out.

@app.route("/notes", methods=["GET", "POST"])
def notes():
    add_notes_form = Add_Notes()
    update_notes_form = Update_Notes()
    notes_database = shelve.open('website/databases/Notes/note.db', 'c')
    user_notes = {}
    try:
        if str(current_user.id) not in notes_database:
            notes_database[str(current_user.id)] = user_notes
        else:
            user_notes = notes_database[str(current_user.id)]
    except IOError:
        flash("An Error Has Occurred Trying to Read The Database", category="error")
    except Exception as e:
        flash(f"An Unknown Error has occurred, {e}")
    else:
        if request.method == "POST":
            new_note = Notes(id = str(uuid4()),
                             title = add_notes_form.title.data,
                             description = add_notes_form.description.data,
                             time_added = datetime.now().strftime("%d/%m/%y %I:%M:%S:%p"),
                             time_updated = datetime.now().strftime("%d/%m/%y %I:%M:%S:%p"))
            user_notes[new_note.get_id()] = new_note
            notes_database[str(current_user.id)] = user_notes
            notes_database.close()
            flash("New Note Added", category='success')
            return redirect(url_for("notes"))
    return render_template("notes.html", form = add_notes_form, update_form=update_notes_form ,user_notes = user_notes)

@app.route("/deleteNotes", methods=["GET", "POST"])
def deleteNotes():
    if request.method == "POST":
        notes_database = shelve.open('website/databases/Notes/note.db', 'w')
        user_notes = {}
        try:
            if str(current_user.id) not in notes_database:
                notes_database[str(current_user.id)] = user_notes
            else:
                user_notes = notes_database[str(current_user.id)]
        except KeyError:
            flash("No such note.", category="error")
        except Exception as e:
            flash(f"An Unknown Error has occurred, {e}")
        else:
            del user_notes[str(request.form.get('uuid'))]
            notes_database[str(current_user.id)] = user_notes
            notes_database.close()
    return redirect(url_for("notes"))

@app.route('/updateNotes', methods=["GET", "POST"])
def updateNotes():
    update_notes_form = Update_Notes()
    notes_database = shelve.open('website/databases/Notes/note.db', 'w')
    user_notes = {}
    try:
        if str(current_user.id) not in notes_database:
            notes_database[str(current_user.id)] = user_notes
        else:
            user_notes = notes_database[str(current_user.id)]
    except KeyError:
        flash("No such note.", category="error")
    except Exception as e:
        flash(f"An Unknown Error has occurred, {e}")
    else:
        if request.method == 'POST':
            current_note = user_notes[str(request.form.get('uuid'))]
            current_note.set_title(update_notes_form.title.data)
            current_note.set_description(update_notes_form.description.data)
            current_note.set_time_updated(datetime.now().strftime("%d/%m/%y %I:%M:%S:%p"))
            notes_database.close()
            flas
            return redirect(url_for("notes"))
        if request.method == 'GET':
            return redirect(url_for("updateNotes"))




