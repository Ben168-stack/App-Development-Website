from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, EmailField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange, optional
from website.models import User
from datetime import datetime


class RegisterForm(FlaskForm):
    # The Validator library allows you to create certain functions
    # with specific usernames which lets the flaskform class
    # do certain stuff for you.
    # The flask form will search for all function names
    # starting with the prefix validate and check if there is even a field
    # with that given name. Once everything is checked out
    # flaskform knows it needs to validate that username
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        # if this returns an object
        if user:
            # checks if user is not 'None'
            # so ya if it returns an object it means this is
            # an existing user created before which raises this error
            raise ValidationError('Username already exist! Please try a different username.')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            # check if email_address is not 'None'.
            raise ValidationError("Email Address already exist. Please try a different email address.")

    # User.query.filter_by(username = username_to_check) will return an object
    # .first() is used to access the first object

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    # email_address = StringField(label='Email:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label="Sign in")


class DepositForm(FlaskForm):
    budget = IntegerField(label='Deposit:', validators=[DataRequired(),NumberRange(min=1, max=50000,message='Please deposit and amount between 1 to 50000')])
    submit = SubmitField(label="Confirm Transaction")


class TransferFunds(FlaskForm):
    transfer = IntegerField(label='Transfer:', validators=[DataRequired(), NumberRange(min=1, max=50000,message='Please transfer and amount between 1 to 50000')])
    submit = SubmitField(label="Confirm Transaction")


class CreatePartnerForm(FlaskForm):
    name = StringField(label='Name', validators=[Length(min=1, max=150), DataRequired()])
    location = StringField(label='Location', validators=[Length(min=1, max=150), DataRequired()])
    email = EmailField(label='Email Address:', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Add Partner')

class UpdatePartnerForm(FlaskForm):
    name = StringField(label='Name', validators=[Length(min=1, max=150), DataRequired()])
    location = StringField(label='Location', validators=[Length(min=1, max=150), DataRequired()])
    email = EmailField(label='Email Address:', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Confirm Changes')

class Add_Notes(FlaskForm):
    description = TextAreaField(label='Description', validators=[Length(min=1, max=150), DataRequired()])
    title = StringField(label='Title', validators=[Length(min=1, max=30), DataRequired()])
    submit = SubmitField(label='Add Notes')

class Update_Notes(FlaskForm):
    description = TextAreaField(label='Description', validators=[Length(min=1, max=150), DataRequired()])
    title = StringField(label='Title', validators=[Length(min=1, max=30), DataRequired()])
    submit = SubmitField(label='Update Notes')