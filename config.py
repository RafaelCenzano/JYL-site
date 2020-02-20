import os

'''
Config file containing Config class
'''


class Config:

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(32)
