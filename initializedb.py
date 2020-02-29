from jyl import db, app, bcrypt
from jyl.models import *
from hashlib import sha256
from datetime import datetime

db.create_all()

'''
pass1 = bcrypt.generate_password_hash(
    sha256(
        ('pass' +
         'raf@demo.com' +
         app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')
pass2 = bcrypt.generate_password_hash(
    sha256(
        ('pass' +
         'rafa@demo.com' +
         app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')
user_1 = User(
    firstname='rafael',
    lastname='cenzano',
    email='raf@demo.com',
    password=pass1,
    confirmed=True,
    hours=0.0,
    nickname='raf',
    nicknameapprove=False)
db.session.add(user_1)
user_2 = User(
    firstname='rafael',
    lastname='cenzano',
    email='rafa@demo.com',
    password=pass2,
    confirmed=True,
    hours=0.0,
    nickname='raf',
    nicknameapprove=True,
    namecount=1)
db.session.add(user_2)

db.session.commit()
'''
'''
start = datetime(2020, 2, 26, 16, 30)

end = datetime(2020, 2, 26, 18)

meeting = Meeting(
    start=start,
    end=end,
    hourcount=1.5,
    description='hello there')

start2 = datetime(2020, 2, 19, 16, 30)

end2 = datetime(2020, 2, 19, 18)

meeting2 = Meeting(
    start=start2,
    end=end2,
    hourcount=1.5,
    description='hello world')

user1 = User.query.filter_by(email='raf@demo.com').first()
user2 = User.query.filter_by(email='rafa@demo.com').first()

db.session.add(meeting)
db.session.add(meeting2)

db.session.commit()

meeting1 = Meeting.query.filter_by(start=start).first()
meeting2 = Meeting.query.filter_by(start=start2).first()

usermeeting1 = UserMeeting(meetingid=meeting1.id, userid=user1.id)
usermeeting2 = UserMeeting(meetingid=meeting1.id, userid=user2.id)
usermeeting3 = UserMeeting(meetingid=meeting2.id, userid=user1.id)

db.session.add(usermeeting1)
db.session.add(usermeeting2)
db.session.add(usermeeting3)

# commit the chagnes to the db
db.session.commit()
'''

start = datetime(2020, 3, 4, 16, 30)

end = datetime(2020, 3, 4, 18)

meeting = Meeting(
    start=start,
    end=end,
    hourcount=1.5,
    description='future meeting')

start2 = datetime(2020, 2, 12, 16, 30)

end2 = datetime(2020, 2, 12, 18)

meeting2 = Meeting(
    start=start2,
    end=end2,
    hourcount=1.5,
    description='past meeting')

db.session.add(meeting)
db.session.add(meeting2)
db.session.commit()

start3 = datetime(2020, 2, 5, 16, 30)

end3 = datetime(2020, 2, 5, 18)

meeting3 = Meeting(
    start=start3,
    end=end3,
    hourcount=1.5,
    description='way past meeting')

db.session.add(meeting3)
db.session.commit()

start4 = datetime(2020, 1, 29, 16, 30)

end4 = datetime(2020, 1, 12, 18)

meeting4 = Meeting(
    start=start4,
    end=end4,
    hourcount=1.5,
    description='super far past meeting')

db.session.add(meeting4)
db.session.commit()

user1 = User.query.filter_by(email='raf@demo.com').first()
user2 = User.query.filter_by(email='rafa@demo.com').first()

meeting1 = Meeting.query.filter_by(start=start).first()
meeting2 = Meeting.query.filter_by(start=start2).first()

usermeeting1 = UserMeeting(meetingid=meeting1.id, userid=user1.id)
usermeeting2 = UserMeeting(meetingid=meeting1.id, userid=user2.id)
usermeeting3 = UserMeeting(meetingid=meeting2.id, userid=user2.id)
usermeeting4 = UserMeeting(meetingid=meeting3.id, userid=user1.id)
usermeeting5 = UserMeeting(meetingid=meeting3.id, userid=user2.id)
usermeeting6 = UserMeeting(meetingid=meeting4.id, userid=user1.id)
usermeeting7 = UserMeeting(meetingid=meeting4.id, userid=user2.id)

db.session.add(usermeeting1)
db.session.add(usermeeting2)
db.session.add(usermeeting3)
db.session.add(usermeeting4)
db.session.add(usermeeting5)
db.session.add(usermeeting6)
db.session.add(usermeeting7)

# commit the chagnes to the db
db.session.commit()