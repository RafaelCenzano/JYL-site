from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from flask_mail import Mail, Message
from datetime import datetime
from jyl.models import *
from flask import url_for
from pytz import timezone
from jyl import db


pacific = timezone('US/Pacific')


def backgroundCheck():
    meetings = Meeting.query.filter_by(currentYear=True).all()
    events = Event.query.filter_by(currentYear=True).all()
    users = User.query.filter_by(currentmember=True, leader=False).all()
    groups = Group.query.filter_by(currentYear=True).all()
    audits = YearAudit.query.filter_by(confirmed=True, completed=False).all()

    now = pacific.localize(datetime.now())

    if audits:
        for audit in audits:
            if (now - pacific.localize(audit.time)).days >= 7:

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

    if meetings:
        for meeting in meetings:
            meetingDate = pacific.localize(meeting.start)
            if meetingDate > now:
                meetingDelta = (now - meetingDate).days
                if meetingDelta == 7 and meeting.alertoneweek == False:
                    
                    meetingTime = meeting.start.strftime('%A %B %-d %Y at %-I:%-M %p')
                    meetingLocation = meeting.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having a meeting in a week on <strong>{meetingTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{meetingLocation}">{meeting.location}</a> for {meeting.hourcount} hours.</p>

<p>Checkout the meeting <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>
                    '''

                    text = f'''
Hello,

JYL is having a meeting in a week on {meetingTime}.

It will be at {meeting.location} for {meeting.hourcount} hours.

Checkout the meeting here!

- JYL Toolbox
                    '''
                    recipients = []
                    for user in users:
                        if user.meetingAlertoneweek:
                            recipients.append(user.email)

                    '''
                    with mail.connect() as conn:
                        for recipient in recipients:
                            msg = Message('Meeting in 1 week! - JYL Toolbox',
                              recipients=recipient)
                            msg.body = text
                            msg.html = html

                            conn.send(msg)
                    '''

                    meeting.alertoneweek = True
                    db.session.commit()

                elif meetingDelta == 3 and meeting.alertthreeday == False:
                    
                    meetingTime = meeting.start.strftime('%A %B %-d %Y at %-I:%-M %p')
                    meetingLocation = meeting.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having a meeting in three days on <strong>{meetingTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{meetingLocation}">{meeting.location}</a> for {meeting.hourcount} hours.</p>

<p>Checkout the meeting <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>
                    '''

                    text = f'''
Hello,

JYL is having a meeting in three days on {meetingTime}.

It will be at {meeting.location} for {meeting.hourcount} hours.

Checkout the meeting here!

- JYL Toolbox
                    '''
                    recipients = []
                    for user in users:
                        if user.meetingAlertthreeday:
                            recipients.append(user.email)

                    '''
                    with mail.connect() as conn:
                        for recipient in recipients:
                            msg = Message('Meeting in 3 days! - JYL Toolbox',
                              recipients=recipient)
                            msg.body = text
                            msg.html = html

                            conn.send(msg)
                    '''

                    meeting.alertthreeday = True
                    db.session.commit()

                elif meetingDelta == 1 and meeting.alertoneday == False:
                    
                    meetingTime = meeting.start.strftime('%A %B %-d %Y at %-I:%-M %p')
                    meetingLocation = meeting.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having a meeting in one day on <strong>{meetingTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{meetingLocation}">{meeting.location}</a> for {meeting.hourcount} hours.</p>

<p>Checkout the meeting <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>
                    '''

                    text = f'''
Hello,

JYL is having a meeting in one day on {meetingTime}.

It will be at {meeting.location} for {meeting.hourcount} hours.

Checkout the meeting here!

- JYL Toolbox
                    '''
                    recipients = []
                    for user in users:
                        if user.meetingAlertoneday:
                            recipients.append(user.email)

                    '''
                    with mail.connect() as conn:
                        for recipient in recipients:
                            msg = Message('Meeting in 3 days! - JYL Toolbox',
                              recipients=recipient)
                            msg.body = text
                            msg.html = html

                            conn.send(msg)
                    '''

                    meeting.alertoneday = True
                    db.session.commit()

    if events:
        for event in events:
            eventDate = pacific.localize(event.start)
            if eventDate > now:
                eventDelta = (now - eventDate).days
                if eventDelta == 7 and event.alertoneweek == False:
                    
                    eventTime = event.start.strftime('%A %B %-d %Y at %-I:%-M %p')
                    eventLocation = event.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having {event.name} in a week on <strong>{eventTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{eventLocation}">{event.location}</a> for {event.hourcount} hours.</p>

<p>Checkout the event <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>
                    '''

                    text = f'''
Hello,

JYL is having {event.name} in a week on {eventTime}.

It will be at {event.location} for {event.hourcount} hours.

Checkout the event here!

- JYL Toolbox
                    '''
                    recipients = []
                    for user in users:
                        if user.eventAlertoneweek:
                            recipients.append(user.email)

                    '''
                    with mail.connect() as conn:
                        for recipient in recipients:
                            msg = Message(f'{event.name} in 1 week! - JYL Toolbox',
                              recipients=recipient)
                            msg.body = text
                            msg.html = html

                            conn.send(msg)
                    '''

                    event.alertoneweek = True
                    db.session.commit()

                elif eventDelta == 3 and event.alertthreeday == False:
                    
                    eventTime = event.start.strftime('%A %B %-d %Y at %-I:%-M %p')
                    eventLocation = event.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having {event.name} in three days on <strong>{eventTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{eventLocation}">{event.location}</a> for {event.hourcount} hours.</p>

<p>Checkout the event <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>
                    '''

                    text = f'''
Hello,

JYL is having {event.name} in three days on {eventTime}.

It will be at {event.location} for {event.hourcount} hours.

Checkout the event here!

- JYL Toolbox
                    '''
                    recipients = []
                    for user in users:
                        if user.eventAlertthreeday:
                            recipients.append(user.email)

                    '''
                    with mail.connect() as conn:
                        for recipient in recipients:
                            msg = Message(f'{event.name} in 3 days! - JYL Toolbox',
                              recipients=recipient)
                            msg.body = text
                            msg.html = html

                            conn.send(msg)
                    '''

                    event.alertthreeday = True
                    db.session.commit()

                elif eventDelta == 1 and event.alertoneday == False:
                    
                    eventTime = event.start.strftime('%A %B %-d %Y at %-I:%-M %p')
                    eventLocation = event.location.replace(' ', '+')

                    html = f'''
<p>Hello,</p>

<p>JYL is having {event.name} in one day on <strong>{eventTime}</strong>.</p>

<p>It will be at <a href="https://www.google.com/maps/place/{eventLocation}">{event.location}</a> for {event.hourcount} hours.</p>

<p>Checkout the event <a href="#">here</a>!</p>

<p>- <a href="#">JYL Toolbox</a></p>
                    '''

                    text = f'''
Hello,

JYL is having {event.name} in one day on {eventTime}.

It will be at {event.location} for {event.hourcount} hours.

Checkout the event here!

- JYL Toolbox
                    '''
                    recipients = []
                    for user in users:
                        if user.eventAlertoneday:
                            recipients.append(user.email)

                    '''
                    with mail.connect() as conn:
                        for recipient in recipients:
                            msg = Message(f'{event.name} in 3 days! - JYL Toolbox',
                              recipients=recipient)
                            msg.body = text
                            msg.html = html

                            conn.send(msg)
                    '''

                    event.alertoneday = True
                    db.session.commit()


# create schedule for printing time
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=backgroundCheck,
    trigger=IntervalTrigger(minutes=5),
    id='background_check',
    name='Server Check',
    replace_existing=True)

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())