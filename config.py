import os


'''
Config class
'''


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.environ.get('jylKey')
    SECURITY_PASSWORD_SALT = os.environ.get('jylSalt')

    TESTING = True
    DEBUG = True

    # Using Postgresql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'email@gmail.com'
    MAIL_PASSWORD = os.environ.get('jylEmailPass')
    email = os.environ.get('jylEmail')
    MAIL_DEFAULT_SENDER = f'JYL Toolbox <{email}>'