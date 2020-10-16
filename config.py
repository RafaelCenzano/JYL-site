import os


'''
Config class
'''


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.environ.get('jylKey')
    SECURITY_PASSWORD_SALT = os.environ.get('jylSalt')

    TESTING = False
    DEBUG = False

    # Using Postgresql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    email = os.environ.get('jylSenderEmail')
    MAIL_USERNAME = email
    MAIL_PASSWORD = os.environ.get('jylEmailPass')
    MAIL_DEFAULT_SENDER = f'JYL Toolbox <{email}>'

    # Sentry config
    SENTRY_URL = os.environ.get('jylSentry')