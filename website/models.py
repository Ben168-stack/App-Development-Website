from flask_login import UserMixin
from website import bcrypt
from website import db, login_manager
from datetime import datetime
import random
import string
from uuid import uuid4
import shelve
from sqlalchemy import func


# Benjamin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# For Login System Helps Identify the log in ID of current user trying log in

# convert received user id into an integer

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    admin = db.Column(db.Integer())
    # the id unique to each user so that flask can identify each individual user
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False, unique=True)
    # the mostly used hashing algorithm that flask allow us to use
    # will always convert the passwords to being 60 characters
    # thats why length is set to 60
    date = db.Column(db.String(), default=datetime.now().strftime("%d/%m/%Y"))
    budget = db.Column(db.Integer(), nullable=False, default=10000)
    gender = db.Column(db.String(), nullable=False, default='Rather not say')
    messages = db.Column(db.Integer(), nullable=False, default=0)
    # items = db.relationship('Item', backref='owned_user', lazy=True)
    # relationship is to make it so some items have some relationship to
    # the user.
    shoppingCartCount = db.Column(db.Integer(), nullable=False, default=0)
    profits = db.Column(db.Integer(), nullable=False, default=0)
    spending = db.Column(db.Integer(), nullable=False, default=0)

    # Account status (Adds 'Disabled' or 'Enabled' status column to User Database)
    status = db.Column(db.Integer(), nullable=False, default='Enabled')

    @property
    def prettier_budget(self):
        # to confirm this is to add a , in the budget
        # e.g 1,000 or 100,000
        # this relies on logic alone not special class names
        # affecting this function
        # if len(str(self.budget)) >= 4:
        #     return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        # else:
        return f"${self.budget:,.2f}"

    @property
    def password(self):
        return self.password

    # return password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # hashes the password entered by users creating new accounts

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        # return true or false

    def can_deposit(self, deposit_to_check):
        return deposit_to_check > 0

    def account_availability(self, status):
        if status == "Disabled":
            return 0

    # Password Reset Function
    def password_otp(self, size=8, chars=string.ascii_uppercase + string.digits):
        otp = ''.join(random.choice(chars) for _ in range(size))
        return otp

    # Make sure otp cannot be reused again.
    def scramble_otp(self, size=128, chars=string.ascii_uppercase + string.digits):
        otp = ''.join(random.choice(chars) for _ in range(size))
        return otp

class Item:
    def __init__(self, id, name, quantity, description, price, owner, owner_id):
        self.__id = id
        self.__name = name
        self.__quantity = quantity
        self.__description = description
        self.__price = price
        self.__owner = owner
        self.__owner_id = owner_id
        self.__date_purchased = None
        self.__qty_purchased = None
        self.__total_cost = None

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_quantity(self):
        return self.__quantity

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_owner(self):
        return self.__owner

    def get_owner_id(self):
        return self.__owner_id

    def get_date_purchase(self):
        return self.__date_purchased

    def get_qty_purchased(self):
        return self.__qty_purchased

    def get_total_cost(self):
        return self.__total_cost

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = price

    def set_owner(self, owner):
        self.__owner = owner

    def set_owner_id(self, owner_id):
        self.__owner_id = owner_id

    def set_date_purchase(self, date_purchase):
        self.__date_purchased = date_purchase

    def set_qty_purchased(self, qty_purchased):
        self.__qty_purchased = qty_purchased

    def set_total_cost(self, total_cost):
        self.__total_cost = total_cost


# class Item(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(length=30), nullable=False, unique=True)
#     price = db.Column(db.Integer(), nullable=False)
#     barcode = db.Column(db.String(length=12), nullable=False, unique=True)
#     description = db.Column(db.String(length=1024), nullable=False, unique=True)
#     owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return f'Item {self.name}'

class Partners:
    def __init__(self, name, location, email):
        self.__id = None
        self.__name = name
        self.__location = location
        self.__email = email
        self.__date = datetime.now().strftime("%d/%m/%Y")

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_location(self):
        return self.__location

    def get_date_added(self):
        return self.__date

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_location(self, location):
        self.__location = location

    def set_email(self, email):
        self.__email = email

    def set_date(self, date):
        self.__date = date

    def __str__(self):
        return f"ID: {self.get_id()} , Company Name: {self.get_name()}, Loacation: {self.get_location()}, Email:{self.get_date_added()}, Date Added: {self.get_date_added()}"


