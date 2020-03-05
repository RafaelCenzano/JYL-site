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
    if 'current' in request.cookies:
        page = request.cookies['current']
        if 'profile' in page:
            num = request.cookies['profile-num']
            first = request.cookies['profile-first']
            last = request.cookies['profile-last']
            return redirect(url_for('profile', num=num, first=first, last=last))
        elif 'meeting' in page:
            meetingid = request.cookies['meeting-id']
            return redirect(url_for('meeting', idOfMeeting=meetingid))
        return redirect(url_for(page))
    return redirect(url_for(where))


def cookieSwitch(page):
    if 'current' in request.cookies:
        current = request.cookies['current']
        page.set_cookie('page', current, max_age=60 * 60 * 24 * 365)

    if 'profile-num-current' in request.cookies:
        current_num = request.cookies['profile-num-current']
        current_first = request.cookies['profile-first-current']
        current_last = request.cookies['profile-last-current']
        page.set_cookie('profile-num', current_num, max_age=60 * 60 * 24 * 365)
        page.set_cookie('profile-first', current_first, max_age=60 * 60 * 24 * 365)
        page.set_cookie('profile-last', current_last, max_age=60 * 60 * 24 * 365)

    if 'meeting-id-current' in request.cookies:
        current_meeting = request.cookies['meeting-id-current']
        page.set_cookie('meeting-id', current_meeting, max_age=60 * 60 * 24 * 365)

    return page