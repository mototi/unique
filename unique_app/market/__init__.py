import flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '39960418812650df760f359a'
app.config['UPLOADED_PHOTOS_DEST'] = './market/static/resources'
app.config['UPLOADED_USERPHOTOS_DEST'] = './market/static/userresources'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'

photos = UploadSet('photos', IMAGES) 
userphotos = UploadSet('userphotos', IMAGES)
configure_uploads(app, photos)
configure_uploads(app, userphotos)

from market import routes