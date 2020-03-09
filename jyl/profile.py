from jyl import db
from jyl.models import User, Meeting, UserMeeting, UserEvent, Event


def profileProccessing(checkUser):

    profileData = {}

    meetings = UserMeeting.query.filter_by(userid=checkUser.id).all()
    events = UserEvent.query.filter_by(userid=checkUser.id).all()

    profileData['meetingHours'] = 0
    profileData['eventHours'] = 0

    meetingId = []
    eventId = []

    for hoursInMeetings in meetings:
        if hoursInMeetings.attended:
            hours = Meeting.query.filter_by(
                id=hoursInMeetings.meetingid).first().hourcount
            profileData['meetingHours'] += hours
            meetingId.append(hoursInMeetings.meetingid)

    for hoursInEvents in events:
        if hoursInEvents.attended:
            hours = Event.query.filter_by(
                id=hoursInEvents.eventid).first().hourcount
            profileData['eventHours'] += hours
            eventId.append(hoursInEvents.eventid)

    checkUser.hours = profileData['meetingHours'] + profileData['eventHours']

    db.session.commit()

    profileData['meetingsPresent'] = False
    profileData['eventsPresent'] = False

    recentMeetings = Meeting.query.order_by('start').all()
    profileData['recentMeetingsAttended'] = []

    recentMeetings.reverse()

    for meeting in recentMeetings:
        if meeting.id in meetingId and len(profileData['recentMeetingsAttended']) < 5:
            profileData['recentMeetingsAttended'].append(meeting)
            profileData['meetingsPresent'] = True

    recentEvents = Event.query.order_by('start').all()
    profileData['recentEventsAttended'] = []

    recentEvents.reverse()

    for event in recentEvents:
        if event.id in eventId and len(profileData['recentEventsAttended']) < 5:
            profileData['recentEventsAttended'].append(event)
            profileData['eventsPresent'] = True

    return profileData