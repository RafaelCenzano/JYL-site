import datetime
from jyl import app, forms, db, bcrypt
from flask import render_template, redirect, url_for, request, flash, make_response, send_file
from random import randint
from hashlib import sha256
from jyl.forms import CreateUser
from jyl.models import *
from jyl.helpers import sendoff, cookieSwitch, cleanValue
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
            if siteCookies['profile-type'] == 'normal':
                return redirect(url_for('profile', num=num, first=first, last=last))
            elif siteCookies['profile-type'] == 'meeting':
                return redirect(url_for('profileMeeting', num=num, first=first, last=last))
            return redirect(url_for('profileEvent', num=num, first=first, last=last))

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

    page = make_response(render_template(
        'profile.html',
        user=checkUser,
        lifetimeHours=cleanValue(checkUser.lifetimeHours),
        currentHours=cleanValue(checkUser.currentHours),
        currentMeetingHours=cleanValue(checkUser.currentMeetingHours),
        currentEventHours=cleanValue(checkUser.currentEventHours)))

    page = cookieSwitch(page)

    num = repr(num)

    page.set_cookie('current', 'profile', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-last-current', last, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-type-current', 'normal', max_age=60 * 60 * 24 * 365)
    return page

@app.route('/profile/<int:num>/<first>/<last>/meetings', methods=['GET'])
@login_required
def profileMeeting(num, first, last):

    checkUser = User.query.filter_by(
        firstname=first,
        lastname=last,
        namecount=num).first()

    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    attended = UserMeeting.query.filter_by(userid=checkUser.id, attended=True, currentYear=True).all()
    going = UserMeeting.query.filter_by(userid=checkUser.id, going=True, attended=False, currentYear=True).all()

    meetingsAttended = []

    for meetings in attended:
        meetingsAttended.append(Meeting.query.get(meetings.meetingid))

    meetingsGoing = []

    for meetings in going:
        theMeeting = Meeting.query.get(meetings.meetingid)
        if theMeeting.start > datetime.datetime.now():
            meetingsGoing.append(theMeeting)

    page = make_response(render_template(
        'userEventMeeting.html',
        user=checkUser,
        itemsAttended=meetingsAttended,
        itemsGoing=meetingsGoing,
        attendedLen=len(meetingsAttended),
        goingLen=len(meetingsGoing),
        event=False,
        lifetimeHours=cleanValue(checkUser.lifetimeMeetingHours),
        currentHours=cleanValue(checkUser.currentMeetingHours)))

    page = cookieSwitch(page)

    num = repr(num)

    page.set_cookie('current', 'profileMeeting', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-last-current', last, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-type-current', 'meeting', max_age=60 * 60 * 24 * 365)
    return page

@app.route('/profile/<int:num>/<first>/<last>/events', methods=['GET'])
@login_required
def profileEvent(num, first, last):

    checkUser = User.query.filter_by(
        firstname=first,
        lastname=last,
        namecount=num).first()

    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    attended = UserEvent.query.filter_by(userid=checkUser.id, attended=True, currentYear=True).all()
    going = UserEvent.query.filter_by(userid=checkUser.id, going=True, attended=False, currentYear=True).all()

    eventsAttended = []

    for events in attended:
        eventsAttended.append(Event.query.get(events.eventid))

    eventsGoing = []

    for events in going:
        theEvent = Event.query.get(events.eventid)
        if theEvent.start > datetime.datetime.now():
            eventsGoing.append(theEvent)

    page = make_response(render_template(
        'userEventMeeting.html',
        user=checkUser,
        itemsAttended=eventsAttended,
        itemsGoing=eventsGoing,
        attendedLen=len(eventsAttended),
        goingLen=len(eventsGoing),
        event=True,
        lifetimeHours=cleanValue(checkUser.lifetimeEventHours),
        currentHours=cleanValue(checkUser.currentEventHours)))

    page = cookieSwitch(page)

    num = repr(num)

    page.set_cookie('current', 'profileEvent', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-type-current', 'event', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/meeting/<int:idOfMeeting>', methods=['GET'])
@login_required
def meetingInfo(idOfMeeting):

    checkMeeting = Meeting.query.get(idOfMeeting)

    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    eventMeeting = eventMeetingProccessing(checkMeeting, meeting=True)

    page = make_response(render_template(
        'eventMeeting.html', eventMeeting=checkMeeting, eventMeetingData=eventMeeting, hourcount=cleanValue(checkMeeting.hourcount)))

    page = cookieSwitch(page)

    idOfMeeting = repr(idOfMeeting)

    page.set_cookie('current', 'meeting', max_age=60 * 60 * 24 * 365)
    page.set_cookie('meeting-id-current', idOfMeeting, max_age=60 * 60 * 24 * 365)
    return page


