import json
import random
from flask import request
from market import app , db , photos , userphotos
from flask import render_template , redirect , url_for 
from market.models import Item , User
from market.forms import EditItemForm, ExtendedItemForm, ItemForm, RegisterForm , LoginForm
from flask_login import current_user, login_user , logout_user , login_required 
from functools import wraps

#middleware to check if the user is admin
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return func(*args, **kwargs)
        else:
            #if the user is not admin redirect him to sell_as_customer page (different form for customer)
            return redirect(url_for('sell_as_customer'))
    return wrapper


# display welcome message and get started to redirect user to market page or login page if he is not logged in
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# display market page with all items that has market = True in unique section 
# for admins display all pending items in pending section 
# for admins and customers display all approved items in fans section
# for customers display all items that has the same owner_id as the current_user.id in my items
# login is required to access this page
@app.route('/market')
@login_required
def market_page():
    items = Item.query.filter_by(market=True)
    role = "admin"
    user_items = None
    pendings = []
    approved_items = []

    # get all items from pending items json file
    file = open('./market/customer_requests.json', 'r')
    temp = json.load(file)
    file.close() 

    # get all items that has the same owner_id as the current_user.id if the current_user is not admin and market = False
    if current_user.role != 'admin':
        user_items = Item.query.filter_by(owner_id=current_user.id , market=False)
        role = "customer" 
    else:
        # get all items from pendding file that has approved = false (still pending)
        for i in temp:
            if i['approved'] == "false":
                pendings.append(i)
    
    # get all items from pendding file that has approved = true (approved - displyed in fans section)
    for i in temp:
        if i['approved'] == "true":
            approved_items.append(i)
                

    return render_template('market.html' , items=items , user_items=user_items , role=role , pendings=pendings , approved_items=approved_items)


@app.route('/register' , methods=['GET' , 'POST']) 
def register_page():
    form = RegisterForm()
    # list to save all validation errors
    errors = []
    if request.method == 'POST':
        # validate user inputs
        if form.validate_on_submit():
            user_to_create = User(username=form.username.data , 
                                  email_address=form.email_address.data , 
                                  password=form.password1.data,
                                  phone=form.phone.data)
            db.session.add(user_to_create)
            db.session.commit()
            # save user credentials in session
            login_user(user_to_create)
            return redirect(url_for('market_page'))
        # if the form is not valid get all errors and save them in errors list
        if form.errors != {}:
            for err_msg in form.errors:
                errors.append(form.errors[err_msg][0])

    return render_template('register.html' , form=form , errors=errors)


@app.route('/login' , methods=['GET' , 'POST'])
def login_page():
    form = LoginForm()
    errors = [] 
    if request.method == 'POST':
        # validate user inputs
        if form.validate_on_submit():
            attempted_email_address = form.email_address.data
            attempted_password = form.password.data
            # check if the user is exist in users table and the password is correct
            user = User.query.filter_by(email_address=attempted_email_address).first()
            if user and user.check_password_correction(attempted_password):
                # save user credentials in session
                login_user(user)
                return redirect(url_for('market_page'))
            else:
                errors.append('Email or Password are not correct!')

    return render_template('login.html' , form=form , errors=errors)


@app.route('/logout')
@login_required
def logout_page():
    # remove user credentials from session
    logout_user()
    return redirect(url_for('home_page'))

# sell form page for admins
@app.route('/sell' , methods=['GET' , 'POST'])
@login_required
# if the user is not an admin redirect him to sell_as_customer page (different form for customer)
@admin_required 
def sell_page():
    form = ItemForm()
    # list to save all validation errors
    errors = []
    # alert to show success message
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

            # save image added by admin in resources folder
            photos.save(form.image.data)

            alert = f'Congratulations! You have added {form.name.data} to the market!'
       
        if form.errors != {}:
            for err_msg in form.errors:
                    errors.append(form.errors[err_msg][0])

    return render_template('sell.html' , form=form , errors=errors , alert=alert)


# sell form page for customers
@app.route('/sell/customer' , methods=['GET' , 'POST'])
@login_required 
def sell_as_customer():
    form = ExtendedItemForm()
    errors = []
    # alert to show success message
    alert = None

    if request.method == 'POST':
        form.barcode.data = random.randint(10000000 , 99999999)
        # validate user inputs
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
            
            #open json file and get all pendding items
            file = open('./market/customer_requests.json', 'r')
            content = json.load(file)
            file.close()

            #append user_request and then write it to the file
            content.append(user_request)
            file = open('./market/customer_requests.json', 'w')
            json.dump(content, file)
            file.close()        

            # save the image that user added in userresources folder
            userphotos.save(form.image.data)

            alert = f'we will reach you as soon as possible!'
       
        if form.errors != {}:
            for err_msg in form.errors:
                    errors.append(form.errors[err_msg][0])


    return render_template('sell_customer.html' , form=form , errors=errors , alert=alert)


