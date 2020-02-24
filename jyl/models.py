from jyl import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(30), unique=False, nullable=False)
    lastname = db.Column(db.String(30), unique=False, nullable=False)
    nickname = db.Column(db.String(30), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    confirmed = db.Column(db.Boolean, unique=False, default=False)
    registered = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    admin = db.Column(db.Boolean, unique=False, default=False)
    leader = db.Column(db.Boolean, unique=False, default=False)
    hours = db.Column(db.Float, unique=False)
    nicknameapprove = db.Column(db.Boolean, unique=False, default=False)

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


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    start = db.Column(db.DateTime, nullable=False, unique=False)
    end = db.Column(db.DateTime, nullable=False, unique=False)
    length = db.Column(db.Integer, nullable=False, unique=False)

    def __repr__(self):
        return f'Meeting id:{self.id}, from {self.start} to {self.end})'


class UserMeeting(db.Model):
    meetingid = db.Column(db.Integer, db.ForeignKey('meeting.id'),  primary_key=True, unique=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, unique=False)

    def __repr__(self):
        return f'User: {self.userid} went to meeting:{self.meetingid})'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    start = db.Column(db.DateTime, nullable=False, unique=False)
    end = db.Column(db.DateTime, nullable=False, unique=False)

    def __repr__(self):
        return f'Event id:{self.id}, from {self.start} to {self.end})'


class EventMeeting(db.Model):
    eventid = db.Column(db.Integer, db.ForeignKey('event.id'),  primary_key=True, unique=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, unique=False)
    length = db.Column(db.Integer, nullable=False, unique=False)

    def __repr__(self):
        return f'User: {self.userid} went to event:{self.eventid})'