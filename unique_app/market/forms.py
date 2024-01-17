from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo , Length , Email , ValidationError
from market.models import User


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
    name = StringField('Name' , validators=[DataRequired()])
    price = IntegerField('Price' , validators=[DataRequired()])
    barcode = StringField('Barcode' , validators=[DataRequired()])
    description = StringField('Description' , validators=[DataRequired()])
    image = FileField('Image' , validators=[DataRequired()])
    submit = SubmitField('Sell Now')