#show pendding items by id from json file only admins can access this page as it is still not approved to be in fans section
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
            # get the user who added the item and send it the the html page to show his details
            user = User.query.filter_by(id=item['user_id']).first()
    return render_template('customer_item.html' , item=item , user=user)

#show items by id that is available in market
@app.route('/item/<int:barcode>' , methods=['GET'])
@login_required
def item_page(barcode):
    item = None
    if barcode:
            item = Item.query.filter_by(barcode=barcode).first()
            if item == None:
                return render_template('notfount.html')
    return render_template('item.html' , item=item)


#route to delete item from market
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
            # get the user who added the item
            user = User.query.filter_by(id=item.owner_id).first()
            # check if the user is customer and send the price back to his budget when deleting item from market
            if user.role == 'customer':
                user.budget += item.price
                db.session.commit()
    return redirect(url_for('market_page'))


#route to delete item from market as customer (not admin) buy it and has enough budget
@app.route('/item-sold/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
def item_sold(barcode):
    item = None
    if barcode:
            item = Item.query.filter_by(barcode=barcode).first()
            user = User.query.filter_by(id=current_user.id).first()
            # check if the user is customer and has enough budget to buy the item if not redirect him to recharge page
            if user.can_purchase(item):
                item.buy(user)
            else:
                return render_template('recharge.html')
            if item == None:
                return render_template('notfount.html')
    return redirect(url_for('market_page'))

#route to allow customers to resell items that they bought from market (and only from market)
@app.route('/item-bought/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
def item_bought(barcode):
    item = None
    if barcode:
            item = Item.query.filter_by(barcode=barcode).first()
            user = User.query.filter_by(id=current_user.id).first()
            # check if the user is customer and has the item in his items if not redirect him to error page
            if user.can_sell(item):
                # check if the user is customer and has at least 10 budget (selling fees) to sell the item if not redirect him to recharge page
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

# route displays recharge form to allow users to recharge their budget
# in future work a paymentmethod will be added to allow users to recharge their budget but for now its just dummy form
@app.route('/recharge' , methods=['GET' , 'POST'])
@login_required
def recharge_page():
    return render_template('recharge.html')

#route to remove items that has pen added by users and displayed in pendding section and add them in fans section
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


#route to show user details by id
@app.route('/user/<int:user_id>' , methods=['GET'])
@login_required
def user_info(user_id):
    user = None
    # warning to be displayed if customers seeked contact with other customers
    warning1 = None
    warning2 = None
    warning3 = None
    if user_id:
            # check if the user approaching this profile page is the owner of this profile or not
            if current_user.id != user_id:
                warning1 = "Note : the app are not responsible for items displayed in fans section"
                warning2 = "don't transfare money to unverified users"
                warning3 = "you may need to examine the physical item before transferring any dollar"
            user = User.query.filter_by(id=user_id).first()
            if user == None:
                return render_template('notfount.html')
    return render_template('user.html' , user=user , warning1=warning1 , warning2=warning2 , warning3=warning3)

#delete from json file with barcode
@app.route('/delete-pendding/<int:barcode>' , methods=['GET' , 'POST'])
@login_required
@admin_required
def delete_pendding(barcode):
    item = None
    if barcode:
            file = open('./market/customer_requests.json', 'r')
            content = json.load(file)
            file.close()

            #if the barcode found delete it and rewite the file
            for i in content:
                if i['barcode'] == barcode:
                    item = i
                    content.remove(i)
                    file = open('./market/customer_requests.json', 'w')
                    json.dump(content, file)
                    file.close()
                    break

            if item == None:
                return render_template('notfount.html')
    return redirect(url_for('market_page'))

#route to show items details from json file
@app.route('/item-fan-section/<int:barcode>' , methods=['GET'])
@login_required
def item_fan_details(barcode):
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
    return render_template('customer_item_details.html' , item=item)

#dummy route to mock payment method that should be applied in future work
@app.route('/add-coins' , methods=['POST'])
@login_required
def add_coins():
    amount = request.form.get('coins')
    if amount:
        current_user.budget += int(amount)
        db.session.commit()
    return redirect(url_for('recharge_page'))