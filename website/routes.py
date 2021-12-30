from website import app, bcrypt
from flask import render_template, request, flash, redirect, url_for
from website.models import User, Partners, Notes, Tickets, Tickets_Response, Item
from website.forms import RegisterForm, LoginForm, DepositForm, TransferFunds, CreatePartnerForm, UpdatePartnerForm, \
    Add_Notes, Update_Notes, Update_User, Update_Username, Update_Email, Update_Gender, Update_Password, Ticket_Form, \
    Ticket_Reply_Form, UpdateSupplierForm, Add_Item_Form, Purchase_Form
from website import db
from flask_login import login_user, logout_user, login_required, current_user
from website import admin_user
import shelve
from datetime import datetime
from uuid import uuid4  # Unique key generator
import os


# For Error Handling when user enters invalid url address
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


# Benjamin
# the '/' route is default route
@app.route('/')
@app.route('/home')
def home_page():
    admin_user()
    return render_template('home.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    update_username_form = Update_Username()
    update_email_form = Update_Email()
    update_gender_form = Update_Gender()
    update_password_form = Update_Password()
    if update_username_form.validate_on_submit:
        pass
    if update_username_form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in update_username_form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')
    return render_template('profile.html', username_form=update_username_form, email_form=update_email_form,
                           gender_form=update_gender_form, password_form=update_password_form)


@app.route('/deleteProfile')
@login_required
def delete_profile():
    db.create_all()
    userID = User.query.filter_by(id=current_user.id).first()
    db.session.delete(userID)
    db.session.commit()
    logout_user()
    flash("Account Deleted Successfully", category="success")
    return redirect(url_for("home_page"))


@app.route("/updateUser", methods=['GET', 'POST'])
def update_user():
    update_user_form = Update_User()
    if request.method == 'POST' and update_user_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=current_user.username).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=update_user_form.password1.data):
            userID = User.query.filter_by(id=current_user.id).first()
            # userID.password = bcrypt.generate_password_hash('update_user_form.password1').decode('utf-8')
            userID.username = update_user_form.username.data
            userID.email_address = update_user_form.email_address.data
            userID.gender = update_user_form.gender.data
            db.session.commit()
            flash("User Particulars changed successfully", category="success")
            return redirect(url_for("profile_page"))
        else:  # If there are not errors from the validations
            flash("Password is Incorrect Try again.", category='danger')
    if update_user_form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in update_user_form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')
    return render_template("UpdateUser.html", form=update_user_form)


@app.route("/updateUsername", methods=['GET', 'POST'])
def update_username():
    update_username_form = Update_Username()
    if request.method == 'POST' and update_username_form.validate_on_submit():
        userID = User.query.filter_by(id=current_user.id).first()
        userID.username = update_username_form.username.data
        db.session.commit()
        flash("Username changed successfully", category="success")
        return redirect(url_for("profile_page"))
    if update_username_form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in update_username_form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')
    return redirect(url_for('profile_page'))


@app.route("/updateEmail", methods=['GET', 'POST'])
def update_email():
    update_email_form = Update_Email()
    if request.method == 'POST' and update_email_form.validate_on_submit():
        userID = User.query.filter_by(id=current_user.id).first()
        userID.email_address = update_email_form.email_address.data
        db.session.commit()
        flash("Email changed successfully", category="success")
        return redirect(url_for("profile_page"))
    if update_email_form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in update_email_form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')
    return redirect(url_for('profile_page'))


@app.route("/updateGender", methods=['GET', 'POST'])
def update_gender():
    update_gender_form = Update_Gender()
    if request.method == 'POST' and update_gender_form.validate_on_submit():
        userID = User.query.filter_by(id=current_user.id).first()
        userID.gender = update_gender_form.gender.data
        db.session.commit()
        flash("Gender changed successfully", category="success")
        return redirect(url_for("profile_page"))
    if update_gender_form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in update_gender_form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')
    return redirect(url_for('profile_page'))


