from jyl import db
from datetime import datetime
from jyl.models import Meeting, UserMeeting, Event, UserEvent, User


def eventMeetingProccessing(check, meeting):

    eventMeeting = {}

    if check.start > datetime.now():

        eventMeeting['future'] = True

        if meeting:
            users = UserMeeting.query.filter_by(
                meetingid=check.id, going=True, attended=False).all()
            eventMeeting['meeting'] = True
        else:
            users = UserEvent.query.filter_by(
                eventid=check.id, going=True, attended=False).all()
            eventMeeting['meeting'] = False

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

        eventMeeting['future'] = False

    length = check.hourcount

    eventMeeting['userreview'] = []
    eventMeeting['userreviewwho'] = []
    eventMeeting['users'] = []

    for user in users:

        if user.comment is not None:
            eventMeeting['userreview'].append(user)
            theUser = User.query.get(user.userid)
            eventMeeting['userreviewwho'].append(theUser)
            eventMeeting['users'].append(theUser)
        else:
            eventMeeting['users'].append(User.query.get(user.userid))

    eventMeeting['users'].sort(key=lambda user: user.lastname)

    return eventMeeting
