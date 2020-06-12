from jyl import db, app, bcrypt
from jyl.models import *
from hashlib import sha256
from datetime import datetime
import random
import sys


if sys.argv[1] == 'testing':

    db.drop_all()
    db.create_all()
    # testing db setup

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
        numberphone='4156007000',
        showemail=False,
        showphone=False,
        meetingAlertoneday=False,
        meetingAlertthreeday=False,
        meetingAlertoneweek=False,
        eventAlertoneday=False,
        eventAlertthreeday=False,
        eventAlertoneweek=False,
        address='Place',
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
        numberphone='4157006000',
        showemail=True,
        showphone=True,
        meetingAlertoneday=False,
        meetingAlertthreeday=False,
        meetingAlertoneweek=False,
        eventAlertoneday=False,
        eventAlertthreeday=False,
        eventAlertoneweek=False,
        address='Place',
        bio='88588 3g432hghjg hj2g4 jh23g4hj3g4 3hgj2343')

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    firstnames = [
        'Jim',
        'Dwight',
        'Stanley',
        'Phyllis',
        'Toby',
        'Micheal',
        'Pam',
        'Kelly',
        'Ryan',
        'Creed',
        'Darryl',
        'Mose',
        'Angela',
        'Andy',
        'Nellie',
        'Erin',
        'Clark',
        'Pete',
        'Merideth',
        'Oscar',
        'Kevin',
        'Gabe',
        'Jan',
        'David',
        'Robert',
        'Roy',
        'Holly',
        'Jo',
        'Cathy',
        'Devon',
        'Danny',
        'A',
        'Karren',
        'Tod',
        'Hide',
        'Val',
        'Nate',
        'Josh',
        'Ed']

    lastnames = [
        'Halpert',
        'Schrute',
        'Hudson',
        'Vance',
        'Flenderson',
        'Scott',
        'Halpert',
        'Kapoor',
        'Howard',
        'Bratton',
        'Philbin',
        'Schrute',
        'Schrute',
        'Bernard',
        'Bertram',
        'Hannon',
        'Green',
        'Miller',
        'Palmer',
        'Martinez',
        'Malone',
        'Lewis',
        'Levison',
        'Wallace',
        'California',
        'Anderson',
        'Flax',
        'Bennet',
        'Simms',
        'White',
        'Cordray',
        'J',
        'Filipelli',
        'Packer',
        'Hasagawa',
        'Johnson',
        'Nickerson',
        'Porter',
        'Truck']

    for i in range(len(firstnames)):

        email = random.choice(['gmail', 'yahoo', 'outlook', 'aol', 'icloud'])
        bios = ['How the turn tables', 
                'WHERE ARE THE TURTLES', 
                'Early worm get the worm', 
                'They say fool you once strike one. But fool me twice, strike three', 
                'I\'m not superstitous. But I am a little sticious',
                'Sometimes i\'ll start a sentence and I don\'t event know where it\'s going. I just hope I find it along the way']

        nicknames = ['Drew',
                     'The Temp',
                     'Tuna',
                     'Dwight Jr.',
                     'Plop',
                     'Dwigt',
                     'Fire Guy',
                     'Fired Guy',
                     'Hired Guy',
                     'Nard Dog']

        first = repr(random.randrange(100, 999))
        last = repr(random.randrange(1000, 9999))
        middle = repr(random.randrange(100, 999))

        user = User(
            firstname=firstnames[i],
            lastname=lastnames[i],
            email=f'{firstnames[i]}{lastnames[i]}@{email}.com',
            password='hello',
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
            nickname=random.choice(nicknames),
            nicknameapprove=False,
            admin=False,
            leader=False,
            namecount=0,
            school=random.choice(['Stamford', 'Scranton', 'New York', 'Jupiter', 'Syracruse', 'Utica', 'Albany', 'Nashua']),
            grade=random.randrange(9, 12),
            currentmember=True,
            numberphone=f'{first}{middle}{last}',
            showemail=random.choice([True, False]),
            showphone=random.choice([True, False]),
            meetingAlertoneday=False,
            meetingAlertthreeday=False,
            meetingAlertoneweek=False,
            eventAlertoneday=False,
            eventAlertthreeday=False,
            eventAlertoneweek=False,
            address=random.choice(['Stamford', 'Scranton', 'New York', 'Jupiter', 'Syracruse', 'Utica', 'Albany', 'Nashua']),
            bio=random.choice(bios))

        db.session.add(user)
        db.session.commit()

elif sys.argv[1] == 'migrate':

    users = User.query.filter_by(currentmember=True).all()
    for user in users:
        users.meetingAlertoneday = False
        users.meetingAlertthreeday = False
        users.meetingAlertoneweek = False
        users.eventAlertoneday = False
        users.eventAlertthreeday = False
        users.eventAlertoneweek = False
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
        firstname='zStart',
        lastname='zAdmin',
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
        nicknameapprove=False,
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
