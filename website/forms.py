from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, EmailField, TextAreaField, \
    SelectField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from website.models import User


# from datetime import datetime

# Benjamin
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
    budget = IntegerField(label='Deposit:', validators=[DataRequired(), NumberRange(min=1, max=50000,
                                                                                    message='Please deposit and amount between 1 to 50000')])
    submit = SubmitField(label="Confirm Transaction")


class TransferFunds(FlaskForm):
    transfer = IntegerField(label='Transfer:', validators=[DataRequired(), NumberRange(min=1, max=50000,
                                                                                       message='Please transfer and amount between 1 to 50000')])
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


class Update_User(FlaskForm):
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

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    gender = SelectField(label='Gender', choices=['Male', 'Female', "Rather not say"], validators=[DataRequired()])
    submit = SubmitField(label='Create Account')


class Update_Username(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        # if this returns an object
        if user:
            # checks if user is not 'None'
            # so ya if it returns an object it means this is
            # an existing user created before which raises this error
            raise ValidationError('Username already exist! Please try a different username.')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    submit = SubmitField(label='Done')


class Update_Email(FlaskForm):
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            # check if email_address is not 'None'.
            raise ValidationError("Email Address already exist. Please try a different email address.")

    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Done')


class Update_Gender(FlaskForm):
    gender = SelectField(label='Gender', choices=['Male', 'Female', "Rather not say"], validators=[DataRequired()])
    submit = SubmitField(label='Done')


class Update_Password(FlaskForm):
    current_password = PasswordField(label='Current Password:', validators=[Length(min=6), DataRequired()])
    new_password = PasswordField(label='New Password:', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Done')


class Ticket_Reply_Form(FlaskForm):
    description = TextAreaField(label='Description', validators=[Length(min=1, max=150), DataRequired()])
    title = StringField(label='Title', validators=[Length(min=1, max=30), DataRequired()])
    issue_status = SelectField(label='Issue Status', choices=['Resolved', 'Unresolved'], validators=[DataRequired()])
    submit = SubmitField(label='Send Ticket')


class Add_To_Cart_Form(FlaskForm):
    quantity = IntegerField(label="Quantity To Add", validators=[NumberRange(min=1), DataRequired()])
    submit = SubmitField(label='Add to Cart')


class Purchase_Form(FlaskForm):
    quantity = IntegerField(label="Quantity To Add", validators=[NumberRange(min=1), DataRequired()])
    submit = SubmitField(label='Add to Cart')


class Edit_Cart(FlaskForm):
    quantity = IntegerField(label="Edit Quantity", validators=[NumberRange(min=1), DataRequired()])
    submit = SubmitField(label='Edit Cart')


class Wish_Form(FlaskForm):
    submit = SubmitField(label='Wish')


# Daniel
class Ticket_Form(FlaskForm):
    description = TextAreaField(label='Description', validators=[Length(min=1, max=150), DataRequired()])
    title = StringField(label='Title', validators=[Length(min=1, max=30), DataRequired()])
    urgency = SelectField(label='Urgency', choices=['Very Urgent', 'Urgent', 'Slightly Urgent'],
                          validators=[DataRequired()])
    submit = SubmitField(label='Send Ticket')


class Booking_form(FlaskForm):
    date = DateField(label='Choose a Date*', validators=[DataRequired()])
    time = SelectField(label='Choose a Timeslot*',
                       choices=['9am Morning', '10am Morning', '11am Morning', '12pm Afternoon', '1pm Afternoon',
                                '2pm Afternoon',
                                '3pm Afternoon', '4pm Afternoon', '5pm Afternoon'], validators=[DataRequired()])
    reason = TextAreaField(label='Additional Comments', validators=[Length(min=1, max=150), DataRequired()])
    submit = SubmitField(label='Confirm Booking')


class Feedback_form(FlaskForm):
    title = StringField("Title: ", validators=[Length(min=1, max=30), DataRequired()])
    description = TextAreaField(label='Additional Comments', validators=[Length(min=1, max=150), DataRequired()])
    improvement = TextAreaField("How else can we improve", [Length(min=1, max=30), DataRequired()])
    favourite = StringField("Favourite thing", [Length(min=1, max=50), DataRequired()])
    least_favourite = StringField("Least favourite thing", [Length(min=1, max=50), DataRequired()])
    submit = SubmitField(label='Send Feedback')


# Inheritance from Purchase_Form Class
class Restock_Item_Form(Purchase_Form):
    quantity = IntegerField(label="Quantity To Add", validators=[NumberRange(min=1), DataRequired()])
    submit = SubmitField(label='Add to Cart')


# Ming Wei
class CreateSupplierForm(FlaskForm):
    company = StringField(label='Company:', validators=[Length(min=1, max=99), DataRequired()])
    remarks = StringField(label='Remarks:', validators=[Length(min=1, max=150), DataRequired()])
    phone = StringField(label='Phone Number:', validators=[Length(min=1, max=150), DataRequired()])
    email = EmailField(label='Email Address:', validators=[Email(), Length(min=1, max=150), DataRequired()])
    submit = SubmitField(label='Create Supplier')


class UpdateSupplierForm(FlaskForm):
    company = StringField(label='Company:', validators=[Length(min=1, max=99), DataRequired()])
    remarks = StringField(label='Remarks:', validators=[Length(min=1, max=150), DataRequired()])
    phone = StringField(label='Phone Number:', validators=[Length(min=1, max=150), DataRequired()])
    email = EmailField(label='Email Address:', validators=[Email(), Length(min=1, max=150), DataRequired()])
    submit = SubmitField(label='Update Supplier')


# Polymorphism + inheritance
class Update_User_Admin(Update_User):
    def username_update_admin(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        # if this returns an object
        if user:
            # checks if user is not 'None'
            # so ya if it returns an object it means this is
            # an existing user created before which raises this error
            raise ValidationError('Username already exist! Please try a different username.')

    def email_address_update_admin(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            # check if email_address is not 'None'.
            raise ValidationError("Email Address already exist. Please try a different email address.")


class password_reset(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    otp = StringField(label='One time password:', validators=[Length(min=8, max=8), DataRequired()])
    submit = SubmitField(label='Submit password reset')
    new_password = PasswordField(label='New Password:', validators=[Length(min=6), DataRequired()])


# Samuel
class Add_Event(FlaskForm):
    description = TextAreaField(label='Description', validators=[Length(min=1, max=150), DataRequired()])
    title = StringField(label='Title', validators=[Length(min=1, max=30), DataRequired()])
    submit = SubmitField(label='Add Event')


class Add_Item_Form(FlaskForm):
    name = StringField(label='Name', validators=[Length(min=1, max=100), DataRequired()])
    quantity = IntegerField(label='Quantity', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField(label='Description', validators=[DataRequired(), Length(min=1, max=1000)])
    price = FloatField(label='Price', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField(label='Add Item')
