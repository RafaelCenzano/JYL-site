from jyl import db
from jyl.models import User, Meeting, UserMeeting, UserEvent, Event


def profileProccessing(checkUser):

    profileData = {}

    meetings = UserMeeting.query.filter_by(userid=checkUser.id).all()
    events = UserEvent.query.filter_by(userid=checkUser.id).all()

    totalHours = 0
    profileData['meetingHours'] = 0
    profileData['eventHours'] = 0

    meetingId = []
    eventId = []

    for hoursInMeetings in meetings:
        hours = Meeting.query.filter_by(
            id=hoursInMeetings.meetingid).first().hourcount
        totalHours += hours
        profileData['meetingHours'] += hours
        meetingId.append(hoursInMeetings.meetingid)

    for hoursInEvents in events:
        hours = Event.query.filter_by(
            id=hoursInEvents.eventid).first().hourcount
        totalHours += hours
        profileData['eventHours'] += hours
        eventId.append(hoursInEvents.eventid)

    checkUser.hours = totalHours

    db.session.commit()

    recentMeetings = Meeting.query.order_by('start').all()
    profileData['recentMeetingsAttended'] = []

    recentMeetings.reverse()

    for meeting in recentMeetings:
        if meeting.id in meetingId and len(profileData['recentMeetingsAttended']) < 5:
            profileData['recentMeetingsAttended'].append(meeting)

    recentEvents = Meeting.query.order_by('start').all()
    profileData['recentEventsAttended'] = []

    recentEvents.reverse()

    for event in recentEvents:
        if event.id in eventId and len(profileData['recentEventsAttended']) < 5:
            profileData['recentEventsAttended'].append(event)

    profileData['meetingsPresent'] = True
    profileData['eventsPresent'] = True

    if len(profileData['recentMeetingsAttended']) == 0:
        profileData['meetingsPresent'] = False

    if len(profileData['recentEventsAttended']) == 0:
        profileData['eventsPresent'] = False

    return profileData