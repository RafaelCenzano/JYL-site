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
        return redirect(url_for(page))
    return redirect(url_for(where))