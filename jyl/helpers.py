from re import search
from jyl import login_manager, mail
from flask import redirect, url_for, request
from jyl.models import User
from flask_mail import Mail, Message
from urllib.parse import urlparse


SECONDS_IN_YEAR = 60 * 60 * 24 * 365


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
            if siteCookies['profile-type'] == 'normal':
                return redirect(
                    url_for(
                        'profile',
                        num=num,
                        first=first,
                        last=last))
            elif siteCookies['profile-type'] == 'meeting':
                return redirect(
                    url_for(
                        'profileMeeting',
                        num=num,
                        first=first,
                        last=last))
            elif siteCookies['profile-type'] == 'event':
                return redirect(
                    url_for(
                        'profileEvent',
                        num=num,
                        first=first,
                        last=last))
            elif siteCookies['profile-type'] == 'eventold':
                return redirect(
                    url_for(
                        'profileEventOld',
                        num=num,
                        first=first,
                        last=last))
            elif siteCookies['profile-type'] == 'meetingold':
                return redirect(
                    url_for(
                        'profileMeetingOld',
                        num=num,
                        first=first,
                        last=last))

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
        pageItem.set_cookie('page', current, max_age=SECONDS_IN_YEAR)

    if 'profile-num-current' in siteCookies:
        currentNum = siteCookies['profile-num-current']
        currentFirst = siteCookies['profile-first-current']
        currentLast = siteCookies['profile-last-current']
        currentType = siteCookies['profile-type-current']
        pageItem.set_cookie(
            'profile-num',
            currentNum,
            max_age=SECONDS_IN_YEAR)
        pageItem.set_cookie(
            'profile-first',
            currentFirst,
            max_age=SECONDS_IN_YEAR)
        pageItem.set_cookie(
            'profile-last',
            currentLast,
            max_age=SECONDS_IN_YEAR)
        pageItem.set_cookie(
            'profile-type',
            currentType,
            max_age=SECONDS_IN_YEAR)

    if 'meeting-id-current' in siteCookies:
        currentMeeting = siteCookies['meeting-id-current']
        pageItem.set_cookie(
            'meeting-id',
            currentMeeting,
            max_age=SECONDS_IN_YEAR)

    if 'event-id-current' in siteCookies:
        currentEvent = siteCookies['event-id-current']
        pageItem.set_cookie(
            'event-id',
            currentEvent,
            max_age=SECONDS_IN_YEAR)

    if 'membertype-current' in siteCookies:
        currentMemberType = siteCookies['membertype-current']
        pageItem.set_cookie(
            'membertype',
            currentMemberType,
            max_age=SECONDS_IN_YEAR)

    return pageItem


class linkFormatting:

    def __init__(self, s):
        self.text = s
        self.url = False
        self.email = False

        urlCheck = urlparse(s)
        if urlCheck.scheme and urlCheck.netloc:
            self.url = True

        emailCheck = search(r'[\w\.-]+@[\w\.-]+', s)
        if emailCheck:
            self.email = True


def cleanValue(num):
    if num.is_integer():
        return int(num)
    return num


def asyncEmail(app, html, text, users, subject):

    with app.app_context():
            with mail.connect() as conn:
                for user in users:
                    msg = Message(subject,
                                  recipients=[user.email])
                    msg.body = text
                    msg.html = html

                    conn.send(msg)

