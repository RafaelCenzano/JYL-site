from jyl import db
from jyl.models import Meeting, UserMeeting, Event, UserEvent


def eventMeetingProccessing(check, meeting):

    eventMeeting = {}

    users = UserMeeting.query.filter_by(userid=checkMeeting.id, attended=True).all()

    length = checkMeeting.hourcount

    eventMeeting['usersAttended'] = []
    eventMeeting['totalHours'] = 0

    for people in users:

        if people.attended or people.going:
            meetingData['usersAttended'].append(people)
            meetingData['totalHours'] += length

    return eventMeeting