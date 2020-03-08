from jyl import db
from jyl.models import Meeting, UserMeeting


def meetingProccessing(checkMeeting):

    meetingData = {}

    users = UserMeeting.query.filter_by(userid=checkMeeting.id, attended=True).all()

    length = checkMeeting.hourcount

    meetingData['usersAttended'] = []
    meetingData['totalHours'] = 0

    for people in users:

        if people.attended or people.going:
            meetingData['usersAttended'].append(people)
            meetingData['totalHours'] += length

    return meetingData