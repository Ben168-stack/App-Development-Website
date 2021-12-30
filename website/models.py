from flask_login import UserMixin
from website import bcrypt
from website import db, login_manager
from datetime import datetime
from uuid import uuid4
import shelve
from sqlalchemy import func


# Benjamin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

    @property
    def prettier_budget(self):
        # to confirm this is to add a , in the budget
        # e.g 1,000 or 100,000
        # this relies on logic alone not special class names
        # affecting this function
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f"${self.budget}"

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


class Item:
    def __init__(self,id,name,quantity,description,price,owner,owner_id):
        self.__id = id
        self.__name = name
        self.__quantity = quantity
        self.__description = description
        self.__price = price
        self.__owner = owner
        self.__owner_id = owner_id

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

    def set_id(self,id):
        self.__id = id

    def set_name(self,name):
        self.__name = name

    def set_quantity(self,quantity):
        self.__quantity = quantity

    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = price

    def set_owner(self, owner):
        self.__owner = owner

    def set_owner_id(self,owner_id):
        self.__owner_id = owner_id


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


class Tickets(Message):
    def __init__(self, id, description, title, time_added, urgency, owner,owner_id, pending):
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

    def set_owner_id(self,owner_id):
        self.__owner_id = owner_id


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



# Daniel
class Booking(Message):
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
