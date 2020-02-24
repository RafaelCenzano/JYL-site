# Import Flask for flask app object
from flask import Flask

# Import Flask modules to create objects for our app
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Create flask app object
app = Flask(__name__)

# Add configurations to app
app.config.from_object(Config)

# Create Database object from flask app object
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Create Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Create mail object from flask app object
#mail = Mail(app)

# importing all the models and initializing them
from jyl.models import *
db.create_all()

user_1 = User(firstname='rafael', lastname='cenzano', email='r@demo.com', password='pass', confirmed=True, hours=0, nickname='raf', nicknameapprove=False)
db.session.add(user_1)
user_2 = User(firstname='rafael', lastname='cenzano', email='ra@demo.com', password='pass', confirmed=True, hours=0, nickname='raf', nicknameapprove=True)
db.session.add(user_2)

# Import all views
import jyl.views