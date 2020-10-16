import random
import sys
from datetime import datetime
from hashlib import sha256

from jyl import app, bcrypt, db
from jyl.models import *

if sys.argv[1] == 'migrate':

    users = User.query.filter_by(currentmember=True).all()
    for user in users:
        user.meetingAlertoneday = False
        user.meetingAlertthreeday = False
        user.meetingAlertoneweek = False
        user.eventAlertoneday = False
        user.eventAlertthreeday = False
        user.eventAlertoneweek = False
        db.session.commit()

    meetings = Meeting.query.filter_by(currentYear=True).all()
    events = Event.query.filter_by(currentYear=True).all()

    for meeting in meetings:
        meeting.alertoneweek = True
        meeting.alertthreeday = True
        meeting.alertoneday = True
        db.session.commit()

    for event in events:
        event.alertoneweek = True
        event.alertthreeday = True
        event.alertoneday = True
        db.session.commit()

elif sys.argv[1] == 'clear':
    db.drop_all()
    db.create_all()

elif sys.argv[1] == 'production':
    db.create_all()

    pass1 = bcrypt.generate_password_hash(
        sha256(
            ('pass' +
             'demo@domain.com' +
             app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')

    user = User(
        firstname='Andy',
        lastname='Bernard',
        email='demo@domain.com',
        password=pass1,
        lifetimeHours=0,
        lifetimeMeetingHours=0,
        lifetimeEventHours=0,
        lifetimeMeetingCount=0,
        lifetimeEventCount=0,
        currentHours=0,
        currentMeetingHours=0,
        currentEventHours=0,
        currentMeetingCount=0,
        currentEventCount=0,
        nickname='Drew',
        nicknameapprove=True,
        admin=True,
        leader=True,
        namecount=0,
        school='Cornell',
        grade=12,
        currentmember=True,
        numberphone='5555555555',
        showemail=False,
        showphone=False,
        meetingAlertoneday=False,
        meetingAlertthreeday=False,
        meetingAlertoneweek=False,
        eventAlertoneday=False,
        eventAlertthreeday=False,
        eventAlertoneweek=False,
        address='Scranton PA',
        bio='The Office is amazing')

    db.session.add(user)
    db.session.commit()

else:
    sys.exit('No argument or exsisting argument found')
