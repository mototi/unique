from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, PasswordField, SubmitField, IntegerField, TextAreaField 
from wtforms.validators import DataRequired, EqualTo , Length , Email , ValidationError
from market.models import User , Item
from market import photos


class RegisterForm(FlaskForm):

    def validate_username(self , username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!')
    
    def validate_email_address(self , email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email already exists!')

    username = StringField('Username', validators=[DataRequired() , Length(min=2 , max=30)])
    email_address = StringField('Email', validators=[DataRequired() , Email()])
    password1 = PasswordField('Password', validators=[DataRequired() , Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('password1')])
    submit = SubmitField('Sign Up')


class LoginForm (FlaskForm):
    email_address = StringField('Email' , validators=[DataRequired()])
    password = PasswordField('Password' , validators=[DataRequired()])
    submit = SubmitField('Log in')


class ItemForm (FlaskForm):

    def validate_name(self , name_to_check):
        name_to_check.data = name_to_check.data.strip()
        item = Item.query.filter_by(name=name_to_check.data).first()
        if item:
            raise ValidationError('the name of item already exists! change another name')
        
    def validate_barcode(self , barcode_to_check):
        item = Item.query.filter_by(barcode=barcode_to_check.data).first()
        if item:
            raise ValidationError('the barcode of item already exists! change another barcode')
    
    def validate_image(self , image_to_check):
        filename = image_to_check.data.filename
        item = Item.query.filter_by(image=filename).first()
        if item:
            raise ValidationError('the image of item already exists! change file name')
        
    def validate_description(self , description_to_check):
        description_to_check.data = description_to_check.data.strip()
        item = Item.query.filter_by(description=description_to_check.data).first()
        if item:
            raise ValidationError('the description of item already exists! change another description')
        
    
    name = StringField('Name' , validators=[DataRequired()])
    price = IntegerField('Price' , validators=[DataRequired()])
    barcode = StringField('Barcode' , validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image' , validators=[DataRequired() , FileAllowed(photos , message='Only images are allowed')])
    submit = SubmitField('Sell Now')


    
class ExtendedItemForm(ItemForm):
   phone_number = StringField('Phone', validators=[DataRequired()])
    