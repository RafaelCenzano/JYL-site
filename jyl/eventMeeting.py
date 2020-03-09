from jyl import db
from datetime import datetime
from jyl.models import Meeting, UserMeeting, Event, UserEvent


def eventMeetingProccessing(check, meeting=True):

    eventMeeting = {}

    if check.start > datetime.now():

        if meeting:
            users = UserMeeting.query.filter_by(userid=check.id, going=True).all()
            eventMeeting['meeting'] = True
        else:
            users = UserEvent.query.filter_by(userid=check.id, going=True).all()
            eventMeeting['meeting'] = False

        eventMeeting['future'] = True

    else:

        if meeting:
            users = UserMeeting.query.filter_by(userid=check.id, attended=True).all()
            eventMeeting['meeting'] = True
        else:
            users = UserEvent.query.filter_by(userid=check.id, attended=True).all()
            eventMeeting['meeting'] = False

        eventMeeting['future'] = False

    length = check.hourcount

    eventMeeting['users'] = []
    eventMeeting['totalHours'] = 0

    for user in users:

        if user.attended or user.going:
            meetingData['users'].append(user)
            meetingData['totalHours'] += length

    return eventMeeting