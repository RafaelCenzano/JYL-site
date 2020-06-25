from jyl import db
from datetime import datetime
from jyl.models import Meeting, UserMeeting, Event, UserEvent, User
from flask_login import login_user, current_user


def eventMeetingProccessing(check, meeting):

    eventMeeting = {}

    if check.start > datetime.now():

        eventMeeting['future'] = True

    else:

        eventMeeting['future'] = False

    if meeting:
        users = UserMeeting.query.filter_by(
            meetingid=check.id, attended=True).all()
        eventMeeting['meeting'] = True
    else:
        users = UserEvent.query.filter_by(
            eventid=check.id, attended=True).all()
        eventMeeting['meeting'] = False

    eventMeeting['userreview'] = []
    eventMeeting['userreviewwho'] = []
    eventMeeting['users'] = []
    eventMeeting['userReview'] = False
    eventMeeting['userAttended'] = False

    if eventMeeting['future']:

        if meeting:
            users = UserMeeting.query.filter_by(meetingid=check.id, going=True).all()

            for user in users:
                eventMeeting['users'].append(user)

        else:
            users = UserEvent.query.filter_by(eventid=check.id, going=True).all()

            for user in users:
                eventMeeting['users'].append(user)

    else:
        for user in users:

            if current_user.id == user.userid:
                eventMeeting['userAttended'] = True

            if user.comment is not None:
                if user.userid == current_user.id:
                    eventMeeting['userReview'] = True
                eventMeeting['userreview'].append(user)
                theUser = User.query.get(user.userid)
                eventMeeting['userreviewwho'].append(theUser)
                eventMeeting['users'].append(theUser)
            else:
                eventMeeting['users'].append(User.query.get(user.userid))

    eventMeeting['users'].sort(key=lambda user: user.lastname.lower())

    return eventMeeting
