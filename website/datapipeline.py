from website import app, bcrypt
from flask import render_template, request, flash, redirect, url_for
from website.models import User, Partners, Notes, Tickets, Tickets_Response, Item, Booking, Feedback, Events
from website.forms import RegisterForm, LoginForm, DepositForm, TransferFunds, CreatePartnerForm, UpdatePartnerForm, \
    Add_Notes, Update_Notes, Update_User, Update_Username, Update_Email, Update_Gender, Update_Password, Ticket_Form, \
    Ticket_Reply_Form, UpdateSupplierForm, Add_Item_Form, Purchase_Form, Wish_Form, Update_User_Admin, Booking_form, \
    Restock_Item_Form, Add_To_Cart_Form, Feedback_form, Add_Event, Edit_Cart
from website import db
from flask_login import login_user, logout_user, login_required, current_user
from website import admin_user
import shelve
from datetime import datetime
from uuid import uuid4  # Unique key generator


@app.route('/formatDate')
def formatDate():
    Owned_Items_Dict = {}
    try:
        Owned_Items_Database = shelve.open('website/databases/Owned_Items/ownedItems.db', 'c')

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

    for i in Owned_Items_Dict


    return Owned_Items_Dict
