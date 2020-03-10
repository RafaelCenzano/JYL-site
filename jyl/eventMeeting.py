from jyl import db
from datetime import datetime
from jyl.models import Meeting, UserMeeting, Event, UserEvent, User


def eventMeetingProccessing(check, meeting=True):

    eventMeeting = {}

    if check.start > datetime.now():

        if meeting:
            users = UserMeeting.query.filter_by(meetingid=check.id, going=True).all()
            eventMeeting['meeting'] = True
        else:
            users = UserEvent.query.filter_by(eventid=check.id, going=True).all()
            eventMeeting['meeting'] = False

        eventMeeting['future'] = True

    else:

        if meeting:
            users = UserMeeting.query.filter_by(meetingid=check.id, attended=True).all()
            eventMeeting['meeting'] = True
        else:
            users = UserEvent.query.filter_by(eventid=check.id, attended=True).all()
            eventMeeting['meeting'] = False

        eventMeeting['future'] = False

    length = check.hourcount

    eventMeeting['usermeeting'] = []
    eventMeeting['users'] = []
    eventMeeting['totalHours'] = 0

    for user in users:

        eventMeeting['usermeeting'].append(user)
        eventMeeting['users'].append(User.query.filter_by(id=user.userid).first())
        eventMeeting['totalHours'] += length

    return eventMeeting