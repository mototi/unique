from curses import flash
from flask import request
from market import app , db 
from flask import render_template , redirect , url_for 
from market.models import Item , User
from market.forms import RegisterForm , LoginForm
from flask_login import login_user , logout_user 




@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items =  Item.query.all()
    return render_template('market.html' , items=items)


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
def logout_page():
    logout_user()
    flash('You have been logged out!' , category='info')
    return redirect(url_for('home_page'))