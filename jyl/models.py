from jyl import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, unique=False, default=False)
    registered = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    admin = db.Column(db.Boolean, unique=False, default=False)
    superuser = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return f'User({self.username}, {self.email})'

    '''
    Create a reset token for the user
    '''
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    '''
    A static func to get the token and get user with the id
    '''
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        '''
        Try to get the user id
        If it doesn't work then the func will return None
        '''
        try:
            user_id = s.loads(token)['user_id']
        except BaseException:
            return None
        return User.query.get(user_id)
