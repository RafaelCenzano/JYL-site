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