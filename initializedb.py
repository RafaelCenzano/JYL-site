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
    lifetimeHours=300.0,
    lifetimeMeetingHours=202.0,
    lifetimeEventHours=300 - 202.0,
    lifetimeMeetingCount=66,
    lifetimeEventCount=50,
    currentHours=56.5,
    currentMeetingHours=35.5,
    currentEventHours=56.5 - 35.5,
    currentMeetingCount=23,
    currentEventCount=5,
    nickname=None,
    nicknameapprove=False,
    admin=True,
    leader=False,
    namecount=0,
    school='Lowell',
    grade=11,
    currentmember=True,
    bio='876 q784538 9762547625376 328763252')

user2 = User(
    firstname='rafael',
    lastname='cenzano',
    email='rafa@demo.com',
    password=pass2,
    lifetimeHours=25.5,
    lifetimeMeetingHours=10.0,
    lifetimeEventHours=15.5,
    lifetimeMeetingCount=4,
    lifetimeEventCount=4,
    currentHours=20,
    currentMeetingHours=10.0,
    currentEventHours=10.0,
    currentMeetingCount=3,
    currentEventCount=3,
    nickname='raf',
    nicknameapprove=True,
    admin=True,
    leader=True,
    namecount=1,
    school='Lowell',
    grade=11,
    currentmember=True,
    bio='88588 3g432hghjg hj2g4 jh23g4hj3g4 3hgj2343')

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
    location='2012 Pine St.',
    currentYear=True)

start1 = datetime(2020, 2, 19, 16, 30)
end1 = datetime(2020, 2, 19, 18)

meeting1 = Meeting(
    currentYear=True,
    start=start1,
    end=end1,
    hourcount=1.5,
    upvote=0,
    downvote=0,
    unsurevote=0,
    description='hello world',
    location='2012 Pine St.')

start = datetime(2020, 3, 4, 16, 30)
end = datetime(2020, 3, 4, 18)
meeting = Meeting(
    currentYear=True,
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
    currentYear=True,
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
    currentYear=True,
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
    currentYear=True,
    start=start4,
    end=end4,
    hourcount=1.5,
    description='super far past meeting',
    upvote=3,
    downvote=1,
    unsurevote=2,
    location='2012 Pine St.')

start = datetime(2020, 1, 30, 10)
end = datetime(2020, 1, 30, 18)
event = Event(
    currentYear=True,
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
    currentYear=True,
    name='An event 223!!!!',
    start=start1,
    end=end1,
    hourcount=8,
    description='235325325',
    upvote=0,
    downvote=0,
    unsurevote=0,
    location='1840 Sutter')

start2 = datetime(2020, 7, 30, 10)
end2 = datetime(2020, 7, 30, 18)
event2 = Event(
    currentYear=True,
    name='A future event',
    start=start2,
    end=end2,
    hourcount=8,
    description='lots of text, yeet',
    upvote=3,
    downvote=1,
    unsurevote=2,
    location='1840 Sutter')

start3 = datetime(2020, 9, 30, 10)
end3 = datetime(2020, 9, 30, 18)
event3 = Event(
    currentYear=True,
    name='A future event test',
    start=start3,
    end=end3,
    hourcount=8,
    description='lots of text, yeeters',
    upvote=3,
    downvote=1,
    unsurevote=2,
    location='1840 Sutter')

db.session.add(event)
db.session.add(event1)
db.session.add(event2)
db.session.add(event3)
db.session.add(meeting)
db.session.add(meeting0)
db.session.add(meeting1)
db.session.add(meeting2)
db.session.add(meeting3)
db.session.add(meeting4)
db.session.commit()

usermeeting = UserMeeting(
    currentYear=True,
    meetingid=meeting0.id,
    userid=user1.id,
    attended=True,
    going=True,
    comment='test1',
    upvote=True,
    downvote=False,
    unsurevote=False)
usermeeting0 = UserMeeting(
    currentYear=True,
    meetingid=meeting1.id,
    userid=user1.id,
    attended=True,
    going=True,
    comment='4243',
    upvote=True,
    downvote=False,
    unsurevote=False)
