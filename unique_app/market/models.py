from market import db
from market import app

class Item(db.Model):
    id = db.Column(db.Integer() , primary_key=True)
    name = db.Column(db.String(length=30) , nullable=False , unique=True)
    price = db.Column(db.Integer() , nullable=False)
    barcode = db.Column(db.String(length=12) , nullable=False , unique=True)
    description = db.Column(db.String(length=1024) , nullable=False , unique=True)
    image = db.Column(db.String(length=1024) , nullable=False , unique=True)



with app.app_context():
    db.create_all()