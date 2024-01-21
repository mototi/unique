import json
import random
from flask import request
from market import app , db , photos , userphotos
from flask import render_template , redirect , url_for 
from market.models import Item , User
from market.forms import EditItemForm, ExtendedItemForm, ItemForm, RegisterForm , LoginForm
from flask_login import current_user, login_user , logout_user , login_required 
from functools import wraps


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('sell_as_customer'))
    return wrapper


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    items = Item.query.filter_by(market=True)
    role = "admin"
    user_items = None
    pendings = []
    approved_items = []

    file = open('./market/customer_requests.json', 'r')
    temp = json.load(file)
    file.close() 

    # get all items that has the same owner_id as the current_user.id if the current_user is not admin and market = False
    if current_user.role != 'admin':
        user_items = Item.query.filter_by(owner_id=current_user.id , market=False)
        role = "customer" 
    else:
        for i in temp:
            if i['approved'] == "false":
                pendings.append(i)
    
    for i in temp:
        if i['approved'] == "true":
            approved_items.append(i)
                

    return render_template('market.html' , items=items , user_items=user_items , role=role , pendings=pendings , approved_items=approved_items)


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
@login_required
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
                    errors.append(form.errors[err_msg][0])

    return render_template('sell.html' , form=form , errors=errors , alert=alert)

@app.route('/sell/customer' , methods=['GET' , 'POST'])
@login_required 
def sell_as_customer():
    form = ExtendedItemForm()
    errors = []
    alert = None

    if request.method == 'POST':
        form.barcode.data = random.randint(10000000 , 99999999)
        if form.validate_on_submit():

            user_request = {
                'username': current_user.username,
                'user_id': current_user.id,
                'name': form.name.data,
                'price': form.price.data,
                'description': form.description.data,
                'image': form.image.data.filename,
                'barcode': form.barcode.data,
                'phone_number': form.phone_number.data,
                'approved': "false"
            }
            
            file = open('./market/customer_requests.json', 'r')
            content = json.load(file)
            file.close()

            #append user_request and then write it to the file
            content.append(user_request)
            file = open('./market/customer_requests.json', 'w')
            json.dump(content, file)
            file.close()        

            userphotos.save(form.image.data)

            alert = f'we will reach you as soon as possible!'
       
        if form.errors != {}:
            for err_msg in form.errors:
                    errors.append(form.errors[err_msg][0])


    return render_template('sell_customer.html' , form=form , errors=errors , alert=alert)


#show customer item by id
@app.route('/customer-item/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
@admin_required
def customer_item_page(barcode):
    item = None
    if barcode:
            file = open('./market/customer_requests.json', 'r')
            content = json.load(file)
            file.close()
            for i in content:
                if i['barcode'] == barcode:
                    item = i
                    break
            if item == None:
                return render_template('notfount.html')
            user = User.query.filter_by(id=item['user_id']).first()
    return render_template('customer_item.html' , item=item , user=user)

@app.route('/item/<int:barcode>' , methods=['GET'])
@login_required
def item_page(barcode):
    item = None
    if barcode:
            item = Item.query.filter_by(barcode=barcode).first()
            if item == None:
                return render_template('notfount.html')
    return render_template('item.html' , item=item)

@app.route('/item-deleted/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
@admin_required
def delete_item(barcode):
    item = None
    if barcode:
            #delete item from database
            item = Item.query.filter_by(barcode=barcode).first()
            db.session.delete(item)
            db.session.commit()
            if item == None:
                return render_template('notfount.html')
            user = User.query.filter_by(id=item.owner_id).first()
            if user.role == 'customer':
                user.budget += item.price
                db.session.commit()
    return redirect(url_for('market_page'))


@app.route('/item-sold/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
def item_sold(barcode):
    item = None
    if barcode:
            #delete item from database
            item = Item.query.filter_by(barcode=barcode).first()
            user = User.query.filter_by(id=current_user.id).first()
            if user.can_purchase(item):
                item.buy(user)
            else:
                return render_template('recharge.html')
            if item == None:
                return render_template('notfount.html')
    return redirect(url_for('market_page'))

@app.route('/item-bought/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
def item_bought(barcode):
    item = None
    if barcode:
            #delete item from database
            item = Item.query.filter_by(barcode=barcode).first()
            user = User.query.filter_by(id=current_user.id).first()
            if user.can_sell(item):
                if user.budget < 10:
                    return render_template('recharge.html')
                item.sell(user)
            else:
                return render_template('error.html')
            if item == None:
                return render_template('notfount.html')
    return redirect(url_for('market_page'))


#route to change only the price of item
@app.route('/item-edit/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
def edit_item(barcode):
    item = None
    form = EditItemForm()
    errors = []
    if request.method == 'POST':
        if barcode:
            item = Item.query.filter_by(barcode=barcode).first()
            if form.validate_on_submit():
                item.price = form.price.data
                db.session.commit()
                return redirect(url_for('market_page'))
            else:
                for err_msg in form.errors:
                    errors.append(form.errors[err_msg][0])
    
    return render_template('edit_item.html' , form=form , errors=errors)


@app.route('/recharge' , methods=['GET' , 'POST'])
@login_required
def recharge_page():
    return render_template('recharge.html')

@app.route('/change-pendding/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
@admin_required
def change_pendding(barcode):
    item = None
    if barcode:
            file = open('./market/customer_requests.json', 'r')
            content = json.load(file)
            file.close()

            #if the barcode found change the approved to true and rewite the file
            for i in content:
                if i['barcode'] == barcode:
                    i['approved'] = "true"
                    item = i
                    file = open('./market/customer_requests.json', 'w')
                    json.dump(content, file)
                    file.close()
                    break

            if item == None:
                return render_template('notfount.html')
    return redirect(url_for('market_page'))


@app.route('/user/<int:user_id>' , methods=['GET'])
@login_required
def user_info(user_id):
    user = None
    if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user == None:
                return render_template('notfount.html')
    return render_template('user.html' , user=user)
