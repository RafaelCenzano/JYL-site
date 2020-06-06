from jyl import app, forms, db, bcrypt
from pytz import timezone
from flask import render_template, redirect, url_for, request, flash, make_response, send_file
from random import randint
from hashlib import sha256
from datetime import datetime
from jyl.forms import *
from jyl.models import *
from flask_mail import Mail, Message
from jyl.helpers import *
from flask_login import current_user, login_required
from jyl.eventMeeting import eventMeetingProccessing


# Timezone
pacific = timezone('US/Pacific')


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


@app.route('/bugreport', methods=['GET', 'POST'])
@login_required
def bugreport():

    form = UserRequestForm()
    if form.validate_on_submit():

        name = current_user.firstname + ' ' + current_user.lastname

        html = render_template(
            'userform_email.html',
            type='Bug Report',
            name=name,
            email=current_user.email,
            text=form.text.data)

        text = f'''
Hi,

A Bug Report for JYL Toolbox has been submitted

Name: {form.name.data}

Email: {current_user.email}

{form.text.data}

- JYL Toolbox
        '''

        '''
        recipients = User.query.filter_by(admin=True, currentmember=True, leader=False).all()

        msg = Message('Bug Report - JYL Toolbox',
          recipients=recipients)
        msg.body = text
        msg.html = html
        mail.send(msg)
        '''
        return html

        flash('Your bug report has been submitted', 'info')

        return sendoff('index')

    page = make_response(
        render_template(
            'userform.html',
            form=form,
            type='Bug Report'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'bugreport', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/request/feature', methods=['GET', 'POST'])
@login_required
def featurerequest():

    form = UserRequestForm()
    if form.validate_on_submit():

        name = current_user.firstname + ' ' + current_user.lastname

        html = render_template(
            'userform_email.html',
            type='Feature request',
            name=name,
            email=current_user.email,
            text=form.text.data)

        text = f'''
Hi,

A Feature Request for JYL Toolbox has been submitted

Name: {name}

Email: {current_user.email}

{form.text.data}

- JYL Toolbox
        '''

        '''
        recipients = User.query.filter_by(admin=True, currentmember=True, Leader=False).all()

        msg = Message('Feature Request - JYL Toolbox',
          recipients=recipients)
        msg.body = text
        msg.html = html
        mail.send(msg)
        '''

        return html

        flash('Your feature request has been submitted', 'info')

        return sendoff('index')

    page = make_response(
        render_template(
            'userform.html',
            form=form,
            type='Feature Request'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'featurerequest', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/request/help', methods=['GET', 'POST'])
@login_required
def helprequest():

    form = UserRequestForm()
    if form.validate_on_submit():

        name = current_user.firstname + ' ' + current_user.lastname

        html = render_template(
            'userform_email.html',
            type='Help Request',
            name=name,
            email=current_user.email,
            text=form.text.data)

        if current_user.nicknameapprove:

            text = f'''
Hi,

A Help Request for JYL Toolbox has been submitted

Name: {name}

Email: {current_user.email}

{form.text.data}

- JYL Toolbox
        '''

        '''
        recipients = User.query.filter_by(currentmember=True, Leader=True).all()

        msg = Message('Help Request - JYL Toolbox',
          recipients=recipients)
        msg.body = text
        msg.html = html
        mail.send(msg)
        '''

        return html

        flash('Your help request has been submitted', 'info')

        return sendoff('index')

    page = make_response(
        render_template(
            'userform.html',
            form=form,
            type='Help Request'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'helprequest', max_age=60 * 60 * 24 * 365)
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
            else:
                flash('An error occured with profile cookies', 'warning')

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
    page.set_cookie(
        'profile-type-current',
        'normal',
        max_age=60 * 60 * 24 * 365)
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

    attended = UserMeeting.query.filter_by(
        userid=checkUser.id, attended=True, currentYear=True).all()

    going = UserMeeting.query.filter_by(
        userid=checkUser.id,
        going=True,
        attended=False,
        currentYear=True).all()

    meetingsAttended = []

    for meetings in attended:
        meetingsAttended.append(Meeting.query.get(meetings.meetingid))

    meetingsGoing = []
    now = pacific.localize(datetime.now())

    for meetings in going:
        theMeeting = Meeting.query.get(meetings.meetingid)
        if pacific.localize(theMeeting.start) > now:
            meetingsGoing.append(theMeeting)

    meetingsAttended.sort(key=lambda meeting: meeting.start, reverse=True)
    meetingsGoing.sort(key=lambda meeting: meeting.start, reverse=True)

    page = make_response(render_template(
        'userEventMeeting.html',
        user=checkUser,
        itemsAttended=meetingsAttended,
        itemsGoing=meetingsGoing,
        attendedLen=len(meetingsAttended),
        goingLen=len(meetingsGoing),
        event=False,
        oldCheck=True,
        lifetimeHours=cleanValue(checkUser.lifetimeMeetingHours),
        currentHours=cleanValue(checkUser.currentMeetingHours)))

    page = cookieSwitch(page)

    num = repr(num)

    page.set_cookie('current', 'profileMeeting', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-last-current', last, max_age=60 * 60 * 24 * 365)
    page.set_cookie(
        'profile-type-current',
        'meeting',
        max_age=60 * 60 * 24 * 365)
    return page


@app.route('/profile/<int:num>/<first>/<last>/meetings/old', methods=['GET'])
@login_required
def profileMeetingOld(num, first, last):

    checkUser = User.query.filter_by(
        firstname=first,
        lastname=last,
        namecount=num).first()

    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    attended = UserMeeting.query.filter_by(
        userid=checkUser.id, attended=True).all()

    meetingsAttended = []

    for meetings in attended:
        meetingsAttended.append(Meeting.query.get(meetings.meetingid))

    meetingsAttended.sort(key=lambda meeting: meeting.start, reverse=True)

    page = make_response(render_template(
        'userEventMeeting.html',
        user=checkUser,
        itemsAttended=meetingsAttended,
        itemsGoing=[],
        attendedLen=len(meetingsAttended),
        goingLen=0,
        event=False,
        oldCheck=False,
        lifetimeHours=cleanValue(checkUser.lifetimeMeetingHours),
        currentHours=cleanValue(checkUser.currentMeetingHours)))

    page = cookieSwitch(page)

    num = repr(num)

    page.set_cookie('current', 'profileMeetingOld', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-last-current', last, max_age=60 * 60 * 24 * 365)
    page.set_cookie(
        'profile-type-current',
        'meetingold',
        max_age=60 * 60 * 24 * 365)
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

    attended = UserEvent.query.filter_by(
        userid=checkUser.id,
        attended=True,
        currentYear=True).all()
    going = UserEvent.query.filter_by(
        userid=checkUser.id,
        going=True,
        attended=False,
        currentYear=True).all()

    eventsAttended = []

    for events in attended:
        eventsAttended.append(Event.query.get(events.eventid))

    eventsGoing = []
    now = pacific.localize(datetime.now())

    for events in going:
        theEvent = Event.query.get(events.eventid)
        if pacific.localize(theEvent.start) > now:
            eventsGoing.append(theEvent)

    eventsAttended.sort(key=lambda event: event.start, reverse=True)
    eventsGoing.sort(key=lambda event: event.start, reverse=True)

    page = make_response(render_template(
        'userEventMeeting.html',
        user=checkUser,
        itemsAttended=eventsAttended,
        itemsGoing=eventsGoing,
        attendedLen=len(eventsAttended),
        goingLen=len(eventsGoing),
        event=True,
        oldCheck=True,
        lifetimeHours=cleanValue(checkUser.lifetimeEventHours),
        currentHours=cleanValue(checkUser.currentEventHours)))

    page = cookieSwitch(page)

    num = repr(num)

    page.set_cookie('current', 'profileEvent', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie(
        'profile-type-current',
        'event',
        max_age=60 * 60 * 24 * 365)
    return page


@app.route('/profile/<int:num>/<first>/<last>/events/old', methods=['GET'])
@login_required
def profileEventOld(num, first, last):

    checkUser = User.query.filter_by(
        firstname=first,
        lastname=last,
        namecount=num).first()

    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    attended = UserEvent.query.filter_by(
        userid=checkUser.id, attended=True).all()

    eventsAttended = []

    for events in attended:
        eventsAttended.append(Event.query.get(events.eventid))

    eventsAttended.sort(key=lambda event: event.start, reverse=True)

    page = make_response(render_template(
        'userEventMeeting.html',
        user=checkUser,
        itemsAttended=eventsAttended,
        itemsGoing=[],
        attendedLen=len(eventsAttended),
        goingLen=0,
        event=True,
        oldCheck=False,
        lifetimeHours=cleanValue(checkUser.lifetimeMeetingHours),
        currentHours=cleanValue(checkUser.currentMeetingHours)))

    page = cookieSwitch(page)

    num = repr(num)

    page.set_cookie('current', 'profileEventOld', max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-num-current', num, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-first-current', first, max_age=60 * 60 * 24 * 365)
    page.set_cookie('profile-last-current', last, max_age=60 * 60 * 24 * 365)
    page.set_cookie(
        'profile-type-current',
        'eventold',
        max_age=60 * 60 * 24 * 365)
    return page


@app.route('/meeting/<int:idOfMeeting>', methods=['GET'])
@login_required
def meetingInfo(idOfMeeting):

    checkMeeting = Meeting.query.get(idOfMeeting)

    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    eventMeeting = eventMeetingProccessing(checkMeeting, True)

    areyougoing = False

    if eventMeeting['future']:
        checkUserMeeting = UserMeeting.query.filter_by(
            meetingid=idOfMeeting, userid=current_user.id).first()
        if checkUserMeeting is not None and checkUserMeeting.going:
            areyougoing = True

    page = make_response(
        render_template(
            'eventMeeting.html',
            areyougoing=areyougoing,
            desc=linkFormatting(checkMeeting.description),
            eventMeeting=checkMeeting,
            eventMeetingData=eventMeeting,
            hourcount=cleanValue(
                checkMeeting.hourcount),
            reviewlen=len(
                eventMeeting['userreview'])))

    page = cookieSwitch(page)
    idOfMeeting = repr(idOfMeeting)
    page.set_cookie('current', 'meeting', max_age=60 * 60 * 24 * 365)
    page.set_cookie(
        'meeting-id-current',
        idOfMeeting,
        max_age=60 * 60 * 24 * 365)
    return page


@app.route('/leader/dashboard', methods=['GET'])
@login_required
def creation():

    if current_user.leader or current_user.admin:

        page = make_response(render_template('leaderDashboard.html'))
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

                duplicationCheck = User.query.filter_by(
                    email=form.email.data).first()

                if duplicationCheck is not None:

                    flash(f'Duplicate email found', 'error')

                    return render_template('userCreate.html', form=form)

                samename = User.query.filter_by(
                    firstname=form.first.data,
                    lastname=form.last.data).all()

                passNum = repr(randint(100000, 999999))

                tempPass = bcrypt.generate_password_hash(
                    sha256(
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
                    numberphone=None,
                    showemail=False,
                    showphone=False,
                    address=None,
                    bio=None)

                db.session.add(newUser)
                db.session.commit()
                flash(
                    f'User created for {form.first.data} {form.last.data}',
                    'success')

            except BaseException as e:
                flash(f'User couldn\'t be created. Error: {e}', 'error')

            return(redirect(url_for('creation')))

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

                length = round((form.endtime.data -
                                form.starttime.data).total_seconds() / (60 * 60), 2)
                newEvent = Event(
                    name=form.name.data,
                    start=form.starttime.data,
                    end=form.endtime.data,
                    hourcount=length,
                    description=form.description.data,
                    upvote=0,
                    unsurevote=0,
                    downvote=0,
                    location=form.location.data,
                    currentYear=True,
                    attendancecount=0)

                db.session.add(newEvent)
                db.session.commit()

                flash(f'Event "{form.name.data}" created', 'success')
                return redirect(url_for('creation'))

            except BaseException as e:
                flash(f'Event couldn\'t be created. Error: {e}', 'error')

            return(url_for('creation'))

        page = make_response(render_template('eventCreate.html', form=form))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventCreation', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/attendance/event', methods=['GET'])
def attendanceEventList():

    if current_user.leader or current_user.admin:

        currentEvents = Event.query.filter_by(currentYear=True).all()
        currentEvents.sort(key=lambda event: event.start)
        now = pacific.localize(datetime.now())

        page = make_response(
            render_template(
                'attendanceList.html',
                meeting=False,
                eventMeetings=currentEvents,
                now=now,
                pacific=pacific))
        page = cookieSwitch(page)
        page.set_cookie(
            'current',
            'attendanceEventList',
            max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/attendance/meeting', methods=['GET'])
def attendanceMeetingList():

    if current_user.leader or current_user.admin:

        currentMeetings = Meeting.query.filter_by(currentYear=True).all()
        currentMeetings.sort(key=lambda meeting: meeting.start)
        now = pacific.localize(datetime.now())

        page = make_response(
            render_template(
                'attendanceList.html',
                meeting=True,
                eventMeetings=currentMeetings,
                now=now,
                pacific=pacific))
        page = cookieSwitch(page)
        page.set_cookie(
            'current',
            'attendanceMeetingList',
            max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/attendance/meeting/<int:idOfMeeting>', methods=['GET', 'POST'])
@login_required
def meetingAttendance(idOfMeeting):

    if current_user.leader or current_user.admin:

        checkMeeting = Meeting.query.get(idOfMeeting)

        if checkMeeting is None:

            flash('Meeting not found', 'error')
            return sendoff('index')

        if pacific.localize(
                checkMeeting.start) > pacific.localize(
                datetime.now()):

            flash('Meeting hasn\'t occured yet', 'warning')
            return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

        if request.method == 'POST':

            users = User.query.filter_by(currentmember=True).all()
            users.sort(key=lambda user: user.lastname)
            count = 0

            for user in users:

                thisUser = request.form.get(
                    user.firstname +
                    user.lastname +
                    repr(
                        user.namecount))

                checkUserMeeting = UserMeeting.query.filter_by(
                    meetingid=idOfMeeting, userid=user.id).first()

                if checkUserMeeting is not None and thisUser is None:

                    checkUserMeeting.attended = False

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours -= checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingHours -= checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingCount -= 1
                    thisUserQuery.currentHours -= checkMeeting.hourcount
                    thisUserQuery.currentMeetingHours -= checkMeeting.hourcount
                    thisUserQuery.currentMeetingCount -= 1

                    db.session.commit()

                elif checkUserMeeting is not None and thisUser is not None:

                    checkUserMeeting.attended = True

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingCount += 1
                    thisUserQuery.currentHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingCount += 1

                    db.session.commit()
                    count += 1

                elif thisUser and checkUserMeeting is None:

                    newUserMeeting = UserMeeting(
                        meetingid=idOfMeeting,
                        userid=user.id,
                        attended=True,
                        going=True,
                        comment=None,
                        upvote=False,
                        unsurevote=False,
                        downvote=False,
                        currentYear=True)
                    db.session.add(newUserMeeting)

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingCount += 1
                    thisUserQuery.currentHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingCount += 1

                    db.session.commit()
                    count += 1

            checkMeeting.attendancecount = count
            db.session.commit()

            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('attendanceMeetingList'))

        users = User.query.filter_by(currentmember=True).all()
        inputs = []

        users.sort(key=lambda user: user.lastname)

        for user in users:

            checkUserMeeting = UserMeeting.query.filter_by(
                meetingid=idOfMeeting, userid=user.id).first()

            data = {}

            data['check'] = False

            if checkUserMeeting is not None and checkUserMeeting.attended:
                data['check'] = True

            data['nicknameapprove'] = user.nicknameapprove
            data['firstname'] = user.firstname
            data['lastname'] = user.lastname
            data['nickname'] = user.nickname
            data['id'] = user.firstname + user.lastname + repr(user.namecount)

            inputs.append(data)

        page = make_response(
            render_template(
                'attendance.html',
                meeting=True,
                inputs=inputs))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/meeting/<int:idOfMeeting>/attendance', methods=['GET', 'POST'])
@login_required
def meetingAttendance1(idOfMeeting):

    if current_user.leader or current_user.admin:

        checkMeeting = Meeting.query.get(idOfMeeting)

        if checkMeeting is None:

            flash('Meeting not found', 'error')
            return sendoff('index')

        if pacific.localize(
                checkMeeting.start) > pacific.localize(
                datetime.now()):

            flash('Event hasn\'t occured yet', 'warning')
            return redirect(url_for('attendanceMeetingList'))

        if request.method == 'POST':

            users = User.query.filter_by(currentmember=True).all()
            users.sort(key=lambda user: user.lastname)
            count = 0

            for user in users:

                thisUser = request.form.get(
                    user.firstname +
                    user.lastname +
                    repr(
                        user.namecount))

                checkUserMeeting = UserMeeting.query.filter_by(
                    meetingid=idOfMeeting, userid=user.id).first()

                if checkUserMeeting is not None and thisUser is None:

                    checkUserMeeting.attended = False

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours -= checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingHours -= checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingCount -= 1
                    thisUserQuery.currentHours -= checkMeeting.hourcount
                    thisUserQuery.currentMeetingHours -= checkMeeting.hourcount
                    thisUserQuery.currentMeetingCount -= 1

                    db.session.commit()

                elif checkUserMeeting is not None and thisUser is not None:

                    checkUserMeeting.attended = True

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingCount += 1
                    thisUserQuery.currentHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingCount += 1

                    db.session.commit()
                    count += 1

                elif thisUser and checkUserMeeting is None:

                    newUserMeeting = UserMeeting(
                        meetingid=idOfMeeting,
                        userid=user.id,
                        attended=True,
                        going=True,
                        comment=None,
                        upvote=False,
                        unsurevote=False,
                        downvote=False,
                        currentYear=True)
                    db.session.add(newUserMeeting)

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingCount += 1
                    thisUserQuery.currentHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingCount += 1

                    db.session.commit()
                    count += 1

            checkMeeting.attendancecount = count
            db.session.commit()

            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

        users = User.query.filter_by(currentmember=True).all()
        inputs = []

        users.sort(key=lambda user: user.lastname)

        for user in users:

            checkUserMeeting = UserMeeting.query.filter_by(
                meetingid=idOfMeeting, userid=user.id).first()

            data = {}

            data['check'] = False

            if checkUserMeeting is not None and checkUserMeeting.attended:
                data['check'] = True

            data['nicknameapprove'] = user.nicknameapprove
            data['firstname'] = user.firstname
            data['lastname'] = user.lastname
            data['nickname'] = user.nickname
            data['id'] = user.firstname + user.lastname + repr(user.namecount)

            inputs.append(data)

        page = make_response(
            render_template(
                'attendance.html',
                meeting=True,
                inputs=inputs))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/create/meeting', methods=['GET', 'POST'])
def meetingCreate():

    if current_user.leader or current_user.admin:

        form = CreateMeeting()

        if request.method == 'POST' and form.validate_on_submit():

            length = round((form.endtime.data -
                            form.starttime.data).total_seconds() / (60 * 60), 2)

            newMeeting = Meeting(
                start=form.starttime.data,
                end=form.endtime.data,
                hourcount=length,
                description=form.description.data,
                upvote=0,
                unsurevote=0,
                downvote=0,
                location=form.location.data,
                currentYear=True,
                attendancecount=0)

            db.session.add(newMeeting)
            db.session.commit()

            meetingDate = form.starttime.data.strftime('%B %-d, %Y')
            flash(f'New meeting created for {meetingDate}', 'success')
            return redirect(url_for('creation'))

        now = pacific.localize(datetime.now())

        form.starttime.data = now.replace(hour=12 + 4, minute=30, second=0)
        form.endtime.data = now.replace(hour=12 + 6, minute=0, second=0)
        form.location.data = '2012 Pine Street San Francisco CA'

        page = make_response(render_template('createMeeting.html', form=form))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/user', methods=['GET'])
def userEditList():
    return 'hello'


@app.route('/edit/user/<int:userId>', methods=['GET', 'POST'])
def userEdit(userId):
    return 'hello'


@app.route('/profile/<int:num>/<first>/<last>/edit', methods=['GET', 'POST'])
def userEdit1(num, first, last):
    return 'hello'


@app.route('/profile/<int:num>/<first>/<last>/request/nickname',
           methods=['GET', 'POST'])
def userNicknameRequest(num, first, last):
    return 'hello'


@app.route('/profile/<int:num>/<first>/<last>/nickname',
           methods=['GET', 'POST'])
def userNicknameAccept(num, first, last):
    return 'hello'


@app.route('/edit/event', methods=['GET'])
def eventEditList():

    if current_user.leader or current_user.admin:

        currentEvents = Event.query.filter_by(currentYear=True).all()

        futureEvents = []
        pastEvents = []

        now = pacific.localize(datetime.now())

        for event in currentEvents:
            if pacific.localize(event.start) > now:
                futureEvents.append(event)
            else:
                pastEvents.append(event)

        futureEvents.sort(key=lambda event: event.start)
        pastEvents.sort(key=lambda event: event.start)

        page = make_response(
            render_template(
                'eventMeetingList.html',
                meeting=False,
                futureEventMeetings=futureEvents,
                pastEventMeetings=pastEvents))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventEditList', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/event/<int:eventId>', methods=['GET', 'POST'])
@login_required
def eventEdit(eventId):

    if current_user.leader or current_user.admin:

        checkEvent = Event.query.get(eventId)

        if checkEvent is None:

            flash('Event not found', 'error')
            return sendoff('index')

        form = CreateEvent()

        if request.method == 'POST' and form.validate_on_submit():

            checkEvent.name = form.name.data
            checkEvent.description = form.description.data
            checkEvent.location = form.location.data
            checkEvent.start = form.starttime.data
            checkEvent.end = form.endtime.data

            db.session.commit()

            flash('Event edited successfully!', 'success')
            return redirect(url_for('eventEditList'))

        form.name.data = checkEvent.name
        form.description.data = checkEvent.description
        form.location.data = checkEvent.location
        form.starttime.data = checkEvent.start
        form.endtime.data = checkEvent.end

        page = make_response(render_template('editEvent.html', form=form))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/event/<int:eventId>/edit', methods=['GET', 'POST'])
@login_required
def eventEdit2(eventId):

    if current_user.leader or current_user.admin:

        checkEvent = Event.query.get(eventId)

        if checkEvent is None:

            flash('Event not found', 'error')
            return sendoff('index')

        form = CreateEvent()

        if request.method == 'POST' and form.validate_on_submit():

            checkEvent.name = form.name.data
            checkEvent.description = form.description.data
            checkEvent.location = form.location.data
            checkEvent.start = form.starttime.data
            checkEvent.end = form.endtime.data

            db.session.commit()

            flash('Event edited successfully!', 'success')
            return redirect(url_for('eventInfo', idOfEvent=eventId))

        form.name.data = checkEvent.name
        form.description.data = checkEvent.description
        form.location.data = checkEvent.location
        form.starttime.data = checkEvent.start
        form.endtime.data = checkEvent.end

        page = make_response(render_template('editEvent.html', form=form))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/event/<int:eventId>/attendance', methods=['GET', 'POST'])
@login_required
def eventAttendance(eventId):

    if current_user.leader or current_user.admin:

        checkEvent = Event.query.get(eventId)

        if checkEvent is None:

            flash('Event not found', 'error')
            return sendoff('index')

        if pacific.localize(
                checkEvent.start) > pacific.localize(
                datetime.now()):

            flash('Event hasn\'t occured yet', 'warning')
            return redirect(url_for('eventInfo', idOfEvent=eventId))

        if request.method == 'POST':

            users = User.query.filter_by(currentmember=True).all()
            users.sort(key=lambda user: user.lastname)
            count = 0

            for user in users:

                thisUser = request.form.get(
                    user.firstname +
                    user.lastname +
                    repr(
                        user.namecount))

                checkUserEvent = UserEvent.query.filter_by(
                    eventid=eventId, userid=user.id).first()

                if checkUserEvent is not None and thisUser is None:

                    checkUserEvent.attended = False

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours -= checkEvent.hourcount
                    thisUserQuery.lifetimeEventHours -= checkEvent.hourcount
                    thisUserQuery.lifetimeEventCount -= 1
                    thisUserQuery.currentHours -= checkEvent.hourcount
                    thisUserQuery.currentEventHours -= checkEvent.hourcount
                    thisUserQuery.currentEventCount -= 1

                    db.session.commit()

                elif checkUserEvent is not None and thisUser is not None:

                    checkUserEvent.attended = True

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventCount += 1
                    thisUserQuery.currentHours += checkEvent.hourcount
                    thisUserQuery.currentEventHours += checkEvent.hourcount
                    thisUserQuery.currentEventCount += 1

                    db.session.commit()
                    count += 1

                elif thisUser and checkUserEvent is None:

                    newUserEvent = UserEvent(
                        eventid=eventId,
                        userid=user.id,
                        attended=True,
                        going=True,
                        comment=None,
                        upvote=False,
                        unsurevote=False,
                        downvote=False,
                        currentYear=True)
                    db.session.add(newUserEvent)

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventCount += 1
                    thisUserQuery.currentHours += checkEvent.hourcount
                    thisUserQuery.currentEventHours += checkEvent.hourcount
                    thisUserQuery.currentEventCount += 1

                    db.session.commit()
                    count += 1

            checkEvent.attendancecount = count
            db.session.commit()

            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('eventInfo', idOfEvent=eventId))

        users = User.query.filter_by(currentmember=True).all()
        inputs = []

        users.sort(key=lambda user: user.lastname)

        for user in users:

            checkUserEvent = UserEvent.query.filter_by(
                eventid=eventId, userid=user.id).first()

            data = {}

            data['check'] = False

            if checkUserEvent is not None and checkUserEvent.attended:
                data['check'] = True

            data['nicknameapprove'] = user.nicknameapprove
            data['firstname'] = user.firstname
            data['lastname'] = user.lastname
            data['nickname'] = user.nickname
            data['id'] = user.firstname + user.lastname + repr(user.namecount)

            inputs.append(data)

        page = make_response(
            render_template(
                'attendance.html',
                meeting=False,
                inputs=inputs))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/attendance/event/<int:eventId>', methods=['GET', 'POST'])
@login_required
def eventAttendance1(eventId):

    if current_user.leader or current_user.admin:

        checkEvent = Event.query.get(eventId)

        if checkEvent is None:

            flash('Event not found', 'error')
            return sendoff('index')

        if pacific.localize(
                checkEvent.start) > pacific.localize(
                datetime.now()):

            flash('Event hasn\'t occured yet', 'warning')
            return redirect(url_for('attendanceEventList'))

        if request.method == 'POST':

            users = User.query.filter_by(currentmember=True).all()
            users.sort(key=lambda user: user.lastname)
            count = 0

            for user in users:

                thisUser = request.form.get(
                    user.firstname +
                    user.lastname +
                    repr(
                        user.namecount))

                checkUserEvent = UserEvent.query.filter_by(
                    eventid=eventId, userid=user.id).first()

                if checkUserEvent is not None and thisUser is None:

                    checkUserEvent.attended = False

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours -= checkEvent.hourcount
                    thisUserQuery.lifetimeEventHours -= checkEvent.hourcount
                    thisUserQuery.lifetimeEventCount -= 1
                    thisUserQuery.currentHours -= checkEvent.hourcount
                    thisUserQuery.currentEventHours -= checkEvent.hourcount
                    thisUserQuery.currentEventCount -= 1

                    db.session.commit()

                elif checkUserEvent is not None and thisUser is not None:

                    checkUserEvent.attended = True

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventCount += 1
                    thisUserQuery.currentHours += checkEvent.hourcount
                    thisUserQuery.currentEventHours += checkEvent.hourcount
                    thisUserQuery.currentEventCount += 1

                    db.session.commit()
                    count += 1

                elif thisUser and checkUserEvent is None:

                    newUserEvent = UserEvent(
                        eventid=eventId,
                        userid=user.id,
                        attended=True,
                        going=True,
                        comment=None,
                        upvote=False,
                        unsurevote=False,
                        downvote=False,
                        currentYear=True)
                    db.session.add(newUserEvent)

                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventCount += 1
                    thisUserQuery.currentHours += checkEvent.hourcount
                    thisUserQuery.currentEventHours += checkEvent.hourcount
                    thisUserQuery.currentEventCount += 1

                    db.session.commit()
                    count += 1

            checkEvent.attendancecount = count
            db.session.commit()

            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('attendanceEventList'))

        users = User.query.filter_by(currentmember=True).all()
        inputs = []

        users.sort(key=lambda user: user.lastname)

        for user in users:

            checkUserEvent = UserEvent.query.filter_by(
                eventid=eventId, userid=user.id).first()

            data = {}

            data['check'] = False

            if checkUserEvent is not None and checkUserEvent.attended:
                data['check'] = True

            data['nicknameapprove'] = user.nicknameapprove
            data['firstname'] = user.firstname
            data['lastname'] = user.lastname
            data['nickname'] = user.nickname
            data['id'] = user.firstname + user.lastname + repr(user.namecount)

            inputs.append(data)

        page = make_response(
            render_template(
                'attendance.html',
                meeting=False,
                inputs=inputs))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/meeting', methods=['GET'])
def meetingEditList():

    if current_user.leader or current_user.admin:

        currentMeeting = Meeting.query.filter_by(currentYear=True).all()

        futureMeetings = []
        pastMeetings = []

        now = pacific.localize(datetime.now())

        for meeting in currentMeeting:
            if pacific.localize(meeting.start) > now:
                futureMeetings.append(meeting)
            else:
                pastMeetings.append(meeting)

        futureMeetings.sort(key=lambda meeting: meeting.start)
        pastMeetings.sort(key=lambda meeting: meeting.start)

        page = make_response(
            render_template(
                'eventMeetingList.html',
                meeting=True,
                futureEventMeetings=futureMeetings,
                pastEventMeetings=pastMeetings))
        page = cookieSwitch(page)
        page.set_cookie(
            'current',
            'meetingEditList',
            max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/meeting/<int:meetingId>', methods=['GET', 'POST'])
def meetingEdit(meetingId):

    if current_user.leader or current_user.admin:

        checkMeeting = Meeting.query.get(meetingId)

        if checkMeeting is None:

            flash('Meeting not found', 'error')
            return sendoff('index')

        form = CreateMeeting()

        if request.method == 'POST' and form.validate_on_submit():

            checkMeeting.description = form.description.data
            checkMeeting.location = form.location.data
            checkMeeting.start = form.starttime.data
            checkMeeting.end = form.endtime.data

            db.session.commit()

            flash('Meeting edited successfully!', 'success')
            return redirect(url_for('meetingEditList'))

        form.description.data = checkMeeting.description
        form.location.data = checkMeeting.location
        form.starttime.data = checkMeeting.start
        form.endtime.data = checkMeeting.end

        page = make_response(render_template('editMeeting.html', form=form))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/meeting/<int:meetingId>/edit', methods=['GET', 'POST'])
def meetingEdit1(meetingId):

    if current_user.leader or current_user.admin:

        checkMeeting = Meeting.query.get(meetingId)

        if checkMeeting is None:

            flash('Meeting not found', 'error')
            return sendoff('index')

        form = CreateMeeting()

        if request.method == 'POST' and form.validate_on_submit():

            checkMeeting.description = form.description.data
            checkMeeting.location = form.location.data
            checkMeeting.start = form.starttime.data
            checkMeeting.end = form.endtime.data

            db.session.commit()

            flash('Meeting edited successfully!', 'success')
            return redirect(url_for('meetingInfo', idOfMeeting=meetingId))

        form.description.data = checkMeeting.description
        form.location.data = checkMeeting.location
        form.starttime.data = checkMeeting.start
        form.endtime.data = checkMeeting.end

        page = make_response(render_template('editMeeting.html', form=form))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/event/<int:idOfEvent>', methods=['GET'])
@login_required
def eventInfo(idOfEvent):

    checkEvent = Event.query.get(idOfEvent)

    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    eventMeeting = eventMeetingProccessing(checkEvent, False)

    areyougoing = False

    if eventMeeting['future']:
        checkUserEvent = UserEvent.query.filter_by(
            eventid=idOfEvent, userid=current_user.id).first()
        if checkUserEvent is not None and checkUserEvent.going:
            areyougoing = True

    page = make_response(
        render_template(
            'eventMeeting.html',
            areyougoing=areyougoing,
            desc=linkFormatting(checkEvent.description),
            eventMeeting=checkEvent,
            eventMeetingData=eventMeeting,
            hourcount=cleanValue(
                checkEvent.hourcount),
            reviewlen=len(
                eventMeeting['userreview'])))

    page = cookieSwitch(page)

    idOfEvent = repr(idOfEvent)

    page.set_cookie('current', 'event', max_age=60 * 60 * 24 * 365)
    page.set_cookie('event-id-current', idOfEvent, max_age=60 * 60 * 24 * 365)
    return page


@app.route('/event/<int:idOfEvent>/going', methods=['GET'])
@login_required
def eventGoing(idOfEvent):

    checkEvent = Event.query.get(idOfEvent)

    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    elif pacific.localize(checkEvent.start) <= pacific.localize(datetime.now()):

        flash('Event occured already', 'error')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    eventuser = UserEvent.query.filter_by(
        eventid=idOfEvent, userid=current_user.id).first()

    if eventuser is not None and eventuser.going:

        flash('Already showed interest in this event', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    elif eventuser is not None and eventuser.going == False:

        eventuser.going = True
        db.session.commit()
        flash('You have shown your interest in this event', 'success')

    else:

        userevent = UserEvent(
            eventid=idOfEvent,
            userid=current_user.id,
            attended=False,
            going=True,
            currentYear=True,
            upvote=False,
            unsurevote=False,
            downvote=False)
        db.session.add(userevent)
        db.session.commit()

    return redirect(url_for('eventInfo', idOfEvent=idOfEvent))


@app.route('/event/<int:idOfEvent>/notgoing', methods=['GET'])
@login_required
def eventNotGoing(idOfEvent):

    checkEvent = Event.query.get(idOfEvent)

    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    elif pacific.localize(checkEvent.start) <= pacific.localize(datetime.now()):

        flash('Event occured already', 'error')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    eventuser = UserEvent.query.filter_by(
        eventid=idOfEvent, userid=current_user.id).first()

    if eventuser is not None and eventuser.going == False or eventuser is None:

        flash('You haven\'t showed interest in this event', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    elif eventuser is not None and eventuser.going:

        eventuser.going = False
        db.session.commit()
        flash('You have removed your interest in this event', 'success')

    return redirect(url_for('eventInfo', idOfEvent=idOfEvent))


@app.route('/meeting/<int:idOfMeeting>/going', methods=['GET'])
@login_required
def meetingGoing(idOfMeeting):

    checkMeeting = Meeting.query.get(idOfMeeting)

    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    elif pacific.localize(checkMeeting.start) <= pacific.localize(datetime.now()):

        flash('Meeting occured already', 'error')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    meetinguser = UserMeeting.query.filter_by(
        meetingid=idOfMeeting, userid=current_user.id).first()

    if meetinguser is not None and meetinguser.going:

        flash('Already showed interest in this meeting', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    elif meetinguser is not None and meetinguser.going == False:

        meetinguser.going = True
        db.session.commit()
        flash('You have shown your interest in this meeting', 'success')

    else:

        usermeeting = UserMeeting(
            meetingid=idOfMeeting,
            userid=current_user.id,
            attended=False,
            going=True,
            currentYear=True,
            upvote=False,
            unsurevote=False,
            downvote=False)
        db.session.add(usermeeting)
        db.session.commit()

    return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))


@app.route('/meeting/<int:idOfMeeting>/notgoing', methods=['GET'])
@login_required
def meetingNotGoing(idOfMeeting):

    checkMeeting = Meeting.query.get(idOfMeeting)

    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    elif pacific.localize(checkMeeting.start) <= pacific.localize(datetime.now()):

        flash('Meeting occured already', 'error')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    meetinguser = UserMeeting.query.filter_by(
        meetingid=idOfMeeting, userid=current_user.id).first()

    if meetinguser is not None and meetinguser.going == False or meetinguser is None:

        flash('You haven\'t showed interest in this meeting', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    elif meetinguser is not None and meetinguser.going:

        meetinguser.going = False
        db.session.commit()
        flash('You have removed your interest in this meeting', 'success')

    return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))


@app.route('/members', methods=['GET'])
@login_required
def members():

    currentMembers = User.query.filter_by(
        currentmember=True).order_by('lastname').all()
    oldMembers = User.query.filter_by(
        currentmember=False).order_by('lastname').all()

    page = make_response(
        render_template(
            'members.html',
            currentMembers=currentMembers,
            oldMembers=oldMembers,
            identifier=False,
            indentify='',
            oldthings=len(oldMembers)))
    page = cookieSwitch(page)
    page.set_cookie('current', 'members', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/members/<identifier>', methods=['GET'])
@login_required
def memberType(identifier):

    if identifier == 'Admin':
        currentMembers = User.query.filter_by(
            admin=True, currentmember=True).order_by('lastname').all()
        oldMembers = User.query.filter_by(
            admin=True, currentmember=False).order_by('lastname').all()

    elif identifier == 'Leader':
        currentMembers = User.query.filter_by(
            leader=True, currentmember=True).order_by('lastname').all()
        oldMembers = User.query.filter_by(
            leader=True, currentmember=False).order_by('lastname').all()

    else:
        flash(f'No users in this catagory {identifier}', 'warning')
        return sendoff('members')

    page = make_response(
        render_template(
            'members.html',
            currentMembers=currentMembers,
            oldMembers=oldMembers,
            identifier=True,
            indentify=identifier,
            oldthings=len(oldMembers)))
    page = cookieSwitch(page)
    page.set_cookie('current', 'membersType', max_age=60 * 60 * 24 * 365)
    page.set_cookie(
        'membertype-current',
        identifier,
        max_age=60 * 60 * 24 * 365)
    return page


@app.route('/membersdata', methods=['GET'])
@login_required
def memberData():

    if current_user.leader:

        users = User.query.filter_by(currentmember=True, leader=False).all()

        page = make_response(
            render_template(
                'membersdata.html',
                users=users,
                oldCheck=True))
        page = cookieSwitch(page)
        page.set_cookie('current', 'memberData', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/membersdata/old', methods=['GET'])
@login_required
def memberDataOld():

    if current_user.leader:

        users = User.query.filter_by(currentmember=False, leader=False).all()

        page = make_response(
            render_template(
                'membersdata.html',
                users=users,
                oldCheck=False))
        page = cookieSwitch(page)
        page.set_cookie('current', 'memberDataOld', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/meetingsdata', methods=['GET'])
@login_required
def meetingData():

    if current_user.leader:

        meetings = Meeting.query.filter_by(currentYear=True).all()

        page = make_response(
            render_template(
                'eventMeetingViews.html',
                meeting=True,
                eventMeetings=meetings,
                oldCheck=True))
        page = cookieSwitch(page)
        page.set_cookie('current', 'meetingData', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/meetingsdata/old', methods=['GET'])
@login_required
def meetingDataOld():

    if current_user.leader:

        meetings = Meeting.query.filter_by(currentYear=False).all()

        page = make_response(
            render_template(
                'eventMeetingViews.html',
                meeting=True,
                eventMeetings=meetings,
                oldCheck=False))
        page = cookieSwitch(page)
        page.set_cookie(
            'current',
            'meetingDataOld',
            max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/eventsdata', methods=['GET'])
@login_required
def eventData():

    if current_user.leader:

        events = Event.query.filter_by(currentYear=True).all()

        page = make_response(
            render_template(
                'eventMeetingViews.html',
                meeting=False,
                eventMeetings=events,
                oldCheck=True))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventData', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/meetingsdata/old', methods=['GET'])
@login_required
def eventDataOld():

    if current_user.leader:

        events = Event.query.filter_by(currentYear=False).all()

        page = make_response(
            render_template(
                'eventMeetingViews.html',
                meeting=False,
                eventMeetings=events,
                oldCheck=False))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventDataOld', max_age=60 * 60 * 24 * 365)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/upcoming/meetings', methods=['GET'])
@login_required
def upcomingMeetings():

    meetings = []
    now = pacific.localize(datetime.now())

    for meet in Meeting.query.filter_by(currentYear=True).all():
        if pacific.localize(meet.start) > now:
            meetings.append(meet)

    interested = []

    for meet in UserMeeting.query.filter_by(
            currentYear=True,
            userid=current_user.id,
            going=True,
            attended=False).all():
        meeting = Meeting.query.get(meet.meetingid)
        if pacific.localize(meeting.start) > now:
            interested.append(meeting)
            if meeting in meetings:
                meetings.remove(meeting)

    meetings.sort(key=lambda meeting: meeting.start)
    interested.sort(key=lambda meeting: meeting.start)

    page = make_response(
        render_template(
            'upcomingEventMeeting.html',
            upcomingThings=meetings,
            interestedThings=interested,
            going=len(interested),
            event=False))

    page = cookieSwitch(page)
    page.set_cookie('current', 'upcomingMeetings', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/upcoming/events', methods=['GET'])
@login_required
def upcomingEvents():

    events = []
    now = pacific.localize(datetime.now())

    for thing in Event.query.filter_by(currentYear=True).all():
        if pacific.localize(thing.start) > now:
            events.append(thing)

    interested = []

    for thing in UserEvent.query.filter_by(
            currentYear=True,
            userid=current_user.id,
            going=True,
            attended=False).all():
        event = Event.query.get(thing.eventid)
        if pacific.localize(event.start) > now:
            interested.append(event)
            if event in events:
                events.remove(event)

    events.sort(key=lambda event: event.start)
    interested.sort(key=lambda event: event.start)

    page = make_response(
        render_template(
            'upcomingEventMeeting.html',
            upcomingThings=events,
            interestedThings=interested,
            going=len(interested),
            event=True))

    page = cookieSwitch(page)
    page.set_cookie('current', 'upcomingEvents', max_age=60 * 60 * 24 * 365)
    return page


app.route('/robots.txt', methods=['GET'])


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
