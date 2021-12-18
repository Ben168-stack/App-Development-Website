from flask_login import UserMixin
from website import bcrypt
from website import db, login_manager
from datetime import datetime
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
    gender = db.Column(db.String(),nullable=False,default = 'rather not say')
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

    def can_deposit(self,deposit_to_check):
        return deposit_to_check > 0

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
    def __init__(self,name,location,email):
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

    def set_id(self,id):
        self.__id = id

    def set_name(self,name):
        self.__name = name

    def set_location(self,location):
        self.__location = location
    def set_email(self,email):
        self.__email = email
    def set_date(self,date):
        self.__date = date

    def __str__(self):
        return f"ID: {self.get_id()} , Company Name: {self.get_name()}, Loacation: {self.get_location()}, Email:{self.get_date_added()}, Date Added: {self.get_date_added()}"

class Message:
    def __init__(self,id,description):
        self.__id = id
        self.__description = description

    def get_id(self):
        return self.__id

    def get_description(self):
        return self.__description

    def set_id(self,id):
        self.__id = id

    def set_description(self,description):
        self.__description = description

class Notes(Message):
    def __init__(self,id,description,title,time_added,time_updated):
        super().__init__(id,description)
        self.__title = title
        self.__time_added = time_added
        self.__time_updated = time_updated

    def get_title(self):
        return self.__title
    def get_time_added(self):
        return self.__time_added
    def get_time_updated(self):
        return self.__time_updated
    def set_title(self,title):
        self.__title = title
    def set_time_added(self,time_added):
        self.__time_added = time_added
    def set_time_updated(self, time_updated):
        self.__time_updated = time_updated

# Ming Wei
class Suppliers:
    def __init__(self,name):
        self.__id = None
        self.__name = name

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_id(self,id):
        self.__id = id

    def set_name(self,name):
        self.__name = name

    def __str__(self):
        return f"ID: {self.get_id()} , Supplier Name: {self.get_name()}"

# Samuel
class Item:
    def __init__(self,name):
        self.__name = name
        self.id = None

    def get_name(self):
        return self.__name

    def set_name(self,name):
        self.__name = name

# Daniel
class Booking(Message):
    def __init__(self,id,description,title,time_added,time_updated):
        super().__init__(id,description)
        self.__title = title
        self.__time_added = time_added
        self.__time_updated = time_updated

    def get_title(self):
        return self.__title
    def get_time_added(self):
        return self.__time_added
    def get_time_updated(self):
        return self.__time_updated
    def set_title(self,title):
        self.__title = title
    def set_time_added(self,time_added):
        self.__time_added = time_added
    def set_time_updated(self, time_updated):
        self.__time_updated = time_updated

















