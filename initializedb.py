from jyl import db, app, bcrypt
from jyl.models import *
from hashlib import sha256
from datetime import datetime

db.drop_all()
db.create_all()

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

user1 = User(
    firstname='rafael',
    lastname='cenzano',
    email='raf@demo.com',
    password=pass1,
    confirmed=True,
    lifetimeHours=0.0,
    lifetimeMeetingHours=0.0,
    lifetimeEventHours=0.0,
    currentHours=0.0,
    currentMeetingHours=0.0,
    currentEvent=0.0,
    nickname='raf',
    nicknameapprove=False,
    admin=True,
    leader=True)

user2 = User(
    firstname='rafael',
    lastname='cenzano',
    email='rafa@demo.com',
    password=pass2,
    confirmed=True,
    lifetimeHours=0.0,
    lifetimeMeetingHours=0.0,
    lifetimeEventHours=0.0,
    currentHours=0.0,
    currentMeetingHours=0.0,
    currentEvent=0.0,
    nickname='raf',
    nicknameapprove=True,
    namecount=1,
    admin=True,
    leader=True)

db.session.add(user1)
db.session.add(user2)
db.session.commit()

start0 = datetime(2020, 2, 26, 16, 30)
end0 = datetime(2020, 2, 26, 18)

meeting0 = Meeting(
    start=start0,
    end=end0,
    hourcount=1.5,
    description='hello there',
    upvote=0,
    downvote=0,
    unsurevote=0,
    location='2012 Pine St.')

start1 = datetime(2020, 2, 19, 16, 30)
end1 = datetime(2020, 2, 19, 18)

meeting1 = Meeting(
    start=start1,
    end=end1,
    hourcount=1.5,
    description='hello world',
    location='2012 Pine St.')

start = datetime(2020, 3, 4, 16, 30)
end = datetime(2020, 3, 4, 18)
meeting = Meeting(
    start=start,
    end=end,
    hourcount=1.5,
    description='future meeting',
    upvote=0,
    downvote=0,
    unsurevote=0,
    location='2012 Pine St.')

start2 = datetime(2020, 2, 12, 16, 30)
end2 = datetime(2020, 2, 12, 18)
meeting2 = Meeting(
    start=start2,
    end=end2,
    hourcount=1.5,
    description='past meeting',
    upvote=0,
    downvote=0,
    unsurevote=0,
    location='2012 Pine St.')

start3 = datetime(2020, 2, 5, 16, 30)
end3 = datetime(2020, 2, 5, 18)
meeting3 = Meeting(
    start=start3,
    end=end3,
    hourcount=1.5,
    description='way past meeting',
    upvote=0,
    downvote=0,
    unsurevote=0,
    location='2012 Pine St.')

start4 = datetime(2020, 1, 29, 16, 30)
end4 = datetime(2020, 1, 29, 18)
meeting4 = Meeting(
    start=start4,
    end=end4,
    hourcount=1.5,
    description='super far past meeting',
    upvote=0,
    downvote=0,
    unsurevote=0,
    location='2012 Pine St.')

start = datetime(2020, 1, 30, 10)
end = datetime(2020, 1, 30, 18)
event = Event(
    name='An event!!!!',
    start=start,
    end=end,
    hourcount=8,
    description='adsasadsad',
    upvote=0,
    downvote=0,
    unsurevote=0,
    location='1840 Sutter')

start1 = datetime(2020, 1, 30, 10)
end1 = datetime(2020, 1, 30, 18)
event1 = Event(
    name='An event 223!!!!',
    start=start1,
    end=end1,
    hourcount=8,
    description='235325325',
    upvote=0,
    downvote=0,
    unsurevote=0,
    location='1840 Sutter')

db.session.add(event)
db.session.add(event1)
db.session.add(meeting0)
db.session.add(meeting1)
db.session.add(meeting)
db.session.add(meeting2)
db.session.add(meeting3)
db.session.add(meeting4)
db.session.commit()

usermeeting0 = UserMeeting(meetingid=meeting0.id, userid=user1.id, attended=True, going=True)
usermeeting = UserMeeting(meetingid=meeting1.id, userid=user1.id, attended=True, going=True)
usermeeting1 = UserMeeting(meetingid=meeting.id, userid=user1.id, attended=True, going=True)
usermeeting2 = UserMeeting(meetingid=meeting.id, userid=user2.id, attended=True, going=True)
usermeeting3 = UserMeeting(meetingid=meeting2.id, userid=user1.id, attended=True, going=True)
usermeeting4 = UserMeeting(meetingid=meeting3.id, userid=user1.id, attended=True, going=True)
usermeeting5 = UserMeeting(meetingid=meeting3.id, userid=user2.id, attended=True, going=True)
usermeeting6 = UserMeeting(meetingid=meeting4.id, userid=user1.id, attended=True, going=True)
usermeeting7 = UserMeeting(meetingid=meeting4.id, userid=user2.id, attended=True, going=True)
userevent = UserEvent(eventid=event.id, userid=user1.id, attended=True, going=True)
userevent1 = UserEvent(eventid=event.id, userid=user2.id, attended=True, going=True)
userevent2 = UserEvent(eventid=event1.id, userid=user1.id, attended=True, going=True)
userevent3 = UserEvent(eventid=event1.id, userid=user2.id, attended=True, going=True)

db.session.add(userevent)
db.session.add(userevent1)
db.session.add(userevent2)
db.session.add(userevent3)
db.session.add(usermeeting0)
db.session.add(usermeeting)
db.session.add(usermeeting1)
db.session.add(usermeeting2)
db.session.add(usermeeting3)
db.session.add(usermeeting4)
db.session.add(usermeeting5)
db.session.add(usermeeting6)
db.session.add(usermeeting7)

# commit the chagnes to the db
db.session.commit()