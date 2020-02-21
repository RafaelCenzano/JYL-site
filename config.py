import os

'''
To create a secret key run the program
import secrets
secrets.token_hex(16)
'''

'''
Config class
'''
class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.environ.get('jylKey')
    SECURITY_PASSWORD_SALT = os.environ.get('jylSalt')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    '''
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'email@gmail.com'
    MAIL_PASSWORD = secret.EMAIL_PASS
    MAIL_DEFAULT_SENDER = 'JYL Toolbox <email@gmail.com>'
    '''