class Message:
    def __init__(self, id, description):
        self.__id = id
        self.__description = description

    def get_id(self):
        return self.__id

    def get_description(self):
        return self.__description

    def set_id(self, id):
        self.__id = id

    def set_description(self, description):
        self.__description = description


class Notes(Message):
    def __init__(self, id, description, title, time_added, time_updated):
        super().__init__(id, description)
        self.__title = title
        self.__time_added = time_added
        self.__time_updated = time_updated

    def get_title(self):
        return self.__title

    def get_time_added(self):
        return self.__time_added

    def get_time_updated(self):
        return self.__time_updated

    def set_title(self, title):
        self.__title = title

    def set_time_added(self, time_added):
        self.__time_added = time_added

    def set_time_updated(self, time_updated):
        self.__time_updated = time_updated


class Tickets_Response(Message):
    def __init__(self, id, description, title, time_added, owner, status, recipient):
        super().__init__(id, description)
        self.__title = title
        self.__time_added = time_added
        self.__issue_status = status
        self.__owner = owner
        self.__recipient = recipient

    def get_title(self):
        return self.__title

    def get_time_added(self):
        return self.__time_added

    def get_issue_status(self):
        return self.__issue_status

    def get_owner(self):
        return self.__owner

    def get_recipient(self):
        return self.__recipient

    def set_title(self, title):
        self.__title = title

    def set_time_added(self, time_added):
        self.__time_added = time_added

    def set_issue_status(self, issue_status):
        self.__issue_status = issue_status

    def set_owner(self, owner):
        self.__owner = owner

    def set_recipient(self, recipient):
        self.__recipient = recipient


class Logs:
    def __init__(self, id, log_description, date_recorded, time_recorded):
        self.__id = id
        self.__log_description = log_description
        self.__date_recorded = date_recorded
        self.__time_recorded = time_recorded

    def get_id(self):
        return self.__id

    def get_log_description(self):
        return self.__log_description

    def get_date_recorded(self):
        return self.__date_recorded

    def get_time_recorded(self):
        return self.__time_recorded

    def set_id(self, id):
        self.__id = id

    def set_log_description(self, log_description):
        self.__log_description = log_description

    def set_date_recorded(self, date_recorded):
        self.__date_recorded = date_recorded

    def set_time_recorded(self, time_recorded):
        self.__time_recorded = time_recorded


class TransactionLogs(Logs):
    def __init__(self, id, log_description, transaction, time_recorded, date_recorded):
        super().__init__(id, log_description, date_recorded, time_recorded, )
        self.__transaction = transaction

    def get_transaction(self):
        return self.__transaction

    def set_transaction(self, transaction):
        self.__transaction = transaction


class SalesLogs(Logs):
    def __init__(self, id, log_description, transaction, time_recorded, date_recorded):
        super().__init__(id, log_description, time_recorded, date_recorded)
        self.__transaction = transaction

    def get_transaction(self):
        return self.__transaction

    def set_transaction(self, transaction):
        self.__transaction = transaction


# Ming Wei
class Suppliers:

    def __init__(self, id, name, remarks, email, phone_number):
        self.__id = id
        self.__name = name
        self.__remarks = remarks
        self.__email = email
        self.__phone_number = phone_number

    def get_supplier_id(self):
        return self.__id

    def get_supplier_name(self):
        return self.__name

    def get_supplier_remarks(self):
        return self.__remarks

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number

    def set_supplier_id(self, id):
        self.__id = id

    def set_supplier_name(self, name):
        self.__name = name

    def set_supplier_remarks(self, remarks):
        self.__remarks = remarks

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def __str__(self):
        return f"ID: {self.get_supplier_id()} , Supplier Name: {self.get_supplier_name()}"


