import random
from flask import request
from market import app , db , photos
from flask import render_template , redirect , url_for 
from market.models import Item , User
from market.forms import ItemForm, RegisterForm , LoginForm
from flask_login import current_user, login_user , logout_user , login_required 
from functools import wraps


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('be_admin_page'))
    return wrapper


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    role = "admin"
    user_items = None
    # get all items that has the same owner_id as the current_user.id if the current_user is not admin
    if current_user.role != 'admin':
        user_items = Item.query.filter_by(owner_id=current_user.id)
        role = "customer"   

    return render_template('market.html' , items=items , user_items=user_items , role=role)


@app.route('/register' , methods=['GET' , 'POST']) 
def register_page():
    form = RegisterForm()
    errors = []
    if request.method == 'POST':
        if form.validate_on_submit():
            user_to_create = User(username=form.username.data , 
                                  email_address=form.email_address.data , 
                                  password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            return redirect(url_for('market_page'))
        if form.errors != {}:
            for err_msg in form.errors:
                if err_msg == 'username':
                    errors.append('Username already exists!')
                elif err_msg == 'email_address':
                    errors.append('Email already exists!')
                elif err_msg == 'password1':
                    errors.append('Password must be at least 6 characters!')
                elif err_msg == 'password2':
                    errors.append('Passwords must match!')

    return render_template('register.html' , form=form , errors=errors)


@app.route('/login' , methods=['GET' , 'POST'])
def login_page():
    form = LoginForm()
    errors = [] 
    if request.method == 'POST':
        if form.validate_on_submit():
            attempted_email_address = form.email_address.data
            attempted_password = form.password.data
            user = User.query.filter_by(email_address=attempted_email_address).first()
            if user and user.check_password_correction(attempted_password):
                login_user(user)
                return redirect(url_for('market_page'))
            else:
                errors.append('Email or Password are not correct!')

    return render_template('login.html' , form=form , errors=errors)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/sell' , methods=['GET' , 'POST'])
@admin_required 
def sell_page():
    form = ItemForm()
    errors = []
    alert = None

    if request.method == 'POST':
        form.barcode.data = random.randint(10000000 , 99999999)
        if form.validate_on_submit():

            item_to_create = Item(name=form.name.data , 
                                  price=form.price.data , 
                                  barcode=form.barcode.data , 
                                  description=form.description.data , 
                                  image=form.image.data.filename,
                                  owner_id=current_user.id)

            db.session.add(item_to_create)
            db.session.commit()

            photos.save(form.image.data)

            alert = f'Congratulations! You have added {form.name.data} to the market!'
       
        if form.errors != {}:
            for err_msg in form.errors:
                if err_msg == 'name':
                    errors.append('Name already exists!')
                elif err_msg == 'price':
                    errors.append('Price must be a number!')
                elif err_msg == 'barcode':
                    errors.append('something wrong please try again!')
                elif err_msg == 'description':
                    errors.append('Description already exists try to change it!')
                elif err_msg == 'image':
                    errors.append('you are trying to uplaod NON_IMAGE file, change it, and try again!')

    return render_template('sell.html' , form=form , errors=errors , alert=alert)

@app.route('/beADMIN' , methods=['GET' , 'POST']) 
def be_admin_page():
    return render_template('adminForm.html')