@app.route("/updatePassword", methods=['GET', 'POST'])
def update_password():
    update_password_form = Update_Password()
    userID = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST' and update_password_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=current_user.username).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=update_password_form.current_password.data):
            userID.password_hash = bcrypt.generate_password_hash(update_password_form.new_password.data).decode('utf-8')
            db.session.commit()
            flash("Password Changed Successfully", category="success")
        else:
            flash("Current Password is Incorrect.", category='danger')

        return redirect(url_for("profile_page"))
    if update_password_form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in update_password_form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')
    return redirect(url_for('profile_page'))


@app.route('/markets')
@login_required
def market_page():
    Items_Dict = {}
    try:
        Item_Database = shelve.open('website/databases/items/items.db', 'r')
        if 'ItemInfo' in Item_Database:
            Items_Dict = Item_Database['ItemInfo']
            Item_Database.close()
        else:
            Item_Database['ItemInfo'] = Items_Dict
            Item_Database.close()

    except IOError:
        print("Unable to Read File")

    except Exception as e:
        print(f"An unknown error has occurred,{e}")
    print("Market Database")
    print(Items_Dict)
    return render_template('market.html', items=Items_Dict)

@app.route('/PastOrders')
@login_required
def past_orders():
    Owned_Items_Dict = {}
    try:
        Owned_Items_Database = shelve.open('website/databases/Owned_Items/ownedItems.db', 'r')

        if str(current_user.id) in Owned_Items_Database:
            Owned_Items_Dict = Owned_Items_Database[str(current_user.id)]
            Owned_Items_Database.close()
        else:
            Owned_Items_Database[str(current_user.id)] = Owned_Items_Dict
            Owned_Items_Database.close()

    except IOError:
        print("Unable to Read File")

    except Exception as e:
        print(f"An unknown error has occurred,{e}")
    print(Owned_Items_Dict)

    return render_template('PastOrders.html',items=Owned_Items_Dict)


@app.route('/AddItemForm', methods=['POST', 'GET'])
@login_required
def Add_Item():
    add_item_form = Add_Item_Form()
    Items_Dict = {}
    unique_id = uuid4()
    try:
        Item_Database = shelve.open('website/databases/items/items.db', 'c')
        if 'ItemInfo' in Item_Database:
            Items_Dict = Item_Database['ItemInfo']
        else:
            Item_Database['ItemInfo'] = Items_Dict

    except IOError:
        print("Unable to Read File")

    except Exception as e:
        print(f"An unknown error has occurred,{e}")

    else:
        if add_item_form.validate_on_submit() and request.method == 'POST':
            while True:
                unique_id = uuid4()
                if str(unique_id) not in Items_Dict:
                    item = Item(id=str(unique_id),
                                name=add_item_form.name.data,
                                quantity=add_item_form.quantity.data,
                                description=add_item_form.description.data,
                                price=add_item_form.price.data,
                                owner=current_user.username,
                                owner_id=current_user.id
                                )
                    Items_Dict[str(unique_id)] = item
                    Item_Database['ItemInfo'] = Items_Dict
                    flash('Item Added Successfully', category='success')
                    print('Item added')
                    Item_Database.close()
                    break
                else:
                    continue

    return render_template('AddItem.html', add_item_form=add_item_form)