@app.route('/create', methods=['GET'])
@login_required
def creation():

    if current_user.leader or current_user.admin:

        page = make_response(render_template('leaderDashboard.html', create=True))
        page = cookieSwitch(page)
        page.set_cookie('current', 'creation', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/create/user', methods=['GET', 'POST'])
@login_required
def userCreation():

    if current_user.leader or current_user.admin:

        form = CreateUser()

        if form.validate_on_submit():

            try:

                samename = User.query.filter_by(firstname=form.first.data, lastname=form.lastname.data).all()

                passNum = randint(100000, 999999)

                tempPass = bcrypt.generate_password_hash(sha256(
                            (passNum +
                             form.email.data +
                             app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')

                newUser = User(
                    firstname=form.first.data,
                    lastname=form.last.data,
                    email=form.email.data,
                    password=tempPass,
                    lifetimeHours=0.0,
                    lifetimeMeetingHours=0.0,
                    lifetimeEventHours=0.0,
                    lifetimeMeetingCount=0,
                    lifetimeEventCount=0,
                    currentHours=0.0,
                    currentMeetingHours=0.0,
                    currentEventHours=0.0,
                    currentMeetingCount=0,
                    currentEventCount=0,
                    nickname=None,
                    nicknameapprove=False,
                    admin=form.admin.data,
                    leader=form.leader.data,
                    namecount=len(samename),
                    school=form.school.data,
                    grade=form.grade.data,
                    currentmember=True,
                    bio=None)

                db.session.add(newUser)
                db.session.commit()
                flash(f'User created for {form.first.data} {form.last.data}', 'success')

            except BaseException as e:
                flash(f'User couldn\'t be created. Error: {e}', 'error')
                
            return(url_for('creation'))

        page = make_response(render_template('userCreate.html', form=form))
        page = cookieSwitch(page)
        page.set_cookie('current', 'userCreation', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/create/event', methods=['GET', 'POST'])
@login_required
def eventCreation():

    if current_user.leader or current_user.admin:

        form = CreateEvent()

        if form.validate_on_submit():

            try:

                newEvent = Event()

                db.session.add(newEvent)
                db.session.commit()

                flash(f'Event "{form.name.data}" created', 'success')

            except BaseException as e:
                flash(f'Event couldn\'t be created. Error: {e}', 'error')
            
            return(url_for('creation'))

        page = make_response(render_template('eventCreate.html', form=form))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventCreation', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/create/meeting', methods=['GET', 'POST'])


@app.route('/edit', methods=['GET'])
@login_required
def modification():

    if current_user.leader or current_user.admin:

        page = make_response(render_template('leaderDashboard.html', create=False))
        page = cookieSwitch(page)
        page.set_cookie('current', 'modification', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
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

    checkEvent = Event.query.get(idOfEvent)

    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    eventMeeting = eventMeetingProccessing(checkEvent, meeting=False)

    page = make_response(render_template(
        'eventMeeting.html', eventMeeting=checkEvent, eventMeetingData=eventMeeting, hourcount=cleanValue(checkEvent.hourcount)))

    page = cookieSwitch(page)

    idOfEvent = repr(idOfEvent)

    page.set_cookie('current', 'event', max_age=60 * 60 * 24 * 365)
    page.set_cookie('event-id-current', idOfEvent, max_age=60 * 60 * 24 * 365)
    return page


@app.route('/members', methods=['GET'])
@login_required
def members():
    
    currentMembers = User.query.filter_by(currentmember=True).order_by('lastname').all()
    oldMembers = User.query.filter_by(currentmember=False).order_by('lastname').all()

    page = make_response(render_template(
        'members.html', currentMembers=currentMembers, oldMembers=oldMembers, identifier=False, indentify='', oldthings=len(oldMembers)))

    page = cookieSwitch(page)

    page.set_cookie('current', 'members', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/members/<identifier>', methods=['GET'])
@login_required
def memberType(identifier):

    if identifier == 'Admin':
        currentMembers = User.query.filter_by(admin=True, currentmember=True).order_by('lastname').all()
        oldMembers = User.query.filter_by(admin=True, currentmember=False).order_by('lastname').all()

    elif identifier == 'Leader':
        currentMembers = User.query.filter_by(leader=True, currentmember=True).order_by('lastname').all()
        oldMembers = User.query.filter_by(leader=True, currentmember=False).order_by('lastname').all()
                
    else:
        flash(f'No users in this catagory {identifier}', 'warning')
        return sendoff('members')

    page = make_response(render_template(
        'members.html', currentMembers=currentMembers, oldMembers=oldMembers, identifier=True, indentify=identifier, oldthings=len(oldMembers)))

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
