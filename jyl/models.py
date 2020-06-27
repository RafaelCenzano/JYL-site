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
    admin = db.Column(db.Boolean, unique=False, default=False)
    leader = db.Column(db.Boolean, unique=False, default=False)
    lifetimeHours = db.Column(db.Float, unique=False, default=0.0)
    lifetimeMeetingHours = db.Column(db.Float, unique=False, default=0.0)
    lifetimeEventHours = db.Column(db.Float, unique=False, default=0.0)
    lifetimeMeetingCount = db.Column(db.Integer, unique=False)
    lifetimeEventCount = db.Column(db.Integer, unique=False)
    currentHours = db.Column(db.Float, unique=False, default=0.0)
    currentMeetingHours = db.Column(db.Float, unique=False, default=0.0)
    currentEventHours = db.Column(db.Float, unique=False, default=0.0)
    currentMeetingCount = db.Column(db.Integer, unique=False)
    currentEventCount = db.Column(db.Integer, unique=False)
    nicknameapprove = db.Column(db.Boolean, unique=False, default=False)
    namecount = db.Column(db.Integer, unique=False, default=0)
    school = db.Column(db.String(100), unique=False)
    grade = db.Column(db.Integer, unique=False)
    currentmember = db.Column(db.Boolean, unique=False)
    bio = db.Column(db.String(500), unique=False)
    numberphone = db.Column(db.String(10), unique=False)
    address = db.Column(db.String(500), unique=False)
    showemail = db.Column(db.Boolean, unique=False, default=False)
    showphone = db.Column(db.Boolean, unique=False, default=False)
    meetingAlertoneday = db.Column(db.Boolean, unique=False)
    meetingAlertthreeday = db.Column(db.Boolean, unique=False)
    meetingAlertoneweek = db.Column(db.Boolean, unique=False)
    eventAlertoneday = db.Column(db.Boolean, unique=False)
    eventAlertthreeday = db.Column(db.Boolean, unique=False)
    eventAlertoneweek = db.Column(db.Boolean, unique=False)
    ingroup = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return f'User({self.firstname} {self.lastname}, {self.email})'

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
    hourcount = db.Column(db.Float, nullable=False, unique=False)
    description = db.Column(db.String(500), nullable=False, unique=False)
    upvote = db.Column(db.Integer, nullable=False, unique=False, default=0)
    unsurevote = db.Column(db.Integer, unique=False, default=0)
    downvote = db.Column(db.Integer, nullable=False, unique=False, default=0)
    location = db.Column(db.String(150), unique=False)
    currentYear = db.Column(db.Boolean, unique=False)
    attendancecount = db.Column(db.Integer, unique=False)
    attendancecheck = db.Column(db.Boolean, unique=False)
    alertoneday = db.Column(db.Boolean, unique=False, default=False)
    alertthreeday = db.Column(db.Boolean, unique=False, default=False)
    alertoneweek = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return f'Meeting id:{self.id}, from {self.start} to {self.end})'


class UserMeeting(db.Model):
    meetingid = db.Column(
        db.Integer,
        db.ForeignKey('meeting.id'),
        primary_key=True,
        unique=False)
    userid = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        unique=False)
    attended = db.Column(db.Boolean, default=False)
    going = db.Column(db.Boolean, default=False)
    comment = db.Column(db.String(500), nullable=True)
    upvote = db.Column(db.Boolean)
    unsurevote = db.Column(db.Boolean)
    downvote = db.Column(db.Boolean)
    currentYear = db.Column(db.Boolean, unique=False)

    def __repr__(self):
        if self.attended:
            return f'User: {self.userid} went to meeting:{self.meetingid})'
        elif self.going:
            return f'User: {self.userid} wants to go to meeting:{self.meetingid})'
        return f'User: {self.userid} meeting:{self.meetingid})'


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    start = db.Column(db.DateTime, nullable=False, unique=False)
    end = db.Column(db.DateTime, nullable=False, unique=False)
    hourcount = db.Column(db.Float, nullable=False, unique=False)
    description = db.Column(db.String(500), nullable=False, unique=False)
    upvote = db.Column(db.Integer, nullable=False, unique=False, default=0)
    unsurevote = db.Column(db.Integer, unique=False, default=0)
    downvote = db.Column(db.Integer, nullable=False, unique=False, default=0)
    location = db.Column(db.String(150), unique=False)
    currentYear = db.Column(db.Boolean, unique=False)
    attendancecount = db.Column(db.Integer, unique=False)
    attendancecheck = db.Column(db.Boolean, unique=False)
    alertoneday = db.Column(db.Boolean, unique=False, default=False)
    alertthreeday = db.Column(db.Boolean, unique=False, default=False)
    alertoneweek = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return f'Event id:{self.id}, from {self.start} to {self.end})'


class UserEvent(db.Model):
    eventid = db.Column(
        db.Integer,
        db.ForeignKey('event.id'),
        primary_key=True,
        unique=False)
    userid = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        unique=False)
    attended = db.Column(db.Boolean, default=False)
    going = db.Column(db.Boolean, default=False)
    comment = db.Column(db.String(500), nullable=True)
    upvote = db.Column(db.Boolean)
    unsurevote = db.Column(db.Boolean)
    downvote = db.Column(db.Boolean)
    currentYear = db.Column(db.Boolean, unique=False)

    def __repr__(self):
        if self.attended:
            return f'User: {self.userid} went to event:{self.eventid})'
        elif self.going:
            return f'User: {self.userid} wants to go to event:{self.eventid})'
        return f'User: {self.userid} event:{self.eventid})'


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    leaderid = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        unique=False)
    currentYear = db.Column(db.Boolean, unique=False)
    goal = db.Column(db.String(500), unique=False)

    def __repr__(self):
        return f'Group id:{self.id}'


class UserGroup(db.Model):
    groupid = db.Column(
        db.Integer,
        db.ForeignKey('group.id'),
        primary_key=True,
        unique=False)
    userid = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        unique=False)
    currentYear = db.Column(db.Boolean, unique=False)

    def __repr__(self):
        return f'User {userid} is in {groupid} group'


class YearAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    leaderid = db.Column(
        db.Integer,
        db.ForeignKey('user.id'), unique=False)
    time = db.Column(db.DateTime, nullable=False, unique=False)
    confirmed = db.Column(db.Boolean, nullable=False, unique=False)
    completed = db.Column(db.Boolean, nullable=False, unique=False)