@app.route('/PurchaseItem', methods=['POST', 'GET'])
@login_required
def Purchase_Item():
    purchase_item_form = Purchase_Form()
    Items_Dict = {}
    Owned_Items_Dict = {}
    try:
        Item_Database = shelve.open('website/databases/items/items.db', 'c')
        Owned_Items_Database = shelve.open('website/databases/Owned_Items/ownedItems.db', 'c')

        if 'ItemInfo' in Item_Database:
            Items_Dict = Item_Database['ItemInfo']
        else:
            Item_Database['ItemInfo'] = Items_Dict

        if str(current_user.id) in Owned_Items_Database:
            Owned_Items_Dict = Owned_Items_Database[str(current_user.id)]
            print(Owned_Items_Database[str(current_user.id)])
        else:
            Owned_Items_Database[str(current_user.id)] = Owned_Items_Dict


    except IOError:
        print("Unable to Read File")

    except Exception as e:
        print(f"An unknown error has occurred,{e}")

    else:
        if request.method == 'POST':
            purchased_item = Items_Dict[str(request.form.get('uuid'))]
            if purchased_item.get_price()<= current_user.budget:
                if purchased_item.get_quantity() > 0:
                    item_quantity = Items_Dict[str(request.form.get('uuid'))].get_quantity()
                    # Minus Quantity of Item
                    item_quantity-=1
                    Items_Dict[str(request.form.get('uuid'))].set_quantity(item_quantity)
                    # Minus Balance of User
                    current_user.budget-=purchased_item.get_price()
                    db.session.commit()
                    Item_Database['ItemInfo'] = Items_Dict

                    Owned_Items_Dict[str(uuid4())] = purchased_item
                    Owned_Items_Database[str(current_user.id)] = Owned_Items_Dict
                    print("Owned items")
                    print(Owned_Items_Dict)
                    print(Owned_Items_Database[str(current_user.id)])
                    flash(f"{purchased_item.get_name()} Purchased Successfully",category='success')
                    Item_Database.close()
                    Owned_Items_Database.close()
                else:
                    flash(f"{purchased_item.get_name()} is out of stock", category='danger')
            else:
                flash(f"Insufficient funds to purchase {purchased_item.get_name()}",category='danger')


    return redirect(url_for('market_page'))


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
            ids += 1
            partner.set_id(ids)
            partners_dict[ids] = partner
            db_shelve['PartnerInfo'] = partners_dict
            db_shelve_uniqueID['ID'] = ids
            flash("Partner Added Successfully", category='success')
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
            return redirect(url_for('home_page'))
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
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        errors = []
        for err_msg in form.errors.values():
            errors.append(err_msg)
        err_message = '<br/>'.join([f'({number}){error[0]}' for number, error in enumerate(errors, start=1)])
        flash(f'{err_message}', category='danger')

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    # to log out the current logged in user
    flash("You have been logged out!", category='info')
    # the category for flash will decide the color of the flashed message
    # for instance 'info' is blue, 'danger' is red, 'success' is green.
    return redirect(url_for("login_page"))
    # redirects user to login page after they are logged out.


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    add_notes_form = Add_Notes()
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
            new_note = Notes(id=str(uuid4()),
                             title=add_notes_form.title.data,
                             description=add_notes_form.description.data,
                             time_added=datetime.now().strftime("%d/%m/%y %I:%M:%S:%p"),
                             time_updated=datetime.now().strftime("%d/%m/%y %I:%M:%S:%p"))
            user_notes[new_note.get_id()] = new_note
            notes_database[str(current_user.id)] = user_notes
            notes_database.close()
            flash("New Note Added", category='success')
            print(user_notes)
            for i in user_notes:
                print(f"{user_notes[i].get_id()}")
            return redirect(url_for("notes"))
    return render_template("notes.html", form=add_notes_form, user_notes=user_notes)


@app.route("/deleteNotes", methods=["GET", "POST"])
@login_required
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
@login_required
def updateNotes():
    if request.method == 'POST':
        update_notes_form = Update_Notes()
        notes_database = shelve.open('website/databases/Notes/note.db', 'w')
        user_notes = {}
        try:
            if str(current_user.id) not in notes_database:
                notes_database[str(current_user.id)] = user_notes
            else:
                user_notes = notes_database[str(current_user.id)]
        except KeyError:
            flash("No such note.", category="danger")
        except Exception as e:
            flash(f"An Unknown Error has occurred, {e}", category="danger")
        else:
            current_note = user_notes[str(request.form.get('uuid'))]
            current_note.set_title(request.form.get('title'))
            current_note.set_description(request.form.get('description'))
            current_note.set_time_updated(datetime.now().strftime("%d/%m/%y %I:%M:%S:%p"))
            notes_database[str(current_user.id)] = user_notes
            notes_database.close()
        return redirect(url_for("notes"))


# Ming Wei
@app.route('/landing')
def landing_page():
    return render_template('landingPage.html')


@app.route('/about_us', methods=['GET', 'POST'])
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


@app.route('/forgot_password')
def forgot_password_page():
    return render_template('forgot_password.html')


