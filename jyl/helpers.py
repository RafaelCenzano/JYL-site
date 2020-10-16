from re import search
from urllib.parse import urlparse

from flask import redirect, request, url_for
from flask_mail import Mail, Message

from jyl import login_manager, mail
from jyl.models import User

SECONDS_IN_YEAR = 60 * 60 * 24 * 365


# Load user or return None if not found
@login_manager.user_loader
def load_user(id):

    # Query for User
    try:
        user = User.query.get(int(id))
    except BaseException:
        db.session.rollback()
        user = User.query.get(int(id))

    # If user not found return None else return User object
    if user is None:
        return None

    return user


# Use saved cookies to determine where user was last
def sendoff(where):

    # Request site cookies
    siteCookies = request.cookies

    # If cookies 'current' exsists
    if 'current' in siteCookies:
        currentCookie = siteCookies['current']

        # Logic for redircting to proper profile page if profile page was the
        # last page to be used by user
        if 'profile' in currentCookie:

            # Get the namecount, first and last name for the redirect
            num = siteCookies['profile-num']
            first = siteCookies['profile-first']
            last = siteCookies['profile-last']

            # Redirect to the last profile type page user attended
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

        # Redirect to meeting
        elif 'meeting' in currentCookie:
            meetingid = siteCookies['meeting-id']
            return redirect(url_for('meetingInfo', idOfMeeting=meetingid))

        # Redirect to event
        elif 'event' in currentCookie:
            eventid = siteCookies['event-id']
            return redirect(url_for('eventInfo', idOfEvent=eventid))

        # Redirect to member list
        elif 'membersType' in currentCookie:
            memberType = siteCookies['membertype']
            return redirect(url_for('memberType', indentifier=memberType))

        # Redirect to page that doesn't require extra parameters
        return redirect(url_for(currentCookie))

    # Redirect to backup location if cookies not found
    return redirect(url_for(where))


# Update cookies
# Cookies store the current and last position
# This function moves current data to past data
def cookieSwitch(pageItem):

    # Request site cookies
    siteCookies = request.cookies

    # If there is a current cookie data move data to 'page' cookie
    if 'current' in siteCookies:
        current = siteCookies['current']
        pageItem.set_cookie('page', current, max_age=SECONDS_IN_YEAR)

    # Move data for profile cookies
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

    # Move data for meeting cookies
    if 'meeting-id-current' in siteCookies:
        currentMeeting = siteCookies['meeting-id-current']
        pageItem.set_cookie(
            'meeting-id',
            currentMeeting,
            max_age=SECONDS_IN_YEAR)

    # Move data for event cookies
    if 'event-id-current' in siteCookies:
        currentEvent = siteCookies['event-id-current']
        pageItem.set_cookie(
            'event-id',
            currentEvent,
            max_age=SECONDS_IN_YEAR)

    # Move data for member lists
    if 'membertype-current' in siteCookies:
        currentMemberType = siteCookies['membertype-current']
        pageItem.set_cookie(
            'membertype',
            currentMemberType,
            max_age=SECONDS_IN_YEAR)

    # Return flask page item
    return pageItem


# Class for formatting input text
# the class is input 1 word/url/email and saves if it as email or url
# this is used by jinja to turn text into links or clickable emails
class linkFormatting:

    def __init__(self, s):
        self.text = s
        self.url = False
        self.email = False

        # Find if string is a url
        urlCheck = urlparse(s)
        if urlCheck.scheme and urlCheck.netloc:
            self.url = True

        # User regex to determine if string is email
        emailCheck = search(r'[\w\.-]+@[\w\.-]+', s)
        if emailCheck:
            self.email = True


# Remove .0  from floats that can be an integer
def cleanValue(num):
    if num.is_integer():
        return int(num)
    return num


# Function that allows emails to be sent asyncornously to reduce page run times
def asyncEmail(app, html, text, users, subject):

    with app.app_context():
        with mail.connect() as conn:
            for user in users:
                msg = Message(subject,
                              recipients=[user.email])
                msg.body = text
                msg.html = html

                conn.send(msg)
