from jyl import app, forms, db, bcrypt
from flask import render_template, redirect, url_for, request, flash, make_response, send_file
from flask_login import current_user
from jyl.models import User
from jyl.profile import profileProccessing
from jyl.helpers import sendoff, cookieSwitch


'''
Views
'''
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/home/', methods=['GET'])
def index():

    page = make_response(render_template('home.html'))

    page = cookieSwitch(page)

    page.set_cookie('current', 'index', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/license', methods=['GET'])
@app.route('/license/', methods=['GET'])
def license():

    page = make_response(render_template('license.html'))

    page = cookieSwitch(page)

    page.set_cookie('current', 'license', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/back')
@app.route('/back/')
def back():

    if 'page' in request.cookies:
        page = request.cookies['page']
        if 'profile' in page:
            num = request.cookies['profile-num']
            first = request.cookies['profile-first']
            last = request.cookies['profile-last']
            return redirect(url_for('profile', num=num, first=first, last=last))
        elif 'meeting' in page:
            meetingid = request.cookies['meeting-id']
            return redirect(url_for('meeting', idOfMeeting=meetingid))
        return redirect(url_for(page))

    else:
        return redirect(url_for('index'))


@app.route('/profile/<num>/<first>/<last>/')
def profile(num, first, last):

    if not current_user.is_authenticated:
        flash('Must be logged in to view a profile', 'warning')
        return sendoff('login'), 403

    try:
        int(num)
        isInt = False

    except ValueError:
        isInt = True

    if isInt or first is None or last is None:

        flash('User not found', 'error')
        return sendoff('index'), 404

    checkUser = User.query.filter_by(
        firstname=first,
        lastname=last,
        namecount=num).first()

    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    profileData = profileProccessing(checkUser)

    page = make_response(render_template(
        'profile.html',
        meetingsPresent=profileData['meetingsPresent'],
        eventsPresent=profileData['eventsPresent'],
        recentMeetingsAttended=profileData['recentMeetingsAttended'],
        recentEventsAttended=profileData['recentEventsAttended'],
        meetingHours=profileData['meetingHours'],
        eventHours=profileData['eventHours'],
        user=checkUser))

    page = cookieSwitch(page)

    page.set_cookie('current', 'profile', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-last-current', last, max_age=60 * 60 * 24 * 365)
    return page


@app.route('/meeting/<idOfMeeting>/')
def meetingInfo(idOfMeeting):

    if not current_user.is_authenticated:
        flash('Must be logged in to view a meeting', 'warning')
        return sendoff('login'), 403

    try:
        int(idOfMeeting)

    except ValueError:
        flash('Meeting not found', 'error')
        return sendoff('index'), 404

    checkMeeting = Meeting.query.filter_by(id=idOfMeeting).first()

    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    page = make_response(render_template(
        'meeting.html', meeting=checkMeeting))

    page = cookieSwitch(page)

    page.set_cookie('current', 'meeting', max_age=60 * 60 * 24 * 365)
    page.set_cookie('meeting-id-current', idOfMeeting, max_age=60 * 60 * 24 * 365)
    return page


@app.route('/robots.txt', methods=['GET'])
def robots():
    return send_file('templates/seo/robots.txt')


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    sitemap_xml = render_template('seo/sitemap.xml')
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response
    

'''
Error Handlers
'''

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_for_server(e):
    return render_template('500.html')