@app.route('/suppliers/create', methods=['GET', 'POST'])
@login_required
def create_supplier():
    from website.models import Suppliers
    from website.forms import CreateSupplierForm

    form = CreateSupplierForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            create_supplier_form = CreateSupplierForm()

            supplier_dict = {}
            supplier_db = shelve.open('website/databases/supplier/supplier.db', 'c')
            supplier_id_db = shelve.open('website/databases/supplier/supplier_id_db', 'c')
            id = 0

            try:
                try:
                    # if company data in database,
                    supplier_dict = supplier_db['Suppliers']
                except Exception as e:
                    flash(f"An unknown error, \"{e}\" has occured!")

                if "ID" in supplier_id_db:
                    id = supplier_id_db["ID"]

                else:
                    supplier_id_db['ID'] = id

                suppliers = Suppliers(id, create_supplier_form.company.data, create_supplier_form.remarks.data,
                                      create_supplier_form.email.data, create_supplier_form.phone.data)

                id += 1
                suppliers.set_supplier_id(id)
                supplier_dict[suppliers.get_supplier_id()] = suppliers
                supplier_db['Suppliers'] = supplier_dict
                supplier_id_db['ID'] = id
                supplier_db.close()

            except Exception as e:
                flash(f"{e} error occurred!", category='danger')
                supplier_db.close()

        return redirect(url_for('supplier_page'))
    return render_template("CreateSupplier.html", form=form)


