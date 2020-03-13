from jyl.models import User
from jyl import login_manager
from flask import redirect, url_for, request


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except BaseException:
        return None


def sendoff(where):
    siteCookies = request.cookies

    if 'current' in siteCookies:
        currentCookie = siteCookies['current']

        if 'profile' in currentCookie:
            num = siteCookies['profile-num']
            first = siteCookies['profile-first']
            last = siteCookies['profile-last']
            return redirect(url_for('profile', num=num, first=first, last=last))

        elif 'meeting' in currentCookie:
            meetingid = siteCookies['meeting-id']
            return redirect(url_for('meetingInfo', idOfMeeting=meetingid))

        elif 'event' in currentCookie:
            eventid = siteCookies['event-id']
            return redirect(url_for('eventInfo', idOfEvent=eventid))

        elif 'membersType' in currentCookie:
            memberType = siteCookies['membertype']
            return redirect(url_for('memberType', indentifier=memberType))

        return redirect(url_for(currentCookie))
    return redirect(url_for(where))


def cookieSwitch(pageItem):
    siteCookies = request.cookies

    if 'current' in siteCookies:
        current = siteCookies['current']
        pageItem.set_cookie('page', current, max_age=60 * 60 * 24 * 365)

    if 'profile-num-current' in siteCookies:
        currentNum = siteCookies['profile-num-current']
        currentFirst = siteCookies['profile-first-current']
        currentLast = siteCookies['profile-last-current']
        pageItem.set_cookie('profile-num', currentNum, max_age=60 * 60 * 24 * 365)
        pageItem.set_cookie('profile-first', currentFirst, max_age=60 * 60 * 24 * 365)
        pageItem.set_cookie('profile-last', currentLast, max_age=60 * 60 * 24 * 365)

    if 'meeting-id-current' in siteCookies:
        currentMeeting = siteCookies['meeting-id-current']
        pageItem.set_cookie('meeting-id', currentMeeting, max_age=60 * 60 * 24 * 365)

    if 'event-id-current' in siteCookies:
        currentEvent = siteCookies['event-id-current']
        pageItem.set_cookie('event-id', currentEvent, max_age=60 * 60 * 24 * 365)

    if 'membertype-current' in siteCookies:
        currentMemberType = siteCookies['membertype-current']
        pageItem.set_cookie('membertype', currentMemberType, max_age=60 * 60 * 24 * 365)

    return pageItem