from jyl import app, forms, db, bcrypt
from flask import render_template, redirect, url_for, request, flash, make_response, send_file
from jyl.models import User, Meeting, Event
from jyl.profile import profileProccessing
from jyl.helpers import sendoff, cookieSwitch
from flask_login import current_user, login_required
from jyl.eventMeeting import eventMeetingProccessing


'''
Views
'''
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
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


@app.route('/back', methods=['GET'])
def back():

    siteCookies = request.cookies

    if 'page' in siteCookies:

        page = siteCookies['page']

        if 'profile' in page:
            num = int(siteCookies['profile-num'])
            first = siteCookies['profile-first']
            last = siteCookies['profile-last']
            return redirect(url_for('profile', num=num, first=first, last=last))

        elif 'meeting' in page:
            meetingId = int(siteCookies['meeting-id'])
            return redirect(url_for('meetingInfo', idOfMeeting=meetingId))

        elif 'event' in page:
            eventId = int(siteCookies['event-id'])
            return redirect(url_for('eventInfo', idOfEvent=eventId))

        elif 'memberType' in page:
            memberType = siteCookies['memberType']
            return redirect(url_for('memberType', identifier=memberType))

        return redirect(url_for(page))

    else:
        return redirect(url_for('index'))


@app.route('/profile/<int:num>/<first>/<last>', methods=['GET'])
@login_required
def profile(num, first, last):

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
        profileData=profileData,
        user=checkUser))

    page = cookieSwitch(page)

    num = repr(num)

    page.set_cookie('current', 'profile', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-last-current', last, max_age=60 * 60 * 24 * 365)
    return page


@app.route('/meeting/<int:idOfMeeting>', methods=['GET'])
@login_required
def meetingInfo(idOfMeeting):

    checkMeeting = Meeting.query.filter_by(id=idOfMeeting).first()

    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    eventMeeting = eventMeetingProccessing(checkMeeting, meeting=True)

    page = make_response(render_template(
        'eventMeeting.html', eventMeeting=checkMeeting, eventMeetingData=eventMeeting))

    page = cookieSwitch(page)

    idOfMeeting = repr(idOfMeeting)

    page.set_cookie('current', 'meeting', max_age=60 * 60 * 24 * 365)
    page.set_cookie('meeting-id-current', idOfMeeting, max_age=60 * 60 * 24 * 365)
    return page


@app.route('/create', methods=['GET'])
@login_required
def creation():

    if current_user.leader or current_user.admin:

        return render_template('leaderDashboard.html', create=True)

    flash('Must be a Leader or Admin')
    return sendoff('index')

@app.route('/create/user', methods=['GET', 'POST'])
@login_required
def userCreation():

    if current_user.leader or current_user.admin:

        return render_template('userEdit.html', create=True)

    flash('Must be a Leader or Admin')
    return sendoff('index')

@app.route('/create/event', methods=['GET', 'POST'])

@app.route('/create/meeting', methods=['GET', 'POST'])

@app.route('/edit', methods=['GET'])
@login_required
def modification():

    if current_user.leader or current_user.admin:

        return render_template('leaderDashboard.html', create=False)

    flash('Must be a Leader or Admin')
    return sendoff('index')

@app.route('/edit/user', methods=['GET'])

@app.route('/edit/user/<int:userId>', methods=['GET', 'POST'])

@app.route('/edit/event', methods=['GET'])

@app.route('/edit/event/<int:eventId>', methods=['GET', 'POST'])

@app.route('/edit/meeting', methods=['GET'])

@app.route('/edit/meeting/<int:meetingId>', methods=['GET', 'POST'])

@app.route('/event/<int:idOfEvent>', methods=['GET'])
@login_required
def eventInfo(idOfEvent):

    checkEvent = Event.query.filter_by(id=idOfEvent).first()

    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    eventMeeting = eventMeetingProccessing(checkEvent, meeting=False)

    page = make_response(render_template(
        'eventMeeting.html', eventMeeting=checkEvent, eventMeetingData=eventMeeting))

    page = cookieSwitch(page)

    idOfEvent = repr(idOfEvent)

    page.set_cookie('current', 'event', max_age=60 * 60 * 24 * 365)
    page.set_cookie('event-id-current', idOfEvent, max_age=60 * 60 * 24 * 365)
    return page


@app.route('/members', methods=['GET'])
@login_required
def members():
    
    members = User.query.order_by('lastname').all()

    page = make_response(render_template(
        'members.html', members=members, identifier=False, indentify=''))

    page = cookieSwitch(page)

    page.set_cookie('current', 'members', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/members/<identifier>', methods=['GET'])
def memberType(identifier):
    
    members = User.query.order_by('lastname').all()

    eligibleMembers = []

    if identifier == 'Admin':
        for user in members:
            if user.admin:
                eligibleMembers.append(user)

    elif identifier == 'Leader':
        for user in members:
            if user.leader:
                eligibleMembers.append(user)
                
    else:
        flash(f'No users in this catagory {indentifier}', 'warning')
        return sendoff('members')

    page = make_response(render_template(
        'members.html', members=eligibleMembers, identifier=True, indentify=identifier))

    page = cookieSwitch(page)

    page.set_cookie('current', 'membersType', max_age=60 * 60 * 24 * 365)
    page.set_cookie('membertype-current', identifier, max_age=60 * 60 * 24 * 365)
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
