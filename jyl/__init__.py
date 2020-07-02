# Import Flask for flask app object
from flask import Flask

# Import Flask modules
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from config import Config


# Create flask app object
app = Flask(__name__)
app.config.from_object(Config)


# Create Database object from brcrypt object
db = SQLAlchemy(app, session_options{'expire_on_commit': False})
bcrypt = Bcrypt(app)


# Create Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'


# Create mail object from flask app object
mail = Mail(app)


# importing all the models and initializing them
from jyl.models import *
db.create_all()


# Import all views
import jyl.views
import jyl.tasks