usermeeting1 = UserMeeting(
    currentYear=True,
    meetingid=meeting.id,
    userid=user1.id,
    attended=True,
    going=True,
    comment='sfafsaf',
    upvote=True,
    downvote=False,
    unsurevote=False)
usermeeting2 = UserMeeting(
    currentYear=True,
    meetingid=meeting.id,
    userid=user2.id,
    attended=True,
    going=True,
    comment='asfvcvc',
    upvote=True,
    downvote=False,
    unsurevote=False)
usermeeting3 = UserMeeting(
    currentYear=True,
    meetingid=meeting2.id,
    userid=user1.id,
    attended=True,
    going=True,
    comment='jhjytjy',
    unsurevote=True,
    downvote=False,
    upvote=False)
usermeeting4 = UserMeeting(
    currentYear=True,
    meetingid=meeting3.id,
    userid=user1.id,
    attended=True,
    going=True,
    comment='tysdfsfdsfsdfdsfsdfds',
    upvote=True,
    downvote=False,
    unsurevote=False)
usermeeting5 = UserMeeting(
    currentYear=True,
    meetingid=meeting3.id,
    userid=user2.id,
    attended=True,
    going=True,
    comment='adsdfsasd',
    downvote=True,
    upvote=False,
    unsurevote=False)
usermeeting6 = UserMeeting(
    currentYear=True,
    meetingid=meeting4.id,
    userid=user1.id,
    attended=True,
    going=True,
    comment='adsdsfsdsdfsdfsdgsasd',
    downvote=True,
    upvote=False,
    unsurevote=False)
usermeeting7 = UserMeeting(
    currentYear=True,
    meetingid=meeting4.id,
    userid=user2.id,
    attended=True,
    going=True,
    comment='adsdsgsdgsdgsdgsdasd',
    upvote=True,
    downvote=False,
    unsurevote=False)
userevent = UserEvent(
    currentYear=True,
    eventid=event.id,
    userid=user1.id,
    attended=True,
    going=True,
    comment='danelle',
    upvote=True,
    downvote=False,
    unsurevote=False)
userevent1 = UserEvent(
    currentYear=True,
    eventid=event.id,
    userid=user2.id,
    attended=True,
    going=True,
    comment='erkia',
    upvote=True,
    downvote=False,
    unsurevote=False)
userevent2 = UserEvent(
    currentYear=True,
    eventid=event1.id,
    userid=user1.id,
    attended=True,
    going=True,
    comment='debbie',
    upvote=True,
    downvote=False,
    unsurevote=False)
userevent3 = UserEvent(
    currentYear=True,
    eventid=event1.id,
    userid=user2.id,
    attended=True,
    going=True,
    comment='JOHN',
    upvote=True,
    downvote=False,
    unsurevote=False)
userevent4 = UserEvent(
    currentYear=True,
    eventid=event2.id,
    userid=user1.id,
    attended=False,
    going=True,
    comment='adsdasd',
    upvote=True,
    downvote=False,
    unsurevote=False)
userevent5 = UserEvent(
    currentYear=True,
    eventid=event2.id,
    userid=user2.id,
    attended=False,
    going=True,
    comment='mikio',
    unsurevote=True,
    downvote=False,
    upvote=False)
userevent6 = UserEvent(
    currentYear=True,
    eventid=event3.id,
    userid=user1.id,
    attended=False,
    going=False,
    comment='mikio',
    unsurevote=True,
    downvote=False,
    upvote=False)

db.session.add(userevent)
db.session.add(userevent1)
db.session.add(userevent2)
db.session.add(userevent3)
db.session.add(userevent4)
db.session.add(userevent5)
db.session.add(userevent6)
db.session.add(usermeeting)
db.session.add(usermeeting0)
db.session.add(usermeeting1)
db.session.add(usermeeting2)
db.session.add(usermeeting3)
db.session.add(usermeeting4)
db.session.add(usermeeting5)
db.session.add(usermeeting6)
db.session.add(usermeeting7)

# commit the chagnes to the db
db.session.commit()
