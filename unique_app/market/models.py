from market import db
from market import bcrypt
from market import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer, nullable=False, default=1000)
    role = db.Column(db.String(length=20), nullable=False, default='cutomer')
    items = db.relationship('Item', backref='owner', lazy=True)

    def __init__(self , username , email_address , password):
        self.username = username
        self.email_address = email_address
        self.password = password

    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
        return item_obj in self.items
    


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    image = db.Column(db.String(length=1024), nullable=False , unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def buy(self, user):
        self.owner = user
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
    

    
