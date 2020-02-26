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
user_1 = User(firstname='rafael', lastname='cenzano', email='raf@demo.com', password=pass1, confirmed=True, hours=0.0, nickname='raf', nicknameapprove=False)
db.session.add(user_1)
user_2 = User(firstname='rafael', lastname='cenzano', email='rafa@demo.com', password=pass2, confirmed=True, hours=0.0, nickname='raf', nicknameapprove=True)
db.session.add(user_2)
'''

start = datetime(2020, 2, 26, 16, 30)

end = datetime(2020, 2, 26, 18)

meeting = Meeting(start=start, end=end, hourcount=1.5)

start2 = datetime(2020, 2, 19, 16, 30)

end2 = datetime(2020, 2, 19, 18)

meeting2 = Meeting(start=start, end=end, hourcount=1.5)

user1 = User.query.filter_by(email='raf@demo.com').first()
user2 = User.query.filter_by(email='rafa@demo.com').first()

db.session.add(meeting)
db.session.add(meeting2)

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