@app.route('/suppliers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def update_supplier(id):
    form = UpdateSupplierForm()

    if request.method == "POST" and form.validate_on_submit():

        supplier_dict = {}
        supplier_db = shelve.open('website/databases/supplier/supplier.db', 'c')
        supplier_dict = supplier_db["Suppliers"]

        for key in supplier_dict:
            print(supplier_dict[key])

        supplier = supplier_dict.get(id)
        supplier.set_supplier_name(form.company.data)
        supplier.set_supplier_remarks(form.remarks.data)
        supplier.set_email(form.email.data)
        supplier.set_phone_number(form.email.data)

        supplier_db['Suppliers'] = supplier_dict
        supplier_db.close()

        return redirect(url_for('supplier_page'))
    else:
        supplier_dict = {}
        supplier_db = shelve.open('website/databases/supplier/supplier.db', 'c')
        supplier_dict = supplier_db['Suppliers']
        supplier_db.close()

        supplier = supplier_dict.get(id)
        form.company.data = supplier.get_supplier_name()
        form.remarks.data = supplier.get_supplier_remarks()
        form.email.data = supplier.get_email()
        form.phone.data = supplier.get_phone_number()

    return render_template('updateSupplier.html', form=form)


@app.route('/suppliers/delete/<int:id>', methods=['POST'])
@login_required
def supplier_delete(id):
    try:
        supplier_dict = {}
        supplier_db = shelve.open('website/databases/supplier/supplier.db', 'c')
        supplier_dict = supplier_db['Suppliers']

        current_id = supplier_dict.get(id)
        supplier_dict.pop(id)
        supplier_db['Suppliers'] = supplier_dict

        if current_id not in supplier_db['Suppliers']:
            flash("Deletion Successful!", category="success")
        else:
            flash("Deletion unsuccessful!", category='danger')

        supplier_db.close()

    except IOError:
        flash("Something went wrong with the database!", category='danger')

    # except Exception as e:
    #     flash(f"{e} went wrongly!")

    return redirect(url_for('supplier_page'))


@app.route('/suppliers')
@login_required
def supplier_page():
    supplier_dict = {}
    try:
        supplier_db = shelve.open('website/databases/supplier/supplier.db', 'r')
        supplier_dict = supplier_db['Suppliers']
        supplier_db.close()
    except IOError:
        print("Failed to read file")
    except Exception as e:
        print(f"An unknown error has occurred, {e}")

    supplier_list = []
    for key in supplier_dict:
        supplier = supplier_dict.get(key)
        supplier_list.append(supplier)

    return render_template('Supplier.html', count=len(supplier_list), supplier_list=supplier_list)


# Samuel


# Daniel


@app.route('/tickets', methods=['GET', 'POST'])
@login_required
def ticket_page():
    ticket_form = Ticket_Form()
    ticket_database = shelve.open('website/databases/Ticket/ticket.db', 'c')
    ticket_database_uniqueID = shelve.open('website/databases/Ticket/ticket_uniqueID.db', 'c')
    tickets = {}
    count = 0
    try:
        if 'TicketInfo' in ticket_database:
            tickets = ticket_database['TicketInfo']
        else:
            ticket_database['TicketInfo'] = tickets

        if 'ID' in ticket_database_uniqueID:
            count = ticket_database_uniqueID['ID']
        else:
            ticket_database_uniqueID['ID'] = count

    except IOError:
        flash("An Error Has Occurred Trying to Read The Database", category="error")
    except Exception as e:
        flash(f"An Unknown Error has occurred, {e}")
    if request.method == 'POST':
        ticket = Tickets(
            id=count,
            description=ticket_form.description.data,
            title=ticket_form.title.data,
            urgency=ticket_form.urgency.data,
            time_added=datetime.now().strftime("%d/%m/%y %I:%M:%S:%p"),
            owner=current_user.username,
            owner_id=current_user.id,
            pending='Pending'
        )
        count += 1
        tickets[count] = ticket
        print(tickets)
        ticket_database['TicketInfo'] = tickets
        ticket_database_uniqueID['ID'] = count
        ticket_database.close()
        ticket_database_uniqueID.close()
        flash("Ticket Sent Successfully", category='success')

    return render_template('ticket.html', form=ticket_form)


@app.route('/ticket_requests', methods=['GET', 'POST'])
@login_required
def ticket_requests_page():
    ticket_reply_form = Ticket_Reply_Form()
    tickets = {}
    count = 0
    try:
        ticket_database = shelve.open('website/databases/Ticket/ticket.db', 'r')
        ticket_database_uniqueID = shelve.open('website/databases/Ticket/ticket_uniqueID.db', 'r')
        if 'TicketInfo' in ticket_database:
            tickets = ticket_database['TicketInfo']
        else:
            ticket_database['TicketInfo'] = tickets

        if 'ID' in ticket_database_uniqueID:
            count = ticket_database_uniqueID['ID']
        else:
            ticket_database_uniqueID['ID'] = count

    except IOError:
        print("An Error Has Occurred Trying to Read The Database")
    except Exception as e:
        print(f"An Unknown Error has occurred, {e}")

    return render_template('ticketRequest.html', tickets=tickets, ticker_response=ticket_reply_form)


@app.route('/delete_ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_ticket_request(id):
    tickets = {}
    count = 0
    try:
        ticket_database = shelve.open('website/databases/Ticket/ticket.db', 'w')
        ticket_database_uniqueID = shelve.open('website/databases/Ticket/ticket_uniqueID.db', 'w')
        if 'TicketInfo' in ticket_database:
            tickets = ticket_database['TicketInfo']
        else:
            ticket_database['TicketInfo'] = tickets

        if 'ID' in ticket_database_uniqueID:
            count = ticket_database_uniqueID['ID']
        else:
            ticket_database_uniqueID['ID'] = count

    except IOError:
        print("An Error Has Occurred Trying to Read The Database")
    except Exception as e:
        print(f"An Unknown Error has occurred, {e}")

    else:
        del tickets[id]
        ticket_database['TicketInfo'] = tickets
        ticket_database.close()
        ticket_database_uniqueID.close()
    return redirect(url_for("ticket_requests_page"))


@app.route('/ticket_reply/<int:id>', methods=['GET', 'POST'])
@login_required
def ticket_reply(id):
    ticket_reply_form = Ticket_Reply_Form()
    tickets = {}
    tickets_response_dict = {}
    count = 0
    response_count = 0
    userID = User.query.filter_by(id=id).first()
    try:
        ticket_database = shelve.open('website/databases/Ticket/ticket.db', 'w')
        ticket_database_uniqueID = shelve.open('website/databases/Ticket/ticket_uniqueID.db', 'w')
        ticket_response_database = shelve.open('website/databases/Messages/messages.db', 'c')
        ticket_response_uniqueID = shelve.open('website/databases/Messages/messages_uniqueID', 'c')

        # Ticket Response Database
        if f'{userID}' in ticket_response_database:
            tickets_response_dict = ticket_response_database[f'{userID}']
        else:
            ticket_response_database[f'{userID}'] = tickets_response_dict

        if f'{userID}' in ticket_response_uniqueID:
            response_count = ticket_response_uniqueID[f'{userID}']
        else:
            ticket_response_uniqueID[f'{userID}'] = response_count

        # TicketInfo Database
        if 'TicketInfo' in ticket_database:
            tickets = ticket_database['TicketInfo']
        else:
            ticket_database['TicketInfo'] = tickets

        if 'ID' in ticket_database_uniqueID:
            count = ticket_database_uniqueID['ID']
        else:
            ticket_database_uniqueID['ID'] = count

    except IOError:
        print("An Error Has Occurred Trying to Read The Database")
    except Exception as e:
        print(f"An Unknown Error has occurred, {e}")

    else:
        if request.method == 'POST':
            if userID:
                ticket_response = Tickets_Response(
                    id=response_count,
                    description=ticket_reply_form.description.data,
                    title=ticket_reply_form.title.data,
                    time_added=datetime.now().strftime("%d/%m/%y %I:%M:%S:%p"),
                    owner=current_user.username,
                    status=ticket_reply_form.issue_status.data,
                    recipient=userID.username
                )

                tickets_response_dict[response_count] = ticket_response
                response_count += 1
                ticket_response_database[f'{userID}'] = tickets_response_dict
                ticket_response_uniqueID[f'{userID}'] = response_count
                # Fix Set Pending Status issue in morning pls
                ticket_response_database.close()
                ticket_response_uniqueID.close()
                ticket_database.close()
                ticket_database_uniqueID.close()
                flash(f"Ticket Response Sent Successfully to {userID.username}", category='success')
                userID.messages = len(tickets_response_dict)
            else:
                flash("User does not exist, user may have disabled or deleted his/her account", category='danger')

            db.session.commit()
    return redirect(url_for('ticket_requests_page'))


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages_page():
    userID = User.query.filter_by(id=current_user.id).first()
    tickets_response_dict = {}
    response_count = 0
    try:
        ticket_database = shelve.open('website/databases/Messages/messages.db', 'w')
        ticket_database_uniqueID = shelve.open('website/databases/Messages/messages_uniqueID', 'w')
        # Ticket Response Database
        if f'{userID}' in ticket_database:
            tickets_response_dict = ticket_database[f'{userID}']
            ticket_database.close()
        else:
            ticket_database[f'{userID}'] = tickets_response_dict
            ticket_database.close()

        if f'{userID}' in ticket_database_uniqueID:
            response_count = ticket_database_uniqueID[f'{userID}']
            ticket_database_uniqueID.close()
        else:
            ticket_database_uniqueID[f'{userID}'] = response_count
            ticket_database_uniqueID.close()

    except IOError:
        print("An Error Has Occurred Trying to Read The Database")
    except Exception as e:
        print(f"An Unknown Error has occurred, {e}")
    userID.messages = len(tickets_response_dict)
    db.session.commit()
    print(tickets_response_dict)
    print(response_count)

    return render_template('messages.html', tickets_response=tickets_response_dict)


@app.route('/delete_messages/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_messages_page(id):
    userID = User.query.filter_by(id=current_user.id).first()
    tickets_response_dict = {}
    response_count = 0

    try:
        ticket_response_database = shelve.open('website/databases/Messages/messages.db', 'c')
        ticket_response_uniqueID = shelve.open('website/databases/Messages/messages_uniqueID', 'c')

        # Ticket Response Database
        if f'{userID}' in ticket_response_database:
            tickets_response_dict = ticket_response_database[f'{userID}']
        else:
            ticket_response_database[f'{userID}'] = tickets_response_dict

        if f'{userID}' in ticket_response_uniqueID:
            response_count = ticket_response_uniqueID[f'{userID}']
        else:
            ticket_response_uniqueID[f'{userID}'] = response_count

    except IOError:
        print("An Error Has Occurred Trying to Read The Database")
    except Exception as e:
        print(f"An Unknown Error has occurred, {e}")

    else:
        del (tickets_response_dict[id])
        ticket_response_database[f'{userID}'] = tickets_response_dict
        ticket_response_database.close()
        ticket_response_uniqueID.close()
        userID.messages = len(tickets_response_dict)
        flash("Message Deleted", category='success')

    return redirect(url_for('messages_page'))
