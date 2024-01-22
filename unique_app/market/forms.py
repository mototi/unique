from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, PasswordField, SubmitField, IntegerField, TextAreaField 
from wtforms.validators import DataRequired, EqualTo , Length , Email , ValidationError
from market.models import User , Item
from market import photos


# forms.py is used to create forms for the user to fill in
# we use flask_wtf to create forms
# we use wtforms to create fields in the form
# we use validators to validate the data entered by the user
# we create a class for each form



class RegisterForm(FlaskForm):

    #check if username already exists in DB and raise error if it exists
    def validate_username(self , username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!')
    #check if email already exists in DB and raise error if it exists
    def validate_email_address(self , email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email already exists!')
    
    #check if phone already exists in DB and raise error if it exists
    def validate_phone(self , phone_to_check):
        phone = User.query.filter_by(phone=phone_to_check.data).first()
        if phone:
            raise ValidationError('Phone already matches with existing user!')

    username = StringField('Username', validators=[DataRequired() , Length(min=2 , max=30)])
    email_address = StringField('Email', validators=[DataRequired() , Email()])
    password1 = PasswordField('Password', validators=[DataRequired() , Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('password1')])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm (FlaskForm):
    email_address = StringField('Email' , validators=[DataRequired()])
    password = PasswordField('Password' , validators=[DataRequired()])
    submit = SubmitField('Log in')


# ItemForm is used to create a form for admin to fill in when he wants to sell an item
class ItemForm (FlaskForm):

    #check if item's name already exists in DB and raise error if it exists
    def validate_name(self , name_to_check):
        name_to_check.data = name_to_check.data.strip()
        item = Item.query.filter_by(name=name_to_check.data).first()
        if item:
            raise ValidationError('the name of item already exists! change another name')
    
    #check if item's barcode already exists in DB and raise error if it exists
    def validate_barcode(self , barcode_to_check):
        item = Item.query.filter_by(barcode=barcode_to_check.data).first()
        if item:
            raise ValidationError('the barcode of item already exists! change another barcode')
    
    #check if item's image filename already exists in DB and raise error if it exists
    def validate_image(self , image_to_check):
        filename = image_to_check.data.filename
        item = Item.query.filter_by(image=filename).first()
        if item:
            raise ValidationError('the image of item already exists! change file name')
    
    #check if item's description already exists in DB and raise error if it exists
    def validate_description(self , description_to_check):
        description_to_check.data = description_to_check.data.strip()
        item = Item.query.filter_by(description=description_to_check.data).first()
        if item:
            raise ValidationError('the description of item already exists! change another description')

    #check if item's price is greater than 1000 and raise error if it is less than 1000
    def validate_price(self , price_to_check):
        if price_to_check.data < 999:
            raise ValidationError('price must be greater than or equals 1000')    
    
    name = StringField('Name' , validators=[DataRequired() , Length(min=2 , max=30)])
    price = IntegerField('Price' , validators=[DataRequired()])
    barcode = StringField('Barcode' , validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image' , validators=[DataRequired() , FileAllowed(photos , message='Only images are allowed')])
    submit = SubmitField('Sell Now')


# ExtendedItemForm is used to create a form for customer to fill in when he rquests to sell an item
class ExtendedItemForm(ItemForm):
   phone_number = StringField('Phone', validators=[DataRequired()])


# EditItemForm is used by customer when he wants to edit itm's price 
class EditItemForm(FlaskForm):
    price = IntegerField('Price' , validators=[DataRequired()])
    submit = SubmitField('Edit Now')

    #check if item's price is greater than 1000 and raise error if it is less than 1000
    def validate_price(self , price_to_check):
        if price_to_check.data < 999:
            raise ValidationError('price must be greater than or equals 1000')
    