# Samuel
class Events(Message):
    def __init__(self, id, description, date_added, time_added, title, updated_date, updated_time):
        super().__init__(id, description)
        self.__date_added = date_added
        self.__time_added = time_added
        self.__title = title
        self.__updated_date = updated_date
        self.__updated_time = updated_time

    def get_date_added(self):
        return self.__date_added

    def get_time_added(self):
        return self.__time_added

    def get_title(self):
        return self.__title

    def get_update_date(self):
        return self.__updated_date

    def get_updated_time(self):
        return self.__updated_time

    def set_time_added(self, time_added):
        self.__time_added = time_added

    def set_date_added(self, date_added):
        self.__date_added = date_added

    def set_title(self, title):
        self.__title = title

    def set_updated_date(self, updated_date):
        self.__updated_date = updated_date

    def set_updated_time(self, updated_time):
        self.__updated_time = updated_time


# Daniel

class Tickets(Message):
    def __init__(self, id, description, title, time_added, urgency, owner, owner_id, pending):
        super().__init__(id, description)
        self.__title = title
        self.__time_added = time_added
        self.__pending_status = pending
        self.__urgency = urgency
        self.__owner = owner
        self.__owner_id = owner_id

    def get_title(self):
        return self.__title

    def get_time_added(self):
        return self.__time_added

    def get_pending_status(self):
        return self.__pending_status

    def get_urgency(self):
        return self.__urgency

    def get_owner(self):
        return self.__owner

    def get_owner_id(self):
        return self.__owner_id

    def set_title(self, title):
        self.__title = title

    def set_time_added(self, time_added):
        self.__time_added = time_added

    def set_pending_status(self, pending_status):
        self.__pending_status = pending_status

    def set_urgency(self, urgency):
        self.__urgency = urgency

    def set_owner(self, owner):
        self.__owner = owner

    def set_owner_id(self, owner_id):
        self.__owner_id = owner_id


class Booking(Message):
    def __init__(self, id, description, time_added, time_updated, phone, nric, date, timeslot):
        super().__init__(id, description)
        self.__time_added = time_added
        self.__time_updated = time_updated
        self.__phone = phone
        self.__nric = nric
        self.__date = date
        self.__timeslot = timeslot

    def get_time_added(self):
        return self.__time_added

    def get_time_updated(self):
        return self.__time_updated

    def get_phone(self):
        return self.__phone

    def get_nric(self):
        return self.__nric

    def get_date(self):
        return self.__date

    def get_timeslot(self):
        return self.__timeslot

    def set_time_added(self, time_added):
        self.__time_added = time_added

    def set_time_updated(self, time_updated):
        self.__time_updated = time_updated

    def set_phone(self, phone):
        self.__phone = phone

    def set_nric(self, nric):
        self.__nric = nric

    def set_date(self, date):
        self.__date = date

    def set_timeslot(self, timeslot):
        self.__timeslot = timeslot


class Feedback(Message):
    def __init__(self, id, description, time_added, time_updated, rating, favourite, least_favourite, improvement,
                 title, sender,sender_id):
        super().__init__(id, description)
        self.__time_added = time_added
        self.__time_updated = time_updated
        self.__rating = rating
        self.__favourite = favourite
        self.__least_favourite = least_favourite
        self.__improvement = improvement
        self.__title = title
        self.__sender = sender
        self.__sender_id = sender_id

    def get_time_added(self):
        return self.__time_added

    def get_time_updated(self):
        return self.__time_updated

    def get_rating(self):
        return self.__rating

    def get_favourite(self):
        return self.__favourite

    def get_least_favourite(self):
        return self.__least_favourite

    def get_improvement(self):
        return self.__improvement

    def get_title(self):
        return self.__title

    def get_sender(self):
        return self.__sender

    def get_sender_id(self):
        return self.__sender_id

    def set_time_added(self, time_added):
        self.__time_added = time_added

    def set_time_updated(self, time_updated):
        self.__time_updated = time_updated

    def set_sender(self,sender):
        self.__sender = sender

    def set_sender_id(self,sender_id):
        self.__sender_id = sender_id

    def set_rating(self, rating):
        self.__rating = rating

    def set_favourite(self, favourite):
        self.__favourite = favourite

    def set_least_favourite(self, least_favourite):
        self.__least_favourite = least_favourite

    def set_improvement(self, improvement):
        self.__improvement = improvement

    def set_title(self, title):
        self.__title = title

