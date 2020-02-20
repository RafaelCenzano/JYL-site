# Flask imports
from flask import Flask
from config import Config

# Create Flask app
app = Flask(__name__)

# Add Configurations to app
app.config.from_object(Config)

# Import all views
import jyl.views