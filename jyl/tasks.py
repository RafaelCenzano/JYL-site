from datetime import datetime
from flask_mail import Message
from pytz import timezone

from jyl import app, db, mail
from jyl.models import *

pacific = timezone('US/Pacific')


def backgroundCheck():
    print('Start background Checks')
    meetings = Meeting.query.filter_by(currentYear=True).all()
    events = Event.query.filter_by(currentYear=True).all()
    users = User.query.filter_by(currentmember=True, leader=False).all()
    groups = Group.query.filter_by(currentYear=True).all()
    audits = YearAudit.query.filter_by(confirmed=True, completed=False).all()
    for event in events:
        print(event)
    for meeting in meetings:
        print(meeting)

    now = pacific.localize(datetime.now())

    if audits:
        for audit in audits:
            if (now - pacific.localize(audit.time)
                ).days >= 7 and not audit.completed and audit.confirmed:

                with app.app_context():
                    for meeting in meetings:
                        meeting.currentYear = False
                        db.session.commit()

                    for event in events:
                        event.currentYear = False
                        db.session.commit()

                    for group in groups:
                        group.currentYear = False
                        db.session.commit()

                    for user in users:
                        user.grade += 1
                        if user.grade > 12:
                            user.currentmember = False
                        user.ingroup = False
                        db.session.commit()

                    usermeeting = UserMeeting.query.filter_by(currentYear=True).all()
                    userevent = UserEvent.query.filter_by(currentYear=True).all()

                    for item in usermeeting:
                        item.currentYear = False
                        db.session.commit()

                    for item in userevent:
                        item.currentYear = False
                        db.session.commit()

                    audit.completed = True
                    db.session.commit()

    if meetings:
        for meeting in meetings:
            meetingDate = pacific.localize(meeting.start)
            if meetingDate > now:
                meetingDelta = (meetingDate - now).days
                if meetingDelta == 7 and meeting.alertoneweek is False:

                    meetingTime = meeting.start.strftime(
                        '%A %B %-d %Y at %-I:%M %p')
                    meetingLocation = meeting.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having a meeting in a week on <strong>{meetingTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{meetingLocation}">{meeting.location}</a> for {meeting.hourcount} hours.</p>

<p>Checkout the meeting <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>

<a href="#">Update email notifications</a>
                    '''

                    text = f'''
Hello,

JYL is having a meeting in a week on {meetingTime}.

It will be at {meeting.location} for {meeting.hourcount} hours.

Checkout the meeting here!

- JYL Toolbox

Update email notifications (#settings)
                    '''

                    with app.app_context():
                        with mail.connect() as conn:
                            for user in users:
                                if user.meetingAlertthreeday:
                                    msg = Message(
                                        'Meeting in 1 week! - JYL Toolbox',
                                        recipients=[
                                            user.email])
                                    msg.body = text
                                    msg.html = html

                                    conn.send(msg)

                        meeting.alertoneweek = True
                        db.session.commit()

                elif meetingDelta == 3 and meeting.alertthreeday is False:

                    meetingTime = meeting.start.strftime(
                        '%A %B %-d %Y at %-I:%M %p')
                    meetingLocation = meeting.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having a meeting in three days on <strong>{meetingTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{meetingLocation}">{meeting.location}</a> for {meeting.hourcount} hours.</p>

<p>Checkout the meeting <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>

<a href="#">Update email notifications</a>
                    '''

                    text = f'''
Hello,

JYL is having a meeting in three days on {meetingTime}.

It will be at {meeting.location} for {meeting.hourcount} hours.

Checkout the meeting here!

- JYL Toolbox

Update email notifications (#settings)
                    '''

                    with app.app_context():
                        with mail.connect() as conn:
                            for user in users:
                                if user.meetingAlertoneweek:
                                    msg = Message(
                                        'Meeting in 3 days! - JYL Toolbox',
                                        recipients=[
                                            user.email])
                                    msg.body = text
                                    msg.html = html

                                    conn.send(msg)

                        meeting.alertthreeday = True
                        db.session.commit()

                elif meetingDelta == 1 and meeting.alertoneday is False:
                    print(meeting.alertoneday)

                    meetingTime = meeting.start.strftime(
                        '%A %B %-d %Y at %-I:%M %p')
                    meetingLocation = meeting.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having a meeting in one day on <strong>{meetingTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{meetingLocation}">{meeting.location}</a> for {meeting.hourcount} hours.</p>

<p>Checkout the meeting <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>

<a href="#">Update email notifications</a>
                    '''

                    text = f'''
Hello,

JYL is having a meeting in one day on {meetingTime}.

It will be at {meeting.location} for {meeting.hourcount} hours.

Checkout the meeting here!

- JYL Toolbox

Update email notifications (#settings)
                    '''

                    with app.app_context():
                        with mail.connect() as conn:
                            for user in users:
                                if user.meetingAlertoneday:
                                    msg = Message(
                                        'Meeting in 1 day! - JYL Toolbox',
                                        recipients=[
                                            user.email])
                                    msg.body = text
                                    msg.html = html

                                    conn.send(msg)

                        meeting.alertoneday = True
                        db.session.commit()
                        print('did i make it here?')
                        print(meeting.alertoneday)
                        print(Meeting.query.get(meeting.id).alertoneday)

    if events:
        for event in events:
            eventDate = pacific.localize(event.start)
            if eventDate > now:
                eventDelta = (eventDate - now).days
                if eventDelta == 7 and event.alertoneweek is False:

                    eventTime = event.start.strftime(
                        '%A %B %-d %Y at %-I:%M %p')
                    eventLocation = event.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having {event.name} in a week on <strong>{eventTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{eventLocation}">{event.location}</a> for {event.hourcount} hours.</p>

<p>Checkout the event <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>

<a href="#">Update email notifications</a>
                    '''

                    text = f'''
Hello,

JYL is having {event.name} in a week on {eventTime}.

It will be at {event.location} for {event.hourcount} hours.

Checkout the event here!

- JYL Toolbox

Update email notifications (#settings)
                    '''

                    with app.app_context():
                        with mail.connect() as conn:
                            for user in users:
                                if user.eventAlertoneweek:
                                    msg = Message(
                                        f'{event.name} in 1 week! - JYL Toolbox',
                                        recipients=[
                                            user.email])
                                    msg.body = text
                                    msg.html = html

                                    conn.send(msg)

                        event.alertoneweek = True
                        db.session.commit()

                elif eventDelta == 3 and event.alertthreeday is False:

                    eventTime = event.start.strftime(
                        '%A %B %-d %Y at %-I:%M %p')
                    eventLocation = event.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having {event.name} in three days on <strong>{eventTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{eventLocation}">{event.location}</a> for {event.hourcount} hours.</p>

<p>Checkout the event <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>

<a href="#">Update email notifications</a>
                    '''

                    text = f'''
Hello,

JYL is having {event.name} in three days on {eventTime}.

It will be at {event.location} for {event.hourcount} hours.

Checkout the event here!

- JYL Toolbox

Update email notifications (#settings)
                    '''

                    with app.app_context():
                        with mail.connect() as conn:
                            for user in users:
                                if user.eventAlertoneweek:
                                    msg = Message(
                                        f'{event.name} in 3 days! - JYL Toolbox',
                                        recipients=[
                                            user.email])
                                    msg.body = text
                                    msg.html = html

                                    conn.send(msg)

                        event.alertthreeday = True
                        db.session.commit()

                elif eventDelta == 1 and event.alertoneday is False:

                    eventTime = event.start.strftime(
                        '%A %B %-d %Y at %-I:%M %p')
                    eventLocation = event.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having {event.name} in one day on <strong>{eventTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{eventLocation}">{event.location}</a> for {event.hourcount} hours.</p>

<p>Checkout the event <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>

<a href="#">Update email notifications</a>
                    '''

                    text = f'''
Hello,

JYL is having {event.name} in one day on {eventTime}.

It will be at {event.location} for {event.hourcount} hours.

Checkout the event here!

- JYL Toolbox

Update email notifications (#settings)
                    '''

                    with app.app_context():
                        with mail.connect() as conn:
                            for user in users:
                                if user.eventAlertoneweek:
                                    msg = Message(
                                        f'{event.name} in 1 day! - JYL Toolbox',
                                        recipients=[
                                            user.email])
                                    msg.body = text
                                    msg.html = html

                                    conn.send(msg)

                        event.alertoneday = True
                        db.session.commit()

'''
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=backgroundCheck,
    trigger=IntervalTrigger(minutes=60),
    id='background_check',
    name='Server Check',
    replace_existing=True)

# Shut down the scheduler when exiting the app
register(lambda: scheduler.shutdown())
'''