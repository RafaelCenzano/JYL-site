import re
from datetime import datetime
from hashlib import sha256
from random import randint
from threading import Thread

from flask import (flash, make_response, redirect, render_template,
                   request, send_file, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from pytz import timezone

from jyl import app, bcrypt, db
from jyl.eventMeeting import eventMeetingProccessing
from jyl.forms import *
from jyl.helpers import *
from jyl.models import *


# Timezone
pacific = timezone('US/Pacific')

'''
Views
'''

# Home page


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():

    page = make_response(render_template('home.html'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'index', max_age=SECONDS_IN_YEAR)
    return page


# Project License
@app.route('/license', methods=['GET'])
def licenseView():

    page = make_response(render_template('license.html'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'license', max_age=SECONDS_IN_YEAR)
    return page


# Bug Report form
@app.route('/bugreport', methods=['GET', 'POST'])
@login_required
def bugreport():

    form = UserRequestForm()

    if form.validate_on_submit():

        name = current_user.firstname + ' ' + current_user.lastname

        html = f'''
Hi,

A Bug Report for <a href="#">JYL Toolbox</a> has been submitted

Name: {name}

Email: {current_user.email}

{form.text.data}

- <a href="#">JYL Toolbox</a>
        '''

        text = f'''
Hi,

A Bug Report for JYL Toolbox has been submitted

Name: {name}

Email: {current_user.email}

{form.text.data}

- JYL Toolbox
        '''

        # Get all users that are admins
        try:
            users = User.query.filter_by(
                admin=True,
                currentmember=True).all()
        except BaseException:
            db.session.rollback()
            users = User.query.filter_by(
                admin=True,
                currentmember=True).all()

        # Create thread to send async email to all admins
        emailThread = Thread(
            target=asyncEmail,
            args=[
                app,
                html,
                text,
                users,
                'Bug Report - JYL Toolbox'])
        emailThread.start()

        flash('Your bug report has been submitted', 'info')
        return redirect(url_for('index'))

    # Return Bug Report Form
    page = make_response(
        render_template(
            'userform.html',
            form=form,
            type='Bug Report'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'bugreport', max_age=SECONDS_IN_YEAR)
    return page


@app.route('/request/feature', methods=['GET', 'POST'])
@login_required
def featurerequest():

    form = UserRequestForm()

    if form.validate_on_submit():

        name = current_user.firstname + ' ' + current_user.lastname

        html = f'''
Hello,

A Feature Request for <a href="#">JYL Toolbox</a> has been submitted

Name: {name}

Email: {current_user.email}

{form.text.data}

- <a href="#">JYL Toolbox</a>
        '''

        text = f'''
Hello,

A Feature Request for JYL Toolbox has been submitted

Name: {name}

Email: {current_user.email}

{form.text.data}

- JYL Toolbox
        '''

        # Get all users that are admins
        try:
            users = User.query.filter_by(
                admin=True,
                currentmember=True).all()
        except BaseException:
            db.session.rollback()
            users = User.query.filter_by(
                admin=True,
                currentmember=True).all()

        # Create thread to send async email to all admins
        emailThread = Thread(
            target=asyncEmail,
            args=[
                app,
                html,
                text,
                users,
                'Feature Request - JYL Toolbox'])
        emailThread.start()

        flash('Your feature request has been submitted', 'info')
        return redirect(url_for('index'))

    # Return Feature Request Form
    page = make_response(
        render_template(
            'userform.html',
            form=form,
            type='Feature Request'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'featurerequest', max_age=SECONDS_IN_YEAR)
    return page


@app.route('/request/help', methods=['GET', 'POST'])
@login_required
def helprequest():

    form = UserRequestForm()

    if form.validate_on_submit():

        name = current_user.firstname + ' ' + current_user.lastname

        html = f'''
Hi,

A Help Request for <a href="#">JYL Toolbox</a> has been submitted

Name: {name}

Email: {current_user.email}

{form.text.data}

- <a href="#">JYL Toolbox</a>
        '''

        if current_user.nicknameapprove:

            text = f'''
Hi,

A Help Request for JYL Toolbox has been submitted

Name: {name}

Email: {current_user.email}

{form.text.data}

- JYL Toolbox
        '''

        # Get all users that are leaders
        try:
            users = User.query.filter_by(
                leader=True,
                currentmember=True).all()
        except BaseException:
            db.session.rollback()
            users = User.query.filter_by(
                leader=True,
                currentmember=True).all()

        # Create thread to send async email to all admins
        emailThread = Thread(
            target=asyncEmail,
            args=[
                app,
                html,
                text,
                users,
                'Help Request - JYL Toolbox'])
        emailThread.start()

        flash('Your help request has been submitted', 'info')
        return redirect(url_for('index'))

    # Return Help Request Form
    page = make_response(
        render_template(
            'userform.html',
            form=form,
            type='Help Request'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'helprequest', max_age=SECONDS_IN_YEAR)
    return page


@app.route('/profile/<int:num>/<first>/<last>', methods=['GET'])
@login_required
def profile(num, first, last):

    # Query for user based on first name, last name, and their number count
    try:
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()
    except BaseException:
        db.session.rollback()
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()

    # User doesn't exsist
    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    # User is a leader
    # Use leader profile
    if checkUser.leader:

        return redirect(
            url_for(
                'profileLeader',
                num=num,
                first=first,
                last=last))

    # Return user profile with user data
    page = make_response(render_template(
        'profile.html',
        user=checkUser,
        lifetimeHours=cleanValue(checkUser.lifetimeHours),
        currentHours=cleanValue(checkUser.currentHours),
        currentMeetingHours=cleanValue(checkUser.currentMeetingHours),
        currentEventHours=cleanValue(checkUser.currentEventHours)))

    page = cookieSwitch(page)

    num = repr(num)

    # Set cookies to store current location in website
    page.set_cookie('current', 'profile', max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-num-current', num, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-first-current', first, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-last-current', last, max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'profile-type-current',
        'normal',
        max_age=SECONDS_IN_YEAR)
    return page


@app.route('/profile/<int:num>/<first>/<last>/leader', methods=['GET'])
@login_required
def profileLeader(num, first, last):

    # Query for user based on first name, last name, and their number count
    try:
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()
    except BaseException:
        db.session.rollback()
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()

    # User not found
    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    # User is not a leader, redirect to normal profile
    if not checkUser.leader:

        flash('User is not a leader', 'warning')
        return redirect(url_for('profile', num=num, first=first, last=last))

    # Return leader profile
    page = make_response(render_template(
        'profileLeader.html',
        user=checkUser))

    page = cookieSwitch(page)
    num = repr(num)
    page.set_cookie('current', 'profileLeader', max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-num-current', num, max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'profile-first-current',
        first,
        max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-last-current', last, max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'profile-type-current',
        'normal',
        max_age=SECONDS_IN_YEAR)
    return page


@app.route('/profile/<int:num>/<first>/<last>/meetings', methods=['GET'])
@login_required
def profileMeeting(num, first, last):

    # Query for user based on first name, last name, and their number count
    try:
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()
    except BaseException:
        db.session.rollback()
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()

    # User not found
    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    # Leaders don't attend meetings
    if checkUser.leader:

        return redirect(url_for('memberType', identifier='leader'))

    # Query for meeintgs user attended
    attended = UserMeeting.query.filter_by(
        userid=checkUser.id, attended=True, currentYear=True).all()

    # Query for meeting user plans to attend
    going = UserMeeting.query.filter_by(
        userid=checkUser.id,
        going=True,
        attended=False,
        currentYear=True).all()

    # Get every meeting object for meetings user attended
    meetingsAttended = [
        Meeting.query.get(
            meeting.meetingid) for meeting in attended]

    meetingsGoing = []

    # Get current time in pacific time zone
    now = pacific.localize(datetime.now())

    for meeting in going:
        theMeeting = Meeting.query.get(meeting.meetingid)

        # Save every meeting that is in the future
        if pacific.localize(theMeeting.start) > now:
            meetingsGoing.append(theMeeting)

        # Remove meetings user never attended
        else:
            db.session.delete(meeting)
            db.session.commit()

    # Sort meetings by datetime
    meetingsAttended.sort(key=lambda meeting: meeting.start, reverse=True)
    meetingsGoing.sort(key=lambda meeting: meeting.start, reverse=True)

    # Return page with user current meeting data
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

    page.set_cookie('current', 'profileMeeting', max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-num-current', num, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-first-current', first, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-last-current', last, max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'profile-type-current',
        'meeting',
        max_age=SECONDS_IN_YEAR)
    return page


@app.route('/profile/<int:num>/<first>/<last>/meetings/old', methods=['GET'])
@login_required
def profileMeetingOld(num, first, last):

    # Query for user based on first name, last name, and their number count
    try:
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()
    except BaseException:
        db.session.rollback()
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()

    # User not found
    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    # Leaders do not attend meetings
    if checkUser.leader:

        return redirect(url_for('memberType', identifier='leader'))

    # Query every meeting attended
    attended = UserMeeting.query.filter_by(
        userid=checkUser.id, attended=True).all()

    # Get every meeting object and sort by date
    meetingsAttended = [
        Meeting.query.get(
            meeting.meetingid) for meeting in attended]
    meetingsAttended.sort(key=lambda meeting: meeting.start, reverse=True)

    # Return page with every meeting user has ever attended
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

    page.set_cookie('current', 'profileMeetingOld', max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-num-current', num, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-first-current', first, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-last-current', last, max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'profile-type-current',
        'meetingold',
        max_age=SECONDS_IN_YEAR)
    return page


@app.route('/profile/<int:num>/<first>/<last>/events', methods=['GET'])
@login_required
def profileEvent(num, first, last):

    # Query for user based on first name, last name, and their number count
    try:
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()
    except BaseException:
        db.session.rollback()
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()

    # User doesn't exsist
    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    # Leaders do not attend events
    if checkUser.leader:

        return redirect(url_for('memberType', identifier='leader'))

    # Query events attended and planning to attend
    attended = UserEvent.query.filter_by(
        userid=checkUser.id,
        attended=True,
        currentYear=True).all()
    going = UserEvent.query.filter_by(
        userid=checkUser.id,
        going=True,
        attended=False,
        currentYear=True).all()

    # Get event ovject for every event user attended
    eventsAttended = [Event.query.get(event.eventid) for event in attended]

    eventsGoing = []

    # Get current time in pacific timezone
    now = pacific.localize(datetime.now())

    for event in going:
        theEvent = Event.query.get(event.eventid)

        # Save every event in the future user plans to attend
        if pacific.localize(theEvent.start) > now:
            eventsGoing.append(theEvent)

        # Remove userEvent because user never attended
        else:
            db.session.delete(event)
            db.session.commit()

    # Sort lists by start datetime
    eventsAttended.sort(key=lambda event: event.start, reverse=True)
    eventsGoing.sort(key=lambda event: event.start, reverse=True)

    # Return page with user current event data
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

    page.set_cookie('current', 'profileEvent', max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-num-current', num, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-first-current', first, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-last-current', last, max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'profile-type-current',
        'event',
        max_age=SECONDS_IN_YEAR)
    return page


@app.route('/profile/<int:num>/<first>/<last>/events/old', methods=['GET'])
@login_required
def profileEventOld(num, first, last):

    # Query for user based on first name, last name, and their number count
    try:
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()
    except BaseException:
        db.session.rollback()
        checkUser = User.query.filter_by(
            firstname=first,
            lastname=last,
            namecount=num).first()

    # User doesn't exsist
    if checkUser is None:

        flash('User not found', 'error')
        return sendoff('index')

    # Leaders don't attend events
    if checkUser.leader:

        return redirect(url_for('memberType', identifier='leader'))

    # Query every event user attended
    attended = UserEvent.query.filter_by(
        userid=checkUser.id, attended=True).all()

    # Get every event object and sort by start datetime for all events user
    # attended
    eventsAttended = [Event.query.get(event.eventid) for event in attended]
    eventsAttended.sort(key=lambda event: event.start, reverse=True)

    # Return page with data about every event user ever attended
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

    page.set_cookie('current', 'profileEventOld', max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-num-current', num, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-first-current', first, max_age=SECONDS_IN_YEAR)
    page.set_cookie('profile-last-current', last, max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'profile-type-current',
        'eventold',
        max_age=SECONDS_IN_YEAR)
    return page


@app.route('/meeting/<int:idOfMeeting>/review', methods=['GET', 'POST'])
@login_required
def meetingReview(idOfMeeting):

    # Query for Meeting
    try:
        checkMeeting = Meeting.query.get(idOfMeeting)
    except BaseException:
        db.session.rollback()
        checkMeeting = Meeting.query.get(idOfMeeting)

    # Meeting not found
    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    # Check if meeting has occured yet
    if pacific.localize(checkMeeting.start) > pacific.localize(datetime.now()):

        flash('Meeting hasn\'t occured yet', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Query for User Meeting
    checkUserMeeting = UserMeeting.query.filter_by(
        userid=current_user.id, meetingid=idOfMeeting).first()

    form = CreateReview()

    if form.validate_on_submit():

        happy = False
        meh = False
        sad = False

        # Find users feeling on review
        if form.reaction.data == 'happy':
            happy = True
        elif form.reaction.data == 'meh':
            meh = True
        else:
            sad = True

        # Save user's review
        checkUserMeeting.comment = form.review.data
        checkUserMeeting.upvote = happy
        checkUserMeeting.unsurevote = meh
        checkUserMeeting.downvote = sad

        # Update counts for types of votes
        if happy:
            checkMeeting.upvote += 1
        elif meh:
            checkMeeting.unsurevote += 1
        else:
            checkMeeting.downvote += 1

        # Update Database
        db.session.commit()

        # Redirect back to meeting page
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Check to make sure user hasn't commented before
    if checkUserMeeting and checkUserMeeting.comment:

        flash('You already created a review for this meeting', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Check to make sure user attended meetings
    if checkUserMeeting is None or not checkUserMeeting.attended:

        flash('You didn\'t attend this meeting', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Format the description
    desc = [linkFormatting(word)
            for word in checkMeeting.description.split(' ')]

    # Process meeting data
    eventMeeting = eventMeetingProccessing(checkMeeting, True)

    # Return page with meeting data and form for review
    page = make_response(
        render_template(
            'eventMeetingReview.html',
            form=form,
            edit=False,
            meeting=True,
            eventMeeting=checkMeeting,
            eventMeetingData=eventMeeting,
            desc=desc,
            hourcount=cleanValue(
                checkMeeting.hourcount)))
    page = cookieSwitch(page)
    return page


@app.route('/meeting/<int:idOfMeeting>/review/edit', methods=['GET', 'POST'])
@login_required
def meetingReviewEdit(idOfMeeting):

    # Query for Meeting
    try:
        checkMeeting = Meeting.query.get(idOfMeeting)
    except BaseException:
        db.session.rollback()
        checkMeeting = Meeting.query.get(idOfMeeting)

    # Meeting doesn't exsist
    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    # Check that meeting has occured
    if pacific.localize(checkMeeting.start) > pacific.localize(datetime.now()):

        flash('Meeting hasn\'t occured yet', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Query User Meeting
    checkUserMeeting = UserMeeting.query.filter_by(
        userid=current_user.id, meetingid=idOfMeeting).first()

    form = CreateReview()

    if form.validate_on_submit():

        currentHappy = checkUserMeeting.upvote
        currentMeh = checkUserMeeting.unsurevote

        happy = False
        meh = False
        sad = False

        # Get user reaction
        if form.reaction.data == 'happy':
            happy = True
        elif form.reaction.data == 'meh':
            meh = True
        else:
            sad = True

        # Update boolean comment and reaction boolean values
        checkUserMeeting.comment = form.review.data
        checkUserMeeting.upvote = happy
        checkUserMeeting.unsurevote = meh
        checkUserMeeting.downvote = sad

        # Remove 1 from count based off user's previous response
        if currentHappy:
            checkMeeting.upvote -= 1
        elif currentMeh:
            checkMeeting.unsurevote -= 1
        else:
            checkMeeting.downvote -= 1

        # Add 1 to new or same count based off user response
        if happy:
            checkMeeting.upvote += 1
        elif meh:
            checkMeeting.unsurevote += 1
        else:
            checkMeeting.downvote += 1

        # Commit to Database
        db.session.commit()

        # Redirect to meeting page
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # If user hasn't written a review redirect to write a review
    if checkUserMeeting and checkUserMeeting.comment is None:

        return redirect(url_for('meetingReview', idOfMeeting=idOfMeeting))

    # Check that user attended the meeting
    if checkUserMeeting and checkUserMeeting.comment:

        # Format meeting description
        desc = [linkFormatting(word)
                for word in checkMeeting.description.split(' ')]

        # Proccess meeting data
        eventMeeting = eventMeetingProccessing(checkMeeting, True)

        # update form to user's past reaction response
        if checkUserMeeting.upvote:
            form.reaction.data = 'happy'
        elif checkUserMeeting.unsurevote:
            form.reaction.data = 'meh'
        else:
            form.reaction.data = 'down'
        form.review.data = checkUserMeeting.comment

        # Return page with meeting data, review form, and user's past review
        # data
        page = make_response(
            render_template(
                'eventMeetingReview.html',
                form=form,
                edit=True,
                meeting=True,
                eventMeeting=checkMeeting,
                eventMeetingData=eventMeeting,
                desc=desc,
                hourcount=cleanValue(
                    checkMeeting.hourcount)))
        page = cookieSwitch(page)
        return page

    flash('You didn\'t attend this meeting', 'warning')
    return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))


@app.route('/meeting/<int:idOfMeeting>/review/delete', methods=['GET', 'POST'])
@login_required
def meetingReviewDelete(idOfMeeting):

    # Query for Meeting
    try:
        checkMeeting = Meeting.query.get(idOfMeeting)
    except BaseException:
        db.session.rollback()
        checkMeeting = Meeting.query.get(idOfMeeting)

    # Meeting doesn't exsist
    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    # Check that meeting has occured
    if pacific.localize(checkMeeting.start) > pacific.localize(datetime.now()):

        flash('Meeting hasn\'t occured yet', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Query for UserMeeting for the current_user
    checkUserMeeting = UserMeeting.query.filter_by(
        userid=current_user.id, meetingid=idOfMeeting).first()

    # Check that user wrote a review
    if checkUserMeeting and checkUserMeeting.comment is None:

        flash('You haven\'t written a review yet', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Check that user wrote a review and attended the meeting
    if checkUserMeeting and checkUserMeeting.comment:

        form = ConfirmPassword()

        if form.validate_on_submit():

            # Confirm user identity with password
            if bcrypt.check_password_hash(
                current_user.password,
                sha256(
                    (form.password.data +
                     current_user.email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                # Remove from reaction counts
                if checkUserMeeting.upvote:
                    checkMeeting.upvote -= 1
                elif checkUserMeeting.unsurevote:
                    checkMeeting.unsurevote -= 1
                else:
                    checkMeeting.downvote -= 1

                # Remove user's comment
                checkUserMeeting.comment = None
                checkUserMeeting.upvote = False
                checkUserMeeting.unsurevote = False
                checkUserMeeting.downvote = False

                db.session.commit()

            flash('Incorrect password', 'error')
            form.password.data = ''

        # Return page to confirm password
        date = checkMeeting.start.strftime('%B %-d, %Y')
        page = make_response(
            render_template(
                'passwordConfirm.html',
                form=form,
                title='Delete Review',
                message=f'Enter your password to delete your review for the meeting {date}'))
        page = cookieSwitch(page)
        return page

    flash('You didn\'t attend this meeting', 'warning')
    return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))


@app.route('/meeting/<int:idOfMeeting>', methods=['GET'])
@login_required
def meetingInfo(idOfMeeting):

    # Query for Meeting
    try:
        checkMeeting = Meeting.query.get(idOfMeeting)
    except BaseException:
        db.session.rollback()
        checkMeeting = Meeting.query.get(idOfMeeting)

    # Meeting not found
    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    # Proccess meeting data into a dictionary
    eventMeeting = eventMeetingProccessing(checkMeeting, True)

    areyougoing = False

    # Meeting has not occured yet
    if eventMeeting['future']:

        # Query for UserMeeting
        checkUserMeeting = UserMeeting.query.filter_by(
            meetingid=idOfMeeting, userid=current_user.id).first()

        # User has stated they plan to attend
        if checkUserMeeting is not None and checkUserMeeting.going:
            areyougoing = True

    # Format meeting description
    desc = [linkFormatting(word)
            for word in checkMeeting.description.split(' ')]

    # Return page with meeting data
    page = make_response(
        render_template(
            'eventMeeting.html',
            areyougoing=areyougoing,
            desc=desc,
            eventMeeting=checkMeeting,
            eventMeetingData=eventMeeting,
            hourcount=cleanValue(
                checkMeeting.hourcount),
            reviewlen=len(
                eventMeeting['userreview'])))

    page = cookieSwitch(page)
    idOfMeeting = repr(idOfMeeting)
    page.set_cookie('current', 'meeting', max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'meeting-id-current',
        idOfMeeting,
        max_age=SECONDS_IN_YEAR)
    return page


@app.route('/leader/dashboard', methods=['GET'])
@login_required
def creation():

    # Allow only admins and leaders
    if current_user.leader or current_user.admin:

        # Return the dashboard
        page = make_response(render_template('leaderDashboard.html'))
        page = cookieSwitch(page)
        page.set_cookie('current', 'creation', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/create/user', methods=['GET', 'POST'])
@login_required
def userCreation():

    # Allow only leaders and admins
    if current_user.leader or current_user.admin:

        form = CreateUser()

        if form.validate_on_submit():

            # Make email lowercase only
            email = form.email.data.lower()

            # Query for user based on email
            try:
                duplicationCheck = User.query.filter_by(
                    email=email).first()
            except BaseException:
                db.session.rollback()
                duplicationCheck = User.query.filter_by(
                    email=email).first()

            # Email already exsist can't create account
            if duplicationCheck is not None:

                flash(f'Duplicate email found', 'error')
                return render_template('userCreate.html', form=form)

            # Query to find if other users with the same name exsist
            samename = User.query.filter_by(
                firstname=form.first.data,
                lastname=form.last.data).all()

            # Generate random 6 digit password for new users
            passNum = repr(randint(100000, 999999))

            # Hash password with email, password, and security salt
            tempPass = bcrypt.generate_password_hash(
                sha256(
                    (passNum +
                     email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')

            # If no address make value None
            if form.address.data == '':
                address = None
            else:
                address = form.address.data

            # If no phone number make value None
            if form.phone.data == '':
                phone = None

            else:

                # Check if value is proper length and all numbers
                try:
                    phone = repr(int(form.phone.data))
                    if len(phone) != 10:
                        raise BaseException
                except BaseException:
                    flash(
                        'Phone number must be 10 digits long and only contain numbers',
                        'warning')
                    form.phone.data = ''
                    return render_template('userCreate.html', form=form)

            # Create new user
            newUser = User(
                firstname=form.first.data,
                lastname=form.last.data,
                email=email,
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
                numberphone=phone,
                showemail=False,
                showphone=False,
                meetingAlertoneday=False,
                meetingAlertthreeday=False,
                meetingAlertoneweek=False,
                eventAlertoneday=False,
                eventAlertthreeday=False,
                eventAlertoneweek=False,
                address=address,
                bio=None)

            # Add to database
            db.session.add(newUser)
            db.session.commit()

            # Create html for email to new user
            html = f'''
<p>Hello,</p>

<p>A JYL Toolbox account has been created for you</p>

<p>Login here: <a href="#">JYL Toolbox</a></p>

<p>Use this email ({email}) and this password: {passNum}</p>

<p>For security reasons, you should reset your password since this is a temporary password.</p>

<p>- <a href="#" class="jyl">JYL Toolbox</a></p>
            '''

            # Create backup text version for email to new user
            text = f'''
Hello,

A JYL Toolbox account has been created for you

Login here: https://url.com

Use this email ({email}) and this password: {passNum}

For security reasons, you should reset your password since this is a temporary password.

- JYL Toolbox
            '''

            # Send async email
            emailThread = Thread(
                target=asyncEmail,
                args=[
                    app,
                    html,
                    text,
                    [newUser],
                    'New JYL Toolbox account'])
            emailThread.start()

            flash(
                f'User created for {form.first.data} {form.last.data}',
                'success')

            return redirect(url_for('creation'))

        # Return page with create user form
        page = make_response(render_template('userCreate.html', form=form))
        page = cookieSwitch(page)
        page.set_cookie('current', 'userCreation', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/create/event', methods=['GET', 'POST'])
@login_required
def eventCreation():

    # Only allow leaders and admins
    if current_user.leader or current_user.admin:

        form = CreateEventMeeting()

        if form.validate_on_submit():

            # Calculate length of new event
            length = round((form.endtime.data -
                            form.starttime.data).total_seconds() / (60 * 60), 2)

            # Create new Event object
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
                attendancecount=0,
                attendancecheck=False)

            # Add to database
            db.session.add(newEvent)
            db.session.commit()

            # If email notification is requested
            if form.email.data:

                # Formate date
                date = form.starttime.data.strftime('%B %-d, %Y at %-I:%M %p')
                endtime = form.endtime.data.strftime('%-I:%M %p')

                # Replace spaces with '+'
                eventLocation = form.location.data.replace(' ', '+')

                # Create html email
                html = f'''
<p>Hello,</p>

<p>New event: {form.name.data} taking place on {date} to {endtime}.</p>

<p>Description: {form.description.data}</p>

<p>Location: <a href="https://www.google.com/maps/place/{eventLocation}">{form.location.data}</a></p></p>

<p>- JYL Toolbox</p>
                '''

                # Create text backup
                text = f'''
Hello,

New event: {form.name.data} taking place on {date} to {endtime}.

Description: {form.description.data}

Location: {form.location.data}

- JYL Toolbox
                '''

                # Query for all users that aren't leaders
                users = User.query.filter_by(
                    currentmember=True, leader=False).all()

                emailThread = Thread(
                    target=asyncEmail, args=[
                        app, html, text, users, 'New Event - JYL Toolbox'])
                emailThread.start()

            flash(f'Event {form.name.data} created', 'success')
            return redirect(url_for('creation'))

        # Return page with create event form
        page = make_response(
            render_template(
                'eventMeetingForm.html',
                form=form,
                meeting=False,
                edit=False))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventCreation', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/attendance/event', methods=['GET'])
@login_required
def attendanceEventList():

    # User must be a leader or admin
    if current_user.leader or current_user.admin:

        # Query for current events
        try:
            currentEvents = Event.query.filter_by(currentYear=True).all()
        except BaseException:
            db.session.rollback()
            currentEvents = Event.query.filter_by(currentYear=True).all()

        # Sort events by start time
        currentEvents.sort(key=lambda event: event.start, reverse=True)

        # Get current datetime
        now = pacific.localize(datetime.now())

        # Return page with all the meetings
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
            max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/attendance/meeting', methods=['GET'])
@login_required
def attendanceMeetingList():

    # Only allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for all current meetings
        try:
            currentMeetings = Meeting.query.filter_by(currentYear=True).all()
        except BaseException:
            db.session.rollback()
            currentMeetings = Meeting.query.filter_by(currentYear=True).all()

        # Sort meetings
        currentMeetings.sort(key=lambda meeting: meeting.start, reverse=True)

        # Get current datetime
        now = pacific.localize(datetime.now())

        # Return page with list of meetings
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
            max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/attendance/meeting/<int:idOfMeeting>', methods=['GET', 'POST'])
@login_required
def meetingAttendance(idOfMeeting):

    # Only allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for meeting
        try:
            checkMeeting = Meeting.query.get(idOfMeeting)
        except BaseException:
            db.session.rollback()
            checkMeeting = Meeting.query.get(idOfMeeting)

        # Meeting doesn't exsist
        if checkMeeting is None:

            flash('Meeting not found', 'error')
            return sendoff('index')

        # Check if meeting occured
        if pacific.localize(
                checkMeeting.start) > pacific.localize(
                datetime.now()):

            flash('Meeting hasn\'t occured yet', 'warning')
            return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

        if request.method == 'POST':

            # Query all current users who aren't leaders
            users = User.query.filter_by(
                currentmember=True, leader=False).all()

            # Sort by lastname
            users.sort(key=lambda user: user.lastname.lower())
            count = 0

            for user in users:

                # Find user in form response
                thisUser = request.form.get(
                    user.firstname +
                    user.lastname +
                    repr(
                        user.namecount))

                # Query for UserMeeting of current user
                checkUserMeeting = UserMeeting.query.filter_by(
                    meetingid=idOfMeeting, userid=user.id).first()

                # User did not attend the meeting
                if checkUserMeeting is not None and thisUser is None:

                    # If user had previously been marked as having attended
                    if checkUserMeeting.attended:

                        # Update user hours and counts
                        thisUserQuery = User.query.get(user.id)
                        thisUserQuery.lifetimeHours -= checkMeeting.hourcount
                        thisUserQuery.lifetimeMeetingHours -= checkMeeting.hourcount
                        thisUserQuery.lifetimeMeetingCount -= 1
                        thisUserQuery.currentHours -= checkMeeting.hourcount
                        thisUserQuery.currentMeetingHours -= checkMeeting.hourcount
                        thisUserQuery.currentMeetingCount -= 1

                    # Mark as not attended
                    checkUserMeeting.attended = False

                    # Update the database
                    db.session.commit()

                # User attended the meeting
                elif checkUserMeeting is not None and thisUser is not None:

                    # If user had not preiously been marked as not having
                    # attended
                    if not checkUserMeeting.attended:

                        # Update user hours and counts
                        thisUserQuery = User.query.get(user.id)
                        thisUserQuery.lifetimeHours += checkMeeting.hourcount
                        thisUserQuery.lifetimeMeetingHours += checkMeeting.hourcount
                        thisUserQuery.lifetimeMeetingCount += 1
                        thisUserQuery.currentHours += checkMeeting.hourcount
                        thisUserQuery.currentMeetingHours += checkMeeting.hourcount
                        thisUserQuery.currentMeetingCount += 1

                    checkUserMeeting.attended = True

                    # Save to database
                    db.session.commit()

                    # Add to count of total people who attended
                    count += 1

                # User attended the meeting but has no UserMeeting row
                elif thisUser is not None and checkUserMeeting is None:

                    # Create new UserMeeting for user
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

                    # add new UserMeeting object to database
                    db.session.add(newUserMeeting)

                    # Update user hours and counts
                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingCount += 1
                    thisUserQuery.currentHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingCount += 1

                    # Save to database
                    db.session.commit()

                    # add to count of total people who attended
                    count += 1

            # Update meeting attendance count
            checkMeeting.attendancecount = count

            # Save to database
            db.session.commit()

            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('attendanceMeetingList'))

        # Query for all users that are not leaders
        users = User.query.filter_by(currentmember=True, leader=False).all()
        inputs = []

        # Sort by last name
        users.sort(key=lambda user: user.lastname.lower())

        for user in users:

            # Query for UserMeeting row of user
            checkUserMeeting = UserMeeting.query.filter_by(
                meetingid=idOfMeeting, userid=user.id).first()

            # Create dictionary for each user
            data = {}

            data['check'] = False

            # If User was marked as attending this meeting
            if checkUserMeeting is not None and checkUserMeeting.attended:
                data['check'] = True

            # Add data for user name preference
            data['nicknameapprove'] = user.nicknameapprove
            data['firstname'] = user.firstname
            data['lastname'] = user.lastname
            data['nickname'] = user.nickname
            data['id'] = user.firstname + user.lastname + repr(user.namecount)

            # Add dictionary into 'inputs' list
            inputs.append(data)

        # Return page with all users and checkboxes for attendance
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

    # Only allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for meeting
        try:
            checkMeeting = Meeting.query.get(idOfMeeting)
        except BaseException:
            db.session.rollback()
            checkMeeting = Meeting.query.get(idOfMeeting)

        # Meeting doesn't exsist
        if checkMeeting is None:

            flash('Meeting not found', 'error')
            return sendoff('index')

        # Check if meeting occured
        if pacific.localize(
                checkMeeting.start) > pacific.localize(
                datetime.now()):

            flash('Meeting hasn\'t occured yet', 'warning')
            return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

        if request.method == 'POST':

            # Query all current users who aren't leaders
            users = User.query.filter_by(
                currentmember=True, leader=False).all()

            # Sort by lastname
            users.sort(key=lambda user: user.lastname.lower())
            count = 0

            for user in users:

                # Find user in form response
                thisUser = request.form.get(
                    user.firstname +
                    user.lastname +
                    repr(
                        user.namecount))

                # Query for UserMeeting of current user
                checkUserMeeting = UserMeeting.query.filter_by(
                    meetingid=idOfMeeting, userid=user.id).first()

                # User did not attend the meeting
                if checkUserMeeting is not None and thisUser is None:

                    # If user had previously been marked as having attended
                    if checkUserMeeting.attended:

                        # Update user hours and counts
                        thisUserQuery = User.query.get(user.id)
                        thisUserQuery.lifetimeHours -= checkMeeting.hourcount
                        thisUserQuery.lifetimeMeetingHours -= checkMeeting.hourcount
                        thisUserQuery.lifetimeMeetingCount -= 1
                        thisUserQuery.currentHours -= checkMeeting.hourcount
                        thisUserQuery.currentMeetingHours -= checkMeeting.hourcount
                        thisUserQuery.currentMeetingCount -= 1

                    # Mark as not attended
                    checkUserMeeting.attended = False

                    # Update the database
                    db.session.commit()

                # User attended the meeting
                elif checkUserMeeting is not None and thisUser is not None:

                    # If user had not preiously been marked as not having
                    # attended
                    if not checkUserMeeting.attended:

                        # Update user hours and counts
                        thisUserQuery = User.query.get(user.id)
                        thisUserQuery.lifetimeHours += checkMeeting.hourcount
                        thisUserQuery.lifetimeMeetingHours += checkMeeting.hourcount
                        thisUserQuery.lifetimeMeetingCount += 1
                        thisUserQuery.currentHours += checkMeeting.hourcount
                        thisUserQuery.currentMeetingHours += checkMeeting.hourcount
                        thisUserQuery.currentMeetingCount += 1

                    checkUserMeeting.attended = True

                    # Save to database
                    db.session.commit()

                    # Add to count of total people who attended
                    count += 1

                # User attended the meeting but has no UserMeeting row
                elif thisUser is not None and checkUserMeeting is None:

                    # Create new UserMeeting for user
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

                    # add new UserMeeting object to database
                    db.session.add(newUserMeeting)

                    # Update user hours and counts
                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingHours += checkMeeting.hourcount
                    thisUserQuery.lifetimeMeetingCount += 1
                    thisUserQuery.currentHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingHours += checkMeeting.hourcount
                    thisUserQuery.currentMeetingCount += 1

                    # Save to database
                    db.session.commit()

                    # add to count of total people who attended
                    count += 1

            # Update meeting attendance count
            checkMeeting.attendancecount = count

            # Save to database
            db.session.commit()

            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

        # Query for all users that are not leaders
        users = User.query.filter_by(currentmember=True, leader=False).all()
        inputs = []

        # Sort by last name
        users.sort(key=lambda user: user.lastname.lower())

        for user in users:

            # Query for UserMeeting row of user
            checkUserMeeting = UserMeeting.query.filter_by(
                meetingid=idOfMeeting, userid=user.id).first()

            # Create dictionary for each user
            data = {}

            data['check'] = False

            # If User was marked as attending this meeting
            if checkUserMeeting is not None and checkUserMeeting.attended:
                data['check'] = True

            # Add data for user name preference
            data['nicknameapprove'] = user.nicknameapprove
            data['firstname'] = user.firstname
            data['lastname'] = user.lastname
            data['nickname'] = user.nickname
            data['id'] = user.firstname + user.lastname + repr(user.namecount)

            # Add dictionary into 'inputs' list
            inputs.append(data)

        # Return page with all users and checkboxes for attendance
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
@login_required
def meetingCreate():

    # Only allow leaders and admins
    if current_user.leader or current_user.admin:

        form = CreateEventMeeting()

        # Fill in name as meetings don't have names
        form.name.data = 'filler'

        if request.method == 'POST' and form.validate_on_submit():

            # Endtime must be after starttime
            if form.endtime.data <= form.starttime.data:
                flash('Endtime must be after starttime', 'error')
                return render_template(
                    'eventMeetingForm.html',
                    form=form,
                    meeting=True,
                    edit=False)

            # Get the length of the meeting
            length = round((form.endtime.data -
                            form.starttime.data).total_seconds() / (60 * 60), 2)

            # Create new meeting object
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
                attendancecount=0,
                attendancecheck=False)

            # Add and save to the database
            db.session.add(newMeeting)
            db.session.commit()

            # If email notification is requested
            if form.email.data:

                # Format date and location
                date = form.starttime.data.strftime(
                    '%B %-d, %Y from %-I:%M %p')
                endtime = form.endtime.data.strftime('%-I:%M %p')
                eventLocation = form.location.data.replace(' ', '+')

                # Create html email
                html = f'''
<p>Hello,</p>

<p>New meeting taking place on {date} to {endtime}.</p>

<p>Location: <a href="https://www.google.com/maps/place/{eventLocation}">{form.location.data}</a></p>

<p>Description: {form.description.data}</p>

<p>- JYL Toolbox</p>
                    '''

                # Create text backup
                text = f'''
Hello,

New meeting taking place on {date} to {endtime}.

Description: {form.description.data}

Location: {form.location.data}

- JYL Toolbox
                '''

                # Query for all users who aren't leaders
                users = User.query.filter_by(
                    currentmember=True, leader=False).all()

                emailThread = Thread(
                    target=asyncEmail,
                    args=[
                        app,
                        html,
                        text,
                        users,
                        'New Meeting - JYL Toolbox'])
                emailThread.start()

            # Format date of meeting
            meetingDate = form.starttime.data.strftime('%B %-d, %Y')

            flash(f'New meeting created for {meetingDate}', 'success')
            return redirect(url_for('creation'))

        # Get current datetime
        now = pacific.localize(datetime.now())

        # Set default times and location
        form.starttime.data = now.replace(hour=12 + 4, minute=0, second=0)
        form.endtime.data = now.replace(hour=12 + 5, minute=30, second=0)
        form.location.data = '2012 Pine Street San Francisco CA'

        # Return page with form to create meeting
        page = make_response(
            render_template(
                'eventMeetingForm.html',
                form=form,
                meeting=True,
                edit=False))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/user', methods=['GET'])
@login_required
def userEditList():

    # Only allow leaders
    if current_user.leader:

        # Query all current users
        try:
            currentMembers = User.query.filter_by(currentmember=True).all()
        except BaseException:
            db.session.rollback()
            currentMembers = User.query.filter_by(currentmember=True).all()

        # Sort users by lastname
        currentMembers.sort(key=lambda user: user.lastname.lower())

        # Return list of users
        page = make_response(
            render_template(
                'memberEdit.html',
                currentMembers=currentMembers))
        page = cookieSwitch(page)
        page.set_cookie('current', 'userEditList', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/edit/user/<int:userId>', methods=['GET', 'POST'])
@login_required
def userEdit(userId):

    # Only allow leaders
    if current_user.leader:

        # Query for user
        try:
            user = User.query.get(userId)
        except BaseException:
            db.session.rollback()
            user = User.query.get(userId)

        # Check if user exsist
        if user is None:

            flash('User doesn\'t exsist', 'error')
            return sendoff('creation')

        form = CreateUser()

        # Fill in user's email
        form.email.data = user.email

        if form.validate_on_submit():

            # If address is empty set to None
            if form.address.data == '':
                address = None
            else:
                address = form.address.data

            # If phone number is empty set to None
            if form.phone.data == '':
                phone = None

            else:
                # Confirm input is a proper phone number
                try:
                    phone = repr(int(form.phone.data))
                    if len(phone) != 10:
                        raise BaseException
                except BaseException:
                    flash(
                        'Phone number must 10 digits long and only contain numbers',
                        'warning')
                    form.phone.data = ''
                    return render_template(
                        'userEdit.html', form=form, user=user)

            # Set user's data to form data
            user.firstname = form.first.data
            user.lastname = form.last.data
            user.school = form.school.data
            user.grade = form.grade.data
            user.address = address
            user.numberphone = phone
            user.leader = form.leader.data
            user.admin = form.admin.data

            # Save to database
            db.session.commit()

            flash(
                f'User edited successfully',
                'success')

            return redirect(
                url_for(
                    'profile',
                    num=user.namecount,
                    first=user.firstname,
                    last=user.lastname))

        # If user address is none set to empty string
        if user.address is None:
            address = ''
        else:
            address = user.address

        # If user phone number is none set to empty string
        if user.numberphone is None:
            phone = ''
        else:
            phone = user.numberphone

        # Set all form fields to current user data
        form.first.data = user.firstname
        form.last.data = user.lastname
        form.email.data = user.email
        form.school.data = user.school
        form.grade.data = user.grade
        form.address.data = address
        form.phone.data = phone
        form.leader.data = user.leader
        form.admin.data = user.admin

        # Return edit user form with user's current data
        page = make_response(
            render_template(
                'userEdit.html',
                form=form,
                user=user))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/edit/user/<int:userId>/delete', methods=['GET', 'POST'])
@login_required
def userDelete(userId):

    # Only allow leaders
    if current_user.leader:

        try:
            checkUser = User.query.get(userId)
        except BaseException:
            db.session.rollback()
            checkUser = User.query.get(userId)

        form = ConfirmPassword()

        if form.validate_on_submit():

            # Confirm password before deleting
            if bcrypt.check_password_hash(
                current_user.password,
                sha256(
                    (form.password.data +
                     current_user.email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                # If current user is deleting themselves logout first
                if checkUser.id == current_user.id:
                    logout_user()

                # Delete User threaded
                deleteThread = Thread(target=asyncDeleteUser, args=[checkUser])
                deleteThread.start()

                flash('User data deleted', 'success')
                return redirect(url_for('creation'))

            flash('Incorrect password', 'error')
            form.password.data = ''

        # Warn user they are going to delete themselves
        if checkUser.id == current_user.id:

            flash(
                'Warning you are on a path to delete your own account',
                'warning')

        # Return password confirm for deleting user
        return render_template(
            'passwordConfirm.html',
            form=form,
            title='Delete User',
            message=f'Enter your password to delete {checkUser.firstname} {checkUser.lastname}\'s account, their data, and data related to their account')

    flash('Must be a leader', 'warning')
    return sendoff('index')


@app.route('/profile/<int:num>/<first>/<last>/settings',
           methods=['GET', 'POST'])
@login_required
def userEdit1(num, first, last):

    # Query for user
    try:
        checkUser = User.query.filter_by(
            namecount=num,
            firstname=first,
            lastname=last).first()
    except BaseException:
        db.session.rollback()
        checkUser = User.query.filter_by(
            namecount=num,
            firstname=first,
            lastname=last).first()

    # User exsist and current user is equal to the user to edit
    if checkUser is not None and current_user.id == checkUser.id:

        # Use different form for leaders
        if checkUser.leader:

            form = LeaderSetting()

            if form.validate_on_submit():

                # If bio is blank set to None
                if form.bio.data == '':
                    bio = None
                else:
                    bio = form.bio.data

                # Update user settings
                checkUser.bio = bio
                checkUser.showemail = form.showemail.data
                checkUser.showphone = form.showphone.data

                # Save to database
                db.session.commit()

                return sendoff('index')

            # If user bio is None set to empty list
            if checkUser.bio:
                bio = checkUser.bio
            else:
                bio = ''

            # Set form fields to
            form.bio.data = bio
            form.showemail.data = checkUser.showemail
            form.showphone.data = checkUser.showphone

            return render_template(
                'leaderSetting.html', form=form, user=checkUser)

        form = UserSettings()

        if form.validate_on_submit():

            # If bio is empty set to None
            if form.bio.data == '':
                bio = None
            else:
                bio = form.bio.data

            # Update user's data and settings
            checkUser.bio = bio
            checkUser.showemail = form.showemail.data
            checkUser.showphone = form.showphone.data
            checkUser.meetingAlertoneday = False  # form.meetingAlertoneday.data
            checkUser.meetingAlertthreeday = False  # form.meetingAlertthreeday.data
            checkUser.meetingAlertoneweek = False  # form.meetingAlertoneweek.data
            checkUser.eventAlertoneday = False  # form.eventAlertoneday.data
            checkUser.eventAlertthreeday = False  # form.eventAlertthreeday.data
            checkUser.eventAlertoneweek = False  # form.eventAlertoneweek.data

            # Save to database
            db.session.commit()

            return sendoff('profile')

        # If bio is None set to empty string
        if checkUser.bio:
            bio = checkUser.bio
        else:
            bio = ''

        # Set form fields to current user data
        form.bio.data = bio
        form.showemail.data = checkUser.showemail
        form.showphone.data = checkUser.showphone
        form.meetingAlertoneday.data = False  # checkUser.meetingAlertoneday
        form.meetingAlertthreeday.data = False  # checkUser.meetingAlertthreeday
        form.meetingAlertoneweek.data = False  # checkUser.meetingAlertoneweek
        form.eventAlertoneday.data = False  # checkUser.eventAlertoneday
        form.eventAlertthreeday.data = False  # checkUser.eventAlertthreeday
        form.eventAlertoneweek.data = False  # checkUser.eventAlertoneweek

        # Jinja code for removed meeting alerts
        '''
        <h3>Meeting alerts</h3>
    <div class="form-group">
    {% if form.meetingAlertoneday.errors %}
        {{ form.meetingAlertoneday(class="form-control form-control-lg is-invalid") }}
        <div class="invalid-feedback">
            {% for error in form.meetingAlertoneday.errors %}
                <span>{{ error }}</span>
            {% endfor %}
        </div>
    {% else %}
        <label class="container">{{ form.meetingAlertoneday.label(class="form-label-css-checkbox") }}
            {{ form.meetingAlertoneday() }}
            <span class="checkmark"></span>
        </label>
    {% endif %}
    </div>
    <div class="form-group">
    {% if form.meetingAlertthreeday.errors %}
        {{ form.meetingAlertthreeday(class="form-control form-control-lg is-invalid") }}
        <div class="invalid-feedback">
            {% for error in form.meetingAlertthreeday.errors %}
                <span>{{ error }}</span>
            {% endfor %}
        </div>
    {% else %}
        <label class="container">{{ form.meetingAlertthreeday.label(class="form-label-css-checkbox") }}
            {{ form.meetingAlertthreeday() }}
            <span class="checkmark"></span>
        </label>
    {% endif %}
    </div>
    <div class="form-group">
    {% if form.meetingAlertoneweek.errors %}
        {{ form.meetingAlertoneweek(class="form-control form-control-lg is-invalid") }}
        <div class="invalid-feedback">
            {% for error in form.meetingAlertoneweek.errors %}
                <span>{{ error }}</span>
            {% endfor %}
        </div>
    {% else %}
        <label class="container">{{ form.meetingAlertoneweek.label(class="form-label-css-checkbox") }}
            {{ form.meetingAlertoneweek() }}
            <span class="checkmark"></span>
        </label>
    {% endif %}
    </div>
    <h3>Event alerts</h3>
    <div class="form-group">
    {% if form.eventAlertoneday.errors %}
        {{ form.eventAlertoneday(class="form-control form-control-lg is-invalid") }}
        <div class="invalid-feedback">
            {% for error in form.eventAlertoneday.errors %}
                <span>{{ error }}</span>
            {% endfor %}
        </div>
    {% else %}
        <label class="container">{{ form.eventAlertoneday.label(class="form-label-css-checkbox") }}
            {{ form.eventAlertoneday() }}
            <span class="checkmark"></span>
        </label>
    {% endif %}
    </div>
    <div class="form-group">
    {% if form.eventAlertthreeday.errors %}
        {{ form.eventAlertthreeday(class="form-control form-control-lg is-invalid") }}
        <div class="invalid-feedback">
            {% for error in form.eventAlertthreeday.errors %}
                <span>{{ error }}</span>
            {% endfor %}
        </div>
    {% else %}
        <label class="container">{{ form.eventAlertthreeday.label(class="form-label-css-checkbox") }}
            {{ form.eventAlertthreeday() }}
            <span class="checkmark"></span>
        </label>
    {% endif %}
    </div>
    <div class="form-group">
    {% if form.eventAlertoneweek.errors %}
        {{ form.eventAlertoneweek(class="form-control form-control-lg is-invalid") }}
        <div class="invalid-feedback">
            {% for error in form.eventAlertoneweek.errors %}
                <span>{{ error }}</span>
            {% endfor %}
        </div>
    {% else %}
        <label class="container">{{ form.eventAlertoneweek.label(class="form-label-css-checkbox") }}
            {{ form.eventAlertoneweek() }}
            <span class="checkmark"></span>
        </label>
    {% endif %}
    </div>
        '''

        # Return users settings form
        return render_template('userSetting.html', form=form, user=checkUser)

    flash('You can\'t access this settings page', 'warning')
    return redirect(url_for('profile', num=num, first=first, last=last))


@app.route('/profile/<int:num>/<first>/<last>/request/nickname',
           methods=['GET', 'POST'])
@login_required
def userNicknameRequest(num, first, last):

    # Query for user
    try:
        checkUser = User.query.filter_by(
            namecount=num,
            firstname=first,
            lastname=last).first()
    except BaseException:
        db.session.rollback()
        checkUser = User.query.filter_by(
            namecount=num,
            firstname=first,
            lastname=last).first()

    # User exsists and current user is requesting a nickname for themselves
    if checkUser is not None and current_user.id == checkUser.id:

        form = RequestNickname()

        if form.validate_on_submit():

            # Confirm that user checked the box
            if not form.understand.data:

                flash('You must check the required checkbox')
                return render_template('requestNickname.html', form=form)

            # Update nickname and don't approve nickname
            checkUser.nickname = form.nickname.data
            checkUser.nicknameapprove = False

            # Save to the database
            db.session.commit()

            return redirect(
                url_for(
                    'profile',
                    num=num,
                    first=first,
                    last=last))

        # If user has a current nickname set form field to nickname
        if checkUser.nickname:
            form.nickname.data = checkUser.nickname

        # Return page with conformation check and request for new nickname
        return render_template('requestNickname.html', form=form)

    flash('You can\'t access this nickname request page', 'warning')
    return redirect(url_for('profile', num=num, first=first, last=last))


@app.route('/edit/nickname', methods=['GET'])
@login_required
def nicknameList():

    # Only allow leaders
    if current_user.leader:

        # Query for all people who don't have an approved nickname
        try:
            users = User.query.filter_by(nicknameapprove=False).all()
        except BaseException:
            db.session.rollback()
            users = User.query.filter_by(nicknameapprove=False).all()

        # Query for users with an approved nickname
        nickedMembers = User.query.filter_by(nicknameapprove=True).all()
        applicableMembers = []

        # If user has unapproved nickname add them to the list
        for user in users:
            if user.nickname:
                applicableMembers.append(user)

        # Sort lists by lastname
        applicableMembers.sort(key=lambda user: user.lastname.lower())
        nickedMembers.sort(key=lambda user: user.lastname.lower())

        # Return page with users with nicknames
        return render_template(
            'nicknameList.html',
            unapproved=applicableMembers,
            approved=nickedMembers)

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/edit/nickname/<int:userId>/approve', methods=['GET', 'POST'])
@login_required
def approveNickname(userId):

    # Only allow leaders
    if current_user.leader:

        # Query for user
        try:
            checkUser = User.query.get(userId)
        except BaseException:
            db.session.rollback()
            checkUser = User.query.get(userId)

        # User not found
        if checkUser is None:

            flash('User not found', 'warning')
            return sendoff('index')

        if not checkUser.nicknameapprove and checkUser.nickname is not None:

            form = ConfirmPassword()

            if form.validate_on_submit():

                # Confirm leader password
                if bcrypt.check_password_hash(
                    current_user.password,
                    sha256(
                        (form.password.data +
                         current_user.email +
                         app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                    # Approve user's nickname
                    checkUser.nicknameapprove = True

                    # Save to database
                    db.session.commit()

                    flash('Nickname approved', 'success')
                    return redirect(url_for('nicknameList'))

                # Password isn't correect ask again
                flash('Incorrect password', 'error')
                form.password.data = ''

            # Return form with password conformation
            return render_template(
                'passwordConfirm.html',
                form=form,
                title='Approve Nickname',
                message=f'Enter your password to approve {checkUser.nickname} as {checkUser.firstname} {checkUser.lastname}\'s nickname')

        flash('User doesn\'t have a nickname request', 'error')
        return sendoff('index')

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/edit/nickname/<int:userId>/deny', methods=['GET', 'POST'])
@login_required
def disapproveNickname(userId):

    # Only allow leaders
    if current_user.leader:

        # Query for user
        try:
            checkUser = User.query.get(userId)
        except BaseException:
            db.session.rollback()
            checkUser = User.query.get(userId)

        # User not found
        if checkUser is None:

            flash('User not found', 'warning')
            return sendoff('index')

        # Confirm user has a nickname request
        if not checkUser.nicknameapprove and checkUser.nickname is not None:

            form = ConfirmPassword()

            if form.validate_on_submit():

                # Check password
                if bcrypt.check_password_hash(
                    current_user.password,
                    sha256(
                        (form.password.data +
                         current_user.email +
                         app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                    # Set approved to False and remove nickname
                    checkUser.nicknameapprove = False
                    checkUser.nickname = None

                    # Save to database
                    db.session.commit()

                    flash('Nickname denied', 'success')
                    return redirect(url_for('nicknameList'))

                # Leader password incorrect
                flash('Incorrect password', 'error')
                form.password.data = ''

            # Return password conformation form
            return render_template(
                'passwordConfirm.html',
                form=form,
                title='Deny Nickname',
                message=f'Enter your password to deny {checkUser.nickname} as {checkUser.firstname} {checkUser.lastname}\'s nickname')

        flash('User doesn\'t have a nickname request', 'error')
        return sendoff('index')

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/edit/nickname/<int:userId>/remove', methods=['GET', 'POST'])
@login_required
def removeNickname(userId):

    # Only allow leaders
    if current_user.leader:

        # Query for user
        try:
            checkUser = User.query.get(userId)
        except BaseException:
            db.session.rollback()
            checkUser = User.query.get(userId)

        # User not found
        if checkUser is None:
            flash('User not found', 'warning')
            return sendoff('index')

        # User has a nickname
        if checkUser.nicknameapprove and checkUser.nickname is not None:

            form = ConfirmPassword()

            if form.validate_on_submit():

                # Confirm leader password
                if bcrypt.check_password_hash(
                    current_user.password,
                    sha256(
                        (form.password.data +
                         current_user.email +
                         app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                    # Set nickname to None and nickname approve to False
                    checkUser.nicknameapprove = False
                    checkUser.nickname = None

                    # Save to database
                    db.session.commit()

                    flash('Nickname removed', 'success')
                    return redirect(url_for('nicknameList'))

                # Leader password not found
                flash('Incorrect password', 'error')
                form.password.data = ''

            # Return password conformation form
            return render_template(
                'passwordConfirm.html',
                form=form,
                title='Remove Nickname',
                message=f'Enter your password to remove {checkUser.nickname} as {checkUser.firstname} {checkUser.lastname}\'s nickname')

        flash('User doesn\'t have a nickname', 'error')
        return sendoff('index')

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/changeyear', methods=['GET', 'POST'])
@login_required
def changeYear():

    # Only allow leaders
    '''
    if current_user.leader:

        form = ConfirmPasswordConfirm()

        if form.validate_on_submit():

            if bcrypt.check_password_hash(
                current_user.password,
                sha256(
                    (form.password.data +
                     current_user.email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                newYearPush = YearAudit(
                    leaderid=current_user.id,
                    time=datetime.now(),
                    confirmed=True,
                    completed=False)
                db.session.add(newYearPush)
                db.session.commit()

                user = User.query.filter_by(
                    currentmember=True, leader=True).all()

                with app.app_context():
                    with mail.connect() as conn:
                        for user in users:
                            msg = Message('New Proccess Started - JYL Toolbox',
                                          recipients=[user.email])
                            msg.body = text
                            msg.html = html

                            conn.send(msg)

                flash('Proccess initiated', 'success')
                return sendoff('index')

            flash('Password is Incorrect', 'error')
            form.password.data = ''

        audits = []
        yearAudits = YearAudit.query.all()

        if yearAudits:
            yearAudits.sort(key=lambda yearaudit: yearaudit.time)

            for thing in yearAudits:
                dictionary = {}
                dictionary['leader'] = User.query.get(thing.leaderid)
                dictionary['audit'] = thing
                audits.append(dictionary)

        page = make_response(
            render_template(
                'changeYear.html',
                form=form,
                audits=audits,
                deny=False))
        page = cookieSwitch(page)
        return page
    '''

    flash('This is not working yet', 'warning')
    return sendoff('index')


@app.route('/changeyear/<int:changeyearId>/deny', methods=['GET', 'POST'])
@login_required
def changeYearDeny(changeyearId):
    '''
    if current_user.leader:

        checkChangeYear = yearAudits.query.get(changeyearId)

        if checkChangeYear:

            if checkChangeYear.completed:

                flash('This has been executed already', 'error')
                return sendoff('index')

            if not checkChangeYear.confirmed:

                flash('This has been denied already', 'warning')
                return sendoff('index')

            form = ConfirmPasswordConfirm()

            if form.validate_on_submit:

                if bcrypt.check_password_hash(
                    current_user.password,
                    sha256(
                        (form.password.data +
                         current_user.email +
                         app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                    checkChangeYear.confirmed = False
                    db.session.commit()

                    user = User.query.filter_by(
                        currentmember=True, leader=True).all()

                    with app.app_context():
                        with mail.connect() as conn:
                            for user in users:
                                msg = Message(
                                    'Change Year Proccess Canceled - JYL Toolbox',
                                    recipients=[
                                        user.email])
                                msg.body = text
                                msg.html = html

                                conn.send(msg)

                    flash('Proccess initiated', 'success')
                    return sendoff('index')

                flash('Password is Incorrect', 'error')
                form.password.data = ''

            audits = []
            yearAudits = YearAudit.query.all()

            if yearAudits:
                yearAudits.sort(key=lambda yearaudit: yearaudit.time)

                for thing in yearAudits:
                    dictionary = {}
                    dictionary['leader'] = User.query.get(thing.leaderid)
                    dictionary['audit'] = thing
                    audits.append(dictionary)

            page = make_response(
                render_template(
                    'changeYear.html',
                    form=form,
                    audits=audits,
                    deny=True))
            page = cookieSwitch(page)
            return page

        abort(404)
    '''

    flash('This is not working', 'warning')
    return sendoff('index')


@app.route('/edit/event', methods=['GET'])
@login_required
def eventEditList():

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for current events
        try:
            currentEvents = Event.query.filter_by(currentYear=True).all()
        except BaseException:
            db.session.rollback()
            currentEvents = Event.query.filter_by(currentYear=True).all()

        futureEvents = []
        pastEvents = []

        # Get current datetime
        now = pacific.localize(datetime.now())

        # Sort events into past and future events
        for event in currentEvents:
            if pacific.localize(event.start) > now:
                futureEvents.append(event)
            else:
                pastEvents.append(event)

        # Sort lists by date
        futureEvents.sort(key=lambda event: event.start)
        pastEvents.sort(key=lambda event: event.start)

        # Return page with past and future events
        page = make_response(
            render_template(
                'eventMeetingList.html',
                meeting=False,
                futureEventMeetings=futureEvents,
                pastEventMeetings=pastEvents))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventEditList', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/event/<int:eventId>', methods=['GET', 'POST'])
@login_required
def eventEdit(eventId):

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        try:
            checkEvent = Event.query.get(eventId)
        except BaseException:
            db.session.rollback()
            checkEvent = Event.query.get(eventId)

        # Event not found
        if checkEvent is None:

            flash('Event not found', 'error')
            return sendoff('index')

        form = CreateEventMeeting()

        if form.validate_on_submit():

            # Get length of event
            length = round((form.endtime.data -
                            form.starttime.data).total_seconds() / (60 * 60), 2)

            # Update event data
            checkEvent.hourcount = length
            checkEvent.name = form.name.data
            checkEvent.description = form.description.data
            checkEvent.location = form.location.data
            checkEvent.start = form.starttime.data
            checkEvent.end = form.endtime.data

            # Save to database
            db.session.commit()

            # If email notification selected
            if form.email.data:

                # Formate date
                date = form.starttime.data.strftime('%B %-d, %Y at %-I:%M %p')
                endtime = form.endtime.data.strftime('%-I:%M %p')
                eventLocation = form.location.data.replace(' ', '+')

                # Create html email
                html = f'''
<p>Hello,</p>

<p>The event {form.name.data} recieved an edit. Here are the new details</p>

<p>Time {date} to {endtime}</p>

<p>Description: {form.description.data}</p>

<p>Location: <a href="https://www.google.com/maps/place/{eventLocation}">{form.location.data}</a></p>

<p>Check out the event <a href="#">here</a>.</p>

<p>- JYL Toolbox</p>
                '''

                # Create text backup
                text = f'''
Hello,

The event {form.name.data} recieved an edit. Here are the new details

From {date} to {endtime}

Description: {form.description.data}

Location: {form.location.data}

Check out the event here: LINK

- JYL Toolbox
                '''

                # Query for all current users who aren't leaders
                users = User.query.filter_by(
                    currentmember=True, leader=False).all()

                # Send async emails
                emailThread = Thread(
                    target=asyncEmail,
                    args=[
                        app,
                        html,
                        text,
                        users,
                        f'Event {form.name.data} Changed - JYL Toolbox'])
                emailThread.start()

            flash('Event edited successfully!', 'success')
            return redirect(url_for('eventEditList'))

        # Set form fields to current event data
        form.name.data = checkEvent.name
        form.description.data = checkEvent.description
        form.location.data = checkEvent.location
        form.starttime.data = checkEvent.start
        form.endtime.data = checkEvent.end

        # Return page with event editing form
        page = make_response(
            render_template(
                'eventMeetingForm.html',
                form=form,
                meeting=False,
                edit=True,
                eventMeeting=checkEvent))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/event/<int:eventId>/delete', methods=['GET', 'POST'])
@login_required
def eventDeleteView(eventId):

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        checkEvent = Event.query.get(eventId)

        form = ConfirmPassword()

        if form.validate_on_submit():

            # Confirm password
            if bcrypt.check_password_hash(
                current_user.password,
                sha256(
                    (form.password.data +
                     current_user.email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                # Delete an event threaded
                deleteThread = Thread(target=eventDelete, args=[checkEvent])
                deleteThread.start()

                flash('Event data deleted', 'success')
                return redirect(url_for('creation'))

            # Password is not correct
            flash('Incorrect password', 'error')
            form.password.data = ''

        # Get current datetime
        date = checkEvent.start.strftime('%B %-d, %Y')

        # Return page for password confomation
        return render_template(
            'passwordConfirm.html',
            form=form,
            title='Delete Event',
            message=f'Enter your password to delete event: {checkEvent.name} that is/was on {date}')

    flash('Must be a leader', 'warning')
    return sendoff('index')


@app.route('/event/<int:eventId>/edit', methods=['GET', 'POST'])
@login_required
def eventEdit2(eventId):

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for event
        try:
            checkEvent = Event.query.get(eventId)
        except BaseException:
            db.session.rollback()
            checkEvent = Event.query.get(eventId)

        # Event doesn't exsist
        if checkEvent is None:

            flash('Event not found', 'error')
            return sendoff('index')

        form = CreateEventMeeting()

        if form.validate_on_submit():

            # Calculate length of event
            length = round((form.endtime.data -
                            form.starttime.data).total_seconds() / (60 * 60), 2)

            # Update event data
            checkEvent.hourcount = length
            checkEvent.name = form.name.data
            checkEvent.description = form.description.data
            checkEvent.location = form.location.data
            checkEvent.start = form.starttime.data
            checkEvent.end = form.endtime.data

            # Save to the database
            db.session.commit()

            # If email requested
            if form.email.data:

                # Format datetime and location
                date = form.starttime.data.strftime('%B %-d, %Y at %-I:%M %p')
                endtime = form.endtime.date.strftime('%-I:%M %p')
                eventLocation = form.location.data.replace(' ', '+')

                # Create html email
                html = f'''
<p>Hello,</p>

<p>The event {form.name.data} recieved an edit. Here are the new details</p>

<p>Time: {date} to {endtime}</p>

<p>Description: {form.description.data}</p>

<p>Location: <a href="https://www.google.com/maps/place/{eventLocation}">{form.location.data}</a></p>

<p>Check out the event <a href="#">here</a>.</p>

<p>- JYL Toolbox</p>
                '''

                # Create email text backup
                text = f'''
Hello,

The event {form.name.data} recieved an edit. Here are the new details

Time: {date} to {endtime}

Description: {form.description.data}

Location: {form.location.data}

Check out the event here: LINK

- JYL Toolbox
                '''

                # Query for all users
                users = User.query.filter_by(
                    currentmember=True, leader=False).all()

                # Send async email
                emailThread = Thread(target=asyncEmail, args=[
                                     [app, html, text, users, f'Event {form.name.data} Changed - JYL Toolbox']])
                emailThread.start()

            flash('Event edited successfully!', 'success')
            return redirect(url_for('eventInfo', idOfEvent=eventId))

        # Set form fields to current event data
        form.name.data = checkEvent.name
        form.description.data = checkEvent.description
        form.location.data = checkEvent.location
        form.starttime.data = checkEvent.start
        form.endtime.data = checkEvent.end

        # Return edit event form
        page = make_response(
            render_template(
                'eventMeetingForm.html',
                form=form,
                meeting=False,
                edit=True,
                eventMeeting=checkEvent))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/event/<int:eventId>/attendance', methods=['GET', 'POST'])
@login_required
def eventAttendance(eventId):

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for event
        try:
            checkEvent = Event.query.get(eventId)
        except BaseException:
            db.session.rollback()
            checkEvent = Event.query.get(eventId)

        # Event doesn't exsist
        if checkEvent is None:

            flash('Event not found', 'error')
            return sendoff('index')

        # Check that event has passed
        if pacific.localize(
                checkEvent.start) > pacific.localize(
                datetime.now()):

            flash('Event hasn\'t occured yet', 'warning')
            return redirect(url_for('eventInfo', idOfEvent=eventId))

        if request.method == 'POST':

            # Query for current users who aren't leaders
            users = User.query.filter_by(
                currentmember=True, leader=False).all()

            # Sort by lastname
            users.sort(key=lambda user: user.lastname.lower())

            count = 0

            for user in users:

                # Get user data from form
                thisUser = request.form.get(
                    user.firstname +
                    user.lastname +
                    repr(
                        user.namecount))

                # Query for UserEvent for user and current event
                checkUserEvent = UserEvent.query.filter_by(
                    eventid=eventId, userid=user.id).first()

                # User did not attend the event
                if checkUserEvent is not None and thisUser is None:

                    # If user had previously been marked as having attended
                    if checkUserEvent.attended:

                        # Update user data
                        thisUserQuery = User.query.get(user.id)
                        thisUserQuery.lifetimeHours -= checkEvent.hourcount
                        thisUserQuery.lifetimeEventHours -= checkEvent.hourcount
                        thisUserQuery.lifetimeEventCount -= 1
                        thisUserQuery.currentHours -= checkEvent.hourcount
                        thisUserQuery.currentEventHours -= checkEvent.hourcount
                        thisUserQuery.currentEventCount -= 1

                    # Set attended to false
                    checkUserEvent.attended = False

                    # Save to database
                    db.session.commit()

                # User attended the event
                elif checkUserEvent is not None and thisUser is not None:

                    # If user had previously been marked as having not attended
                    if not checkUserEvent.attended:

                        thisUserQuery = User.query.get(user.id)
                        thisUserQuery.lifetimeHours += checkEvent.hourcount
                        thisUserQuery.lifetimeEventHours += checkEvent.hourcount
                        thisUserQuery.lifetimeEventCount += 1
                        thisUserQuery.currentHours += checkEvent.hourcount
                        thisUserQuery.currentEventHours += checkEvent.hourcount
                        thisUserQuery.currentEventCount += 1

                    # Set attended to true
                    checkUserEvent.attended = True

                    # Save to database
                    db.session.commit()

                    # Add to total count of attendance
                    count += 1

                # User attended the event
                elif thisUser and checkUserEvent is None:

                    # Create new user event object
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

                    # Add to database
                    db.session.add(newUserEvent)

                    # Update user data
                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventCount += 1
                    thisUserQuery.currentHours += checkEvent.hourcount
                    thisUserQuery.currentEventHours += checkEvent.hourcount
                    thisUserQuery.currentEventCount += 1

                    # Save to database
                    db.session.commit()

                    # Add to total attendance count
                    count += 1

            # Update event attenfance count
            checkEvent.attendancecount = count

            # Save to database
            db.session.commit()

            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('eventInfo', idOfEvent=eventId))

        # Query for all current users who aren't leaders
        users = User.query.filter_by(currentmember=True, leader=False).all()
        inputs = []

        # Sort by lastname
        users.sort(key=lambda user: user.lastname.lower())

        for user in users:

            # Query for User Event
            checkUserEvent = UserEvent.query.filter_by(
                eventid=eventId, userid=user.id).first()

            # Create dictionary to store user data
            data = {}

            data['check'] = False

            # Check form if user had been marked as attended
            if checkUserEvent is not None and checkUserEvent.attended:
                data['check'] = True

            # Store data in dictionary to be used in jinja
            data['nicknameapprove'] = user.nicknameapprove
            data['firstname'] = user.firstname
            data['lastname'] = user.lastname
            data['nickname'] = user.nickname
            data['id'] = user.firstname + user.lastname + repr(user.namecount)

            # Store dictionary in list
            inputs.append(data)

        # Return page with dynamic check list for user attendance
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

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for event
        try:
            checkEvent = Event.query.get(eventId)
        except BaseException:
            db.session.rollback()
            checkEvent = Event.query.get(eventId)

        # Event doesn't exsist
        if checkEvent is None:

            flash('Event not found', 'error')
            return sendoff('index')

        # Check that event has passed
        if pacific.localize(
                checkEvent.start) > pacific.localize(
                datetime.now()):

            flash('Event hasn\'t occured yet', 'warning')
            return redirect(url_for('eventInfo', idOfEvent=eventId))

        if request.method == 'POST':

            # Query for current users who aren't leaders
            users = User.query.filter_by(
                currentmember=True, leader=False).all()

            # Sort by lastname
            users.sort(key=lambda user: user.lastname.lower())

            count = 0

            for user in users:

                # Get user data from form
                thisUser = request.form.get(
                    user.firstname +
                    user.lastname +
                    repr(
                        user.namecount))

                # Query for UserEvent for user and current event
                checkUserEvent = UserEvent.query.filter_by(
                    eventid=eventId, userid=user.id).first()

                # User did not attend the event
                if checkUserEvent is not None and thisUser is None:

                    # If user had previously been marked as having attended
                    if checkUserEvent.attended:

                        # Update user data
                        thisUserQuery = User.query.get(user.id)
                        thisUserQuery.lifetimeHours -= checkEvent.hourcount
                        thisUserQuery.lifetimeEventHours -= checkEvent.hourcount
                        thisUserQuery.lifetimeEventCount -= 1
                        thisUserQuery.currentHours -= checkEvent.hourcount
                        thisUserQuery.currentEventHours -= checkEvent.hourcount
                        thisUserQuery.currentEventCount -= 1

                    # Set attended to false
                    checkUserEvent.attended = False

                    # Save to database
                    db.session.commit()

                # User attended the event
                elif checkUserEvent is not None and thisUser is not None:

                    # If user had previously been marked as having not attended
                    if not checkUserEvent.attended:

                        thisUserQuery = User.query.get(user.id)
                        thisUserQuery.lifetimeHours += checkEvent.hourcount
                        thisUserQuery.lifetimeEventHours += checkEvent.hourcount
                        thisUserQuery.lifetimeEventCount += 1
                        thisUserQuery.currentHours += checkEvent.hourcount
                        thisUserQuery.currentEventHours += checkEvent.hourcount
                        thisUserQuery.currentEventCount += 1

                    # Set attended to true
                    checkUserEvent.attended = True

                    # Save to database
                    db.session.commit()

                    # Add to total count of attendance
                    count += 1

                # User attended the event
                elif thisUser and checkUserEvent is None:

                    # Create new user event object
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

                    # Add to database
                    db.session.add(newUserEvent)

                    # Update user data
                    thisUserQuery = User.query.get(user.id)
                    thisUserQuery.lifetimeHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventHours += checkEvent.hourcount
                    thisUserQuery.lifetimeEventCount += 1
                    thisUserQuery.currentHours += checkEvent.hourcount
                    thisUserQuery.currentEventHours += checkEvent.hourcount
                    thisUserQuery.currentEventCount += 1

                    # Save to database
                    db.session.commit()

                    # Add to total attendance count
                    count += 1

            # Update event attenfance count
            checkEvent.attendancecount = count

            # Save to database
            db.session.commit()

            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('attendanceEventList'))

        # Query for all current users who aren't leaders
        users = User.query.filter_by(currentmember=True, leader=False).all()
        inputs = []

        # Sort by lastname
        users.sort(key=lambda user: user.lastname.lower())

        for user in users:

            # Query for User Event
            checkUserEvent = UserEvent.query.filter_by(
                eventid=eventId, userid=user.id).first()

            # Create dictionary to store user data
            data = {}

            data['check'] = False

            # Check form if user had been marked as attended
            if checkUserEvent is not None and checkUserEvent.attended:
                data['check'] = True

            # Store data in dictionary to be used in jinja
            data['nicknameapprove'] = user.nicknameapprove
            data['firstname'] = user.firstname
            data['lastname'] = user.lastname
            data['nickname'] = user.nickname
            data['id'] = user.firstname + user.lastname + repr(user.namecount)

            # Store dictionary in list
            inputs.append(data)

        # Return page with dynamic check list for user attendance
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
@login_required
def meetingEditList():

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for all current meetings
        try:
            currentMeeting = Meeting.query.filter_by(currentYear=True).all()
        except BaseException:
            db.session.rollback()
            currentMeeting = Meeting.query.filter_by(currentYear=True).all()

        futureMeetings = []
        pastMeetings = []

        # Get cuurent datetime
        now = pacific.localize(datetime.now())

        # Sort meetings by past and present
        for meeting in currentMeeting:
            if pacific.localize(meeting.start) > now:
                futureMeetings.append(meeting)
            else:
                pastMeetings.append(meeting)

        # Sort by start datetime
        futureMeetings.sort(key=lambda meeting: meeting.start)
        pastMeetings.sort(key=lambda meeting: meeting.start)

        # Return list of past and future meetings
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
            max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/meeting/<int:meetingId>', methods=['GET', 'POST'])
@login_required
def meetingEdit(meetingId):

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for meeting
        try:
            checkMeeting = Meeting.query.get(meetingId)
        except BaseException:
            db.session.rollback()
            checkMeeting = Meeting.query.get(meetingId)

        # Meeting not found
        if checkMeeting is None:

            flash('Meeting not found', 'error')
            return sendoff('index')

        form = CreateEventMeeting()

        # Add filler because meetings don't have names
        form.name.data = 'filler'

        if form.validate_on_submit():

            # Calculate meeting length
            length = round((form.endtime.data -
                            form.starttime.data).total_seconds() / (60 * 60), 2)

            # Update meeting data
            checkMeeting.hourcount = length
            checkMeeting.description = form.description.data
            checkMeeting.location = form.location.data
            checkMeeting.start = form.starttime.data
            checkMeeting.end = form.endtime.data

            # Save to database
            db.session.commit()

            # If email notification requested
            if form.email.data:

                # Format datetimes and location
                date = form.starttime.data.strftime('%B %-d, %Y')
                dateFull = form.starttime.data.strftime(
                    '%B %-d, %Y at %-I:%M %p')
                eventLocation = form.location.data.replace(' ', '+')

                # Create html email
                html = f'''
<p>Hello,</p>

<p>The meeting on {date} recieved an edit. Here are the new details:</p>

<p>Date: {dateFull}</p>

<p>Description: {form.description.data}</p>

<p>Location: <a href="https://www.google.com/maps/place/{eventLocation}">{form.location.data}</a></p>

<p>Check out the meeting <a href="#">here</a>.</p>

<p>- JYL Toolbox</p>
                '''

                # Create backup text email
                text = f'''
Hello,

The meeting on {date} recieved an edit. Here are the new details:

Date: {dateFull}

Description: {form.description.data}

Location: {form.location.data}

Check out the meeting here: LINK

- JYL Toolbox
                '''

                # Query for all current users who aren't leaders
                users = User.query.filter_by(
                    currentmember=True, leader=False).all()

                emailThread = Thread(
                    target=asyncEmail,
                    args=[
                        app,
                        html,
                        text,
                        users,
                        f'Meeting on {date} Changed - JYL Toolbox'])

            flash('Meeting edited successfully!', 'success')
            return redirect(url_for('meetingEditList'))

        # Set form fields to current meeting data
        form.description.data = checkMeeting.description
        form.location.data = checkMeeting.location
        form.starttime.data = checkMeeting.start
        form.endtime.data = checkMeeting.end

        # Return meeting edit form with current meeting data
        page = make_response(
            render_template(
                'eventMeetingForm.html',
                form=form,
                meeting=True,
                edit=True,
                eventMeeting=checkMeeting))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/edit/meeting/<int:meetingId>/delete', methods=['GET', 'POST'])
@login_required
def meetingDeleteView(meetingId):

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        try:
            checkMeeting = Meeting.query.get(meetingId)
        except BaseException:
            db.session.rollback()
            checkMeeting = Meeting.query.get(meetingId)

        form = ConfirmPassword()

        if form.validate_on_submit():

            # Password check
            if bcrypt.check_password_hash(
                current_user.password,
                sha256(
                    (form.password.data +
                     current_user.email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                # Delete meeting threaded
                deleteThread = Thread(
                    target=meetingDelete, args=[checkMeeting])
                deleteThread.start()

                flash('Meeting data deleted', 'success')
                return redirect(url_for('creation'))

            # Password isn't correct
            flash('Incorrect password', 'error')
            form.password.data = ''

        # Format datetime
        date = checkMeeting.start.strftime('%B %-d, %Y')

        # Return page with password conformation
        return render_template(
            'passwordConfirm.html',
            form=form,
            title='Delete Meeting',
            message=f'Enter your password to delete meeting: {date}')

    flash('Must be a leader', 'warning')
    return sendoff('index')


@app.route('/meeting/<int:meetingId>/edit', methods=['GET', 'POST'])
@login_required
def meetingEdit1(meetingId):

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        try:
            checkMeeting = Meeting.query.get(meetingId)
        except BaseException:
            db.session.rollback()
            checkMeeting = Meeting.query.get(meetingId)

        # Meeting not found
        if checkMeeting is None:

            flash('Meeting not found', 'error')
            return sendoff('index')

        form = CreateEventMeeting()

        # Add filler since meetings don't have a name
        form.name.data = 'filler'

        if form.validate_on_submit():

            # Calculate length of meeting
            length = round((form.endtime.data -
                            form.starttime.data).total_seconds() / (60 * 60), 2)

            # Update meeting data
            checkMeeting.hourcount = length
            checkMeeting.description = form.description.data
            checkMeeting.location = form.location.data
            checkMeeting.start = form.starttime.data
            checkMeeting.end = form.endtime.data

            # Save to database
            db.session.commit()

            # If email notification requested
            if form.email.data:

                # Format datetimes and location
                date = form.starttime.data.strftime('%B %-d, %Y')
                dateFull = form.starttime.data.strftime(
                    '%B %-d, %Y at %-I:%M %p')
                eventLocation = form.location.data.replace(' ', '+')

                # Create html email
                html = f'''
<p>Hello,</p>

<p>The meeting on {date} recieved an edit. Here are the new details:</p>

<p>Date: {dateFull}</p>

<p>Description: {form.description.data}</p>

<p>Location: <a href="https://www.google.com/maps/place/{eventLocation}">{form.location.data}</a></p>

<p>Check out the meeting <a href="#">here</a>.</p>

<p>- JYL Toolbox</p>
                '''

                # Create text backup email
                text = f'''
Hello,

The meeting on {date} recieved an edit. Here are the new details:

Date: {dateFull}

Description: {form.description.data}

Location: {form.location.data}

Check out the meeting here: LINK

- JYL Toolbox
                '''

                # Query for all current users that aren't leaders
                users = User.query.filter_by(
                    currentmember=True, leader=False).all()

                # Send emails threaded
                emailThread = Thread(
                    target=asyncEmail,
                    args=[
                        app,
                        html,
                        text,
                        users,
                        f'Meeting on {date} Changed - JYL Toolbox'])

            flash('Meeting edited successfully!', 'success')
            return redirect(url_for('meetingInfo', idOfMeeting=meetingId))

        # Set form fields to current meeting data
        form.description.data = checkMeeting.description
        form.location.data = checkMeeting.location
        form.starttime.data = checkMeeting.start
        form.endtime.data = checkMeeting.end

        # Return meeting edit form with current meeting data
        page = make_response(
            render_template(
                'eventMeetingForm.html',
                form=form,
                meeting=True,
                edit=True,
                eventMeeting=checkMeeting))
        page = cookieSwitch(page)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/event/<int:idOfEvent>', methods=['GET'])
@login_required
def eventInfo(idOfEvent):

    # Query for event
    try:
        checkEvent = Event.query.get(idOfEvent)
    except BaseException:
        db.session.rollback()
        checkEvent = Event.query.get(idOfEvent)

    # Event doesn't exsist
    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    # Proccess event data
    eventMeeting = eventMeetingProccessing(checkEvent, False)

    areyougoing = False

    # If event is in the future, check if user stated they intend to attend
    if eventMeeting['future']:
        checkUserEvent = UserEvent.query.filter_by(
            eventid=idOfEvent, userid=current_user.id).first()
        if checkUserEvent is not None and checkUserEvent.going:
            areyougoing = True

    # Format description
    desc = [linkFormatting(word) for word in checkEvent.description.split(' ')]

    # Return event data
    page = make_response(
        render_template(
            'eventMeeting.html',
            areyougoing=areyougoing,
            desc=desc,
            eventMeeting=checkEvent,
            eventMeetingData=eventMeeting,
            hourcount=cleanValue(
                checkEvent.hourcount),
            reviewlen=len(
                eventMeeting['userreview'])))

    page = cookieSwitch(page)
    idOfEvent = repr(idOfEvent)
    page.set_cookie('current', 'event', max_age=SECONDS_IN_YEAR)
    page.set_cookie('event-id-current', idOfEvent, max_age=SECONDS_IN_YEAR)
    return page


@app.route('/event/<int:idOfEvent>/review', methods=['GET', 'POST'])
@login_required
def eventReview(idOfEvent):

    # Query for event
    try:
        checkEvent = Event.query.get(idOfEvent)
    except BaseException:
        db.session.rollback()
        checkEvent = Event.query.get(idOfEvent)

    # Event doesn't exsist
    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    # Make sure event has occured
    if pacific.localize(checkEvent.start) > pacific.localize(datetime.now()):

        flash('Event hasn\'t occured yet', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Query for user event of current event and user
    checkUserEvent = UserEvent.query.filter_by(
        userid=current_user.id, eventid=idOfEvent).first()

    form = CreateReview()

    if form.validate_on_submit():

        happy = False
        meh = False
        sad = False

        # set boolean value for user reaction
        if form.reaction.data == 'happy':
            happy = True
        elif form.reaction.data == 'meh':
            meh = True
        else:
            sad = True

        # Update UserEvent data
        checkUserEvent.comment = form.review.data
        checkUserEvent.upvote = happy
        checkUserEvent.unsurevote = meh
        checkUserEvent.downvote = sad

        # Add to event reactions
        if happy:
            checkEvent.upvote += 1
        elif meh:
            checkEvent.unsurevote += 1
        else:
            checkEvent.downvote += 1

        # Save to database
        db.session.commit()

        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Redirct user to edit review if they have a review
    if checkUserEvent and checkUserEvent.comment:

        return redirect(url_for('eventReviewEdit', idOfEvent=idOfEvent))

    # User did not attend the event
    if checkUserEvent is None or not checkUserEvent.attended:

        flash('You didn\'t attend this event', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    desc = [linkFormatting(word) for word in checkEvent.description.split(' ')]

    # Proccess event data
    eventMeeting = eventMeetingProccessing(checkEvent, False)

    # Return review page for event
    page = make_response(
        render_template(
            'eventMeetingReview.html',
            form=form,
            edit=False,
            meeting=True,
            eventMeeting=checkEvent,
            eventMeetingData=eventMeeting,
            desc=desc,
            hourcount=cleanValue(
                checkEvent.hourcount)))
    page = cookieSwitch(page)
    return page


@app.route('/event/<int:idOfEvent>/review/edit', methods=['GET', 'POST'])
@login_required
def eventReviewEdit(idOfEvent):

    # Query for event
    try:
        checkEvent = Event.query.get(idOfEvent)
    except BaseException:
        db.session.rollback()
        checkEvent = Event.query.get(idOfEvent)

    # Event not found
    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    # Check that event has occured
    if pacific.localize(checkEvent.start) > pacific.localize(datetime.now()):

        flash('Event hasn\'t occured yet', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Query for UserEvent for current user and event
    checkUserEvent = UserEvent.query.filter_by(
        userid=current_user.id, eventid=idOfEvent).first()

    form = CreateReview()

    if form.validate_on_submit():

        # Get current user's reaction
        currentHappy = checkUserEvent.upvote
        currentMeh = checkUserEvent.unsurevote

        happy = False
        meh = False
        sad = False

        # Change user reaction to boolean values
        if form.reaction.data == 'happy':
            happy = True
        elif form.reaction.data == 'meh':
            meh = True
        else:
            sad = True

        # Update UserEvent review
        checkUserEvent.comment = form.review.data
        checkUserEvent.upvote = happy
        checkUserEvent.unsurevote = meh
        checkUserEvent.downvote = sad

        # Remove from event reactions based off user's original reaction
        if currentHappy:
            checkEvent.upvote -= 1
        elif currentMeh:
            checkEvent.unsurevote -= 1
        else:
            checkEvent.downvote -= 1

        # Add to event reaction based off user's new reaction
        if happy:
            checkEvent.upvote += 1
        elif meh:
            checkEvent.unsurevote += 1
        else:
            checkEvent.downvote += 1

        # Save to database
        db.session.commit()

        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Redirect user to write a review if they don't have one
    if checkUserEvent and checkUserEvent.comment is None:

        return redirect(url_for('eventReview', idOfEvent=idOfEvent))

    # User has a previous review
    if checkUserEvent and checkUserEvent.comment:

        desc = [linkFormatting(word)
                for word in checkEvent.description.split(' ')]

        # Proccess event data
        eventMeeting = eventMeetingProccessing(checkEvent, False)

        # Set form to current user's review
        if checkUserEvent.upvote:
            form.reaction.data = 'happy'
        elif checkUserEvent.unsurevote:
            form.reaction.data = 'meh'
        else:
            form.reaction.data = 'down'
        form.review.data = checkUserEvent.comment

        # Return review edit page with current review data
        page = make_response(
            render_template(
                'eventMeetingReview.html',
                form=form,
                edit=True,
                meeting=True,
                eventMeeting=checkEvent,
                eventMeetingData=eventMeeting,
                desc=desc,
                hourcount=cleanValue(
                    checkEvent.hourcount)))
        page = cookieSwitch(page)
        return page

    flash('You didn\'t attend this event', 'warning')
    return redirect(url_for('eventInfo', idOfEvent=idOfEvent))


@app.route('/event/<int:idOfEvent>/review/delete', methods=['GET', 'POST'])
@login_required
def eventReviewDelete(idOfEvent):

    # Query for event
    try:
        checkEvent = Event.query.get(idOfEvent)
    except BaseException:
        db.session.rollback()
        checkEvent = Event.query.get(idOfEvent)

    # Check that event exsists
    if checkEvent is None:

        flash('Ecvent not found', 'error')
        return sendoff('index')

    # Check that event has occured
    if pacific.localize(checkEvent.start) > pacific.localize(datetime.now()):

        flash('Event hasn\'t occured yet', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Query for UserEvent
    checkUserEvent = UserEvent.query.filter_by(
        userid=current_user.id, eventid=idOfEvent).first()

    # User hasn't written a review yet
    if checkUserEvent and checkUserEvent.comment is None:

        flash('You haven\'t written a review yet', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # User has review
    if checkUserEvent and checkUserEvent.comment:

        form = ConfirmPassword()

        if form.validate_on_submit():

            # Confirm password
            if bcrypt.check_password_hash(
                current_user.password,
                sha256(
                    (form.password.data +
                     current_user.email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                # Remove user's reaction from event total
                if checkUserEvent.upvote:
                    checkEvent.upvote -= 1
                elif checkUserEvent.unsurevote:
                    checkEvent.unsurevote -= 1
                else:
                    checkEvent.downvote -= 1

                # Remove user's review
                checkUserEvent.comment = None
                checkUserEvent.upvote = False
                checkUserEvent.unsurevote = False
                checkUserEvent.downvote = False

                # Save to database
                db.session.commit()

            # Incorrect password
            flash('Incorrect password', 'error')
            form.password.data = ''

        # Format datetime
        date = checkEvent.start.strftime('%B %-d, %Y')

        # Return page with password conformation
        page = make_response(
            render_template(
                'passwordConfirm.html',
                form=form,
                title='Delete Review',
                message=f'Enter your password to delete your review for the event {checkEvent.name}: {date}'))
        page = cookieSwitch(page)
        return page

    flash('You didn\'t attend this event', 'warning')
    return redirect(url_for('eventInfo', idOfEvent=idOfEvent))


@app.route('/event/<int:idOfEvent>/going', methods=['GET'])
@login_required
def eventGoing(idOfEvent):

    # Query for event
    try:
        checkEvent = Event.query.get(idOfEvent)
    except BaseException:
        db.session.rollback()
        checkEvent = Event.query.get(idOfEvent)

    # Check that event exsists
    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    # Exclude leaders since they can't attend events
    if current_user.leader:

        flash('Leaders don\'t attend events like members')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Check if event occured already
    if pacific.localize(checkEvent.start) <= pacific.localize(datetime.now()):

        flash('Event occured already', 'error')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Query for UserEvent
    eventuser = UserEvent.query.filter_by(
        eventid=idOfEvent, userid=current_user.id).first()

    # User already showed their intent to attended
    if eventuser is not None and eventuser.going:

        flash('Already showed interest in this event', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # User shows interest in attending
    elif eventuser is not None and eventuser.going is False:

        eventuser.going = True
        db.session.commit()
        flash('You have shown your interest in this event', 'success')

    # User shows interest in attending
    else:

        # Create UserEvent object
        userevent = UserEvent(
            eventid=idOfEvent,
            userid=current_user.id,
            attended=False,
            going=True,
            currentYear=True,
            upvote=False,
            unsurevote=False,
            downvote=False)

        # Add and save to database
        db.session.add(userevent)
        db.session.commit()
        flash('You have shown your interest in this event', 'success')

    return redirect(url_for('eventInfo', idOfEvent=idOfEvent))


@app.route('/event/<int:idOfEvent>/notgoing', methods=['GET'])
@login_required
def eventNotGoing(idOfEvent):

    # Query for event
    try:
        checkEvent = Event.query.get(idOfEvent)
    except BaseException:
        db.session.rollback()
        checkEvent = Event.query.get(idOfEvent)

    # Check that event exsists
    if checkEvent is None:

        flash('Event not found', 'error')
        return sendoff('index')

    # Exclude leaders since they can't attend events
    if current_user.leader:

        flash('Leaders don\'t attend events like members')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Check that event hasn't occured yet
    if pacific.localize(checkEvent.start) <= pacific.localize(datetime.now()):

        flash('Event occured already', 'error')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # Query for UserEvent
    eventuser = UserEvent.query.filter_by(
        eventid=idOfEvent, userid=current_user.id).first()

    # User doesn't want to attend but never said they wanted to intially
    if eventuser is not None and eventuser.going is False or eventuser is None:

        flash('You haven\'t showed interest in this event', 'warning')
        return redirect(url_for('eventInfo', idOfEvent=idOfEvent))

    # User no longer wants to attend
    elif eventuser is not None and eventuser.going:

        eventuser.going = False
        db.session.commit()
        flash('You have removed your interest in this event', 'success')

    return redirect(url_for('eventInfo', idOfEvent=idOfEvent))


@app.route('/meeting/<int:idOfMeeting>/going', methods=['GET'])
@login_required
def meetingGoing(idOfMeeting):

    # Query for meeting
    try:
        checkMeeting = Meeting.query.get(idOfMeeting)
    except BaseException:
        db.session.rollback()
        checkMeeting = Meeting.query.get(idOfMeeting)

    # Meeting doesn't exsist
    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    # Leaders don't attend meetings
    if current_user.leader:

        flash('Leaders don\'t attend meetings like members')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Check that meeting is in the future
    if pacific.localize(
            checkMeeting.start) <= pacific.localize(
            datetime.now()):

        flash('Meeting occured already', 'error')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Query for UserMeeting with current meeting and user
    meetinguser = UserMeeting.query.filter_by(
        meetingid=idOfMeeting, userid=current_user.id).first()

    # User already showed intent to attend
    if meetinguser is not None and meetinguser.going:

        flash('Already showed interest in this meeting', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # User will be attending (has exsisting UserMeeting record)
    elif meetinguser is not None and meetinguser.going is False:

        meetinguser.going = True
        db.session.commit()
        flash('You have shown your interest in this meeting', 'success')

    # User will be attending
    else:

        # Create UserMeeting for current user
        usermeeting = UserMeeting(
            meetingid=idOfMeeting,
            userid=current_user.id,
            attended=False,
            comment=None,
            going=True,
            currentYear=True,
            upvote=False,
            unsurevote=False,
            downvote=False)

        # Add UserMeeting and save to database
        db.session.add(usermeeting)
        db.session.commit()

        flash('You have shown your interest in this meeting', 'success')

    return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))


@app.route('/meeting/<int:idOfMeeting>/notgoing', methods=['GET'])
@login_required
def meetingNotGoing(idOfMeeting):

    # Query for meeting
    try:
        checkMeeting = Meeting.query.get(idOfMeeting)
    except BaseException:
        db.session.rollback()
        checkMeeting = Meeting.query.get(idOfMeeting)

    # Meeting doesn't exsist
    if checkMeeting is None:

        flash('Meeting not found', 'error')
        return sendoff('index')

    # Leaders don't attend meetings the same way
    if current_user.leader:

        flash('Leaders don\'t attend meetings like members')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Make sure meeting is in the future
    if pacific.localize(
            checkMeeting.start) <= pacific.localize(
            datetime.now()):

        flash('Meeting occured already', 'error')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # Query for UserMeeting with current user and meeting
    meetinguser = UserMeeting.query.filter_by(
        meetingid=idOfMeeting, userid=current_user.id).first()

    # User can't say they aren't going to event they didn't say they would
    # attend
    if meetinguser is not None and meetinguser.going is False or meetinguser is None:

        flash('You haven\'t showed interest in this meeting', 'warning')
        return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))

    # User has removed interest in the event
    elif meetinguser is not None and meetinguser.going:

        meetinguser.going = False
        db.session.commit()
        flash('You have removed your interest in this meeting', 'success')

    return redirect(url_for('meetingInfo', idOfMeeting=idOfMeeting))


@app.route('/members', methods=['GET'])
@login_required
def members():

    # Query for current and past users
    try:
        currentMembers = User.query.filter_by(
            currentmember=True).all()
    except BaseException:
        db.session.rollback()
        currentMembers = User.query.filter_by(
            currentmember=True).all()

    oldMembers = User.query.filter_by(
        currentmember=False).all()

    # Sort users by lastname
    currentMembers.sort(key=lambda user: user.lastname.lower())
    oldMembers.sort(key=lambda user: user.lastname.lower())

    # Return page showing current and past JYL members
    page = make_response(
        render_template(
            'members.html',
            currentMembers=currentMembers,
            oldMembers=oldMembers,
            identifier=False,
            indentify='',
            oldthings=len(oldMembers)))
    page = cookieSwitch(page)
    page.set_cookie('current', 'members', max_age=SECONDS_IN_YEAR)
    return page


@app.route('/members/<identifier>', methods=['GET'])
@login_required
def memberType(identifier):

    # Query for current and past admins
    if identifier.lower() == 'admin':
        currentMembers = User.query.filter_by(
            admin=True, currentmember=True).all()
        oldMembers = User.query.filter_by(
            admin=True, currentmember=False).all()

    # Query for current and past leaders
    elif identifier.lower() == 'leader':
        currentMembers = User.query.filter_by(
            leader=True, currentmember=True).all()
        oldMembers = User.query.filter_by(
            leader=True, currentmember=False).all()

    # Category isn't leader or admin
    else:
        flash(f'No users in this catagory {identifier}', 'warning')
        return sendoff('members')

    # Sort users by lastname
    currentMembers.sort(key=lambda user: user.lastname.lower())
    oldMembers.sort(key=lambda user: user.lastname.lower())

    # Return page with specific member types
    page = make_response(
        render_template(
            'members.html',
            currentMembers=currentMembers,
            oldMembers=oldMembers,
            identifier=True,
            indentify=identifier.capitalize(),
            oldthings=len(oldMembers)))
    page = cookieSwitch(page)
    page.set_cookie('current', 'membersType', max_age=SECONDS_IN_YEAR)
    page.set_cookie(
        'membertype-current',
        identifier,
        max_age=SECONDS_IN_YEAR)
    return page


@app.route('/membersdata', methods=['GET'])
@login_required
def memberData():

    # Allow only leaders
    if current_user.leader:

        # Query for all current members that aren't leaders
        try:
            users = User.query.filter_by(
                currentmember=True, leader=False).all()
        except BaseException:
            db.session.rollback()
            users = User.query.filter_by(
                currentmember=True, leader=False).all()

        # Return page with member's data
        page = make_response(
            render_template(
                'membersdata.html',
                users=users,
                oldCheck=True))
        page = cookieSwitch(page)
        page.set_cookie('current', 'memberData', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/membersdata/old', methods=['GET'])
@login_required
def memberDataOld():

    # Allow only leaders
    if current_user.leader:

        # Query for all past members that aren't leaders
        try:
            users = User.query.filter_by(
                currentmember=False, leader=False).all()
        except BaseException:
            db.session.rollback()
            users = User.query.filter_by(
                currentmember=False, leader=False).all()

        # Return page with member data from past members
        page = make_response(
            render_template(
                'membersdata.html',
                users=users,
                oldCheck=False))
        page = cookieSwitch(page)
        page.set_cookie('current', 'memberDataOld', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader', 'warning')
    return sendoff('index')


@app.route('/meetingsdata', methods=['GET'])
@login_required
def meetingData():

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for current meetings
        try:
            meetings = Meeting.query.filter_by(currentYear=True).all()
        except BaseException:
            db.session.rollback()
            meetings = Meeting.query.filter_by(currentYear=True).all()

        # Return page with current meeting data
        page = make_response(
            render_template(
                'eventMeetingViews.html',
                meeting=True,
                eventMeetings=meetings,
                oldCheck=True))
        page = cookieSwitch(page)
        page.set_cookie('current', 'meetingData', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/meetingsdata/old', methods=['GET'])
@login_required
def meetingDataOld():

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for past meetings
        try:
            meetings = Meeting.query.filter_by(currentYear=False).all()
        except BaseException:
            db.session.rollback()
            meetings = Meeting.query.filter_by(currentYear=False).all()

        # Return page with past meeting data
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
            max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/eventsdata', methods=['GET'])
@login_required
def eventData():

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for current events
        try:
            events = Event.query.filter_by(currentYear=True).all()
        except BaseException:
            db.session.rollback()
            events = Event.query.filter_by(currentYear=True).all()

        # Return page with current events data
        page = make_response(
            render_template(
                'eventMeetingViews.html',
                meeting=False,
                eventMeetings=events,
                oldCheck=True))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventData', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/eventsdata/old', methods=['GET'])
@login_required
def eventDataOld():

    # Allow leaders and admins
    if current_user.leader or current_user.admin:

        # Query for past events
        try:
            events = Event.query.filter_by(currentYear=False).all()
        except BaseException:
            db.session.rollback()
            events = Event.query.filter_by(currentYear=False).all()

        # Return page with past events data
        page = make_response(
            render_template(
                'eventMeetingViews.html',
                meeting=False,
                eventMeetings=events,
                oldCheck=False))
        page = cookieSwitch(page)
        page.set_cookie('current', 'eventDataOld', max_age=SECONDS_IN_YEAR)
        return page

    flash('Must be a Leader or Admin', 'warning')
    return sendoff('index')


@app.route('/upcoming/meetings', methods=['GET'])
@login_required
def upcomingMeetings():

    meetings = []

    # Get current datetime
    now = pacific.localize(datetime.now())

    # Store every meeting that is in the future
    for meet in Meeting.query.filter_by(currentYear=True).all():
        if pacific.localize(meet.start) > now:
            meetings.append(meet)

    interested = []

    # Move meetings into interested list if user has shown interest into
    # meeting
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

    # Sort lists by start datetime
    meetings.sort(key=lambda meeting: meeting.start)
    interested.sort(key=lambda meeting: meeting.start)

    # Return page with upcoming meetings
    page = make_response(
        render_template(
            'upcomingEventMeeting.html',
            upcomingThings=meetings,
            interestedThings=interested,
            going=len(interested),
            event=False))

    page = cookieSwitch(page)
    page.set_cookie('current', 'upcomingMeetings', max_age=SECONDS_IN_YEAR)
    return page


@app.route('/upcoming/events', methods=['GET'])
@login_required
def upcomingEvents():

    events = []

    # Get current datetime
    now = pacific.localize(datetime.now())

    # Get all future events
    for thing in Event.query.filter_by(currentYear=True).all():
        if pacific.localize(thing.start) > now:
            events.append(thing)

    interested = []

    # Sort events into events from
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

    # Sort by event start datetime
    events.sort(key=lambda event: event.start)
    interested.sort(key=lambda event: event.start)

    # Return page with future events
    page = make_response(
        render_template(
            'upcomingEventMeeting.html',
            upcomingThings=events,
            interestedThings=interested,
            going=len(interested),
            event=True))

    page = cookieSwitch(page)
    page.set_cookie('current', 'upcomingEvents', max_age=SECONDS_IN_YEAR)
    return page


@app.route('/login', methods=['GET', 'POST'])
def login():

    # If user is logged in stop them from logging in again
    if current_user.is_authenticated:
        flash('You are already logged in', 'warning')
        return sendoff('index'), 403

    form = LoginForm()

    if form.validate_on_submit():

        # Get input email
        email = form.email.data.lower()

        # Query for user by email
        try:
            user = User.query.filter_by(email=email).first()
        except BaseException:
            db.session.rollback()
            user = User.query.filter_by(email=email).first()

        # User not found
        if user is None:
            flash(
                f'Login Unsuccessful. User dosen\'t exsist',
                'error')
        else:

            # Check user password
            if bcrypt.check_password_hash(
                user.password,
                sha256(
                    (form.password.data +
                     email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                # Login user
                login_user(user, remember=form.remember.data)

                # Get next page
                next_page = request.args.get('next')

                # Redirect to index or to next
                flash(f'Logged in successfully.', 'success')
                return redirect(next_page) if next_page else redirect(
                    url_for('index'))

            # Password is incorrect
            else:
                flash(
                    'Login Unsuccessful. Please check email and password',
                    'error')

    # Return login form
    page = make_response(render_template('login.html', form=form))
    page = cookieSwitch(page)
    return page


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():

    # Prevent logged in user from resetting password
    if current_user.is_authenticated:
        flash(
            'You do not need to reset your password as you are logged in already',
            'warning')
        return sendoff('index')

    form = RequestResetForm()

    if form.validate_on_submit():

        # Query for user by email
        user = User.query.filter_by(email=form.email.data).first()

        # User not found
        if user is None:
            flash(
                f'Password Reset Unsuccessful. User dosen\'t exsist',
                'error')
        else:

            # Get user reset password token
            token = user.get_reset_token()

            # Create url for password reset
            reset_url = url_for('reset_token', token=token, _external=True)

            # Create html email
            html = f'''
<p>Hello,</p>

<p>Somebody (hopefully you!) requested a password reset for a <a href="#">JYL Toolbox</a> account.</p>

<p><a href="{reset_url}">Your reset link is here</a>. It will expire in 30 minutes.</p>

<p>- <a href="#">JYL Toolbox</a></p>
            '''

            # Create text backup
            text = f'''
Hello,

Somebody (hopefully you!) requested a password reset for a JYL Toolbox account.

Your reset link is here: {reset_url}. It will expire in 30 minutes.

- JYL Toolbox
            '''

            # Send async email
            emailThread = Thread(
                target=asyncEmail,
                args=[
                    app,
                    html,
                    text,
                    [user],
                    'Password Reset - JYL Toolbox'])
            emailThread.start()

            flash(
                f'An email has been sent to {form.email.data} with instructions to reset your password',
                'info')
            return sendoff('login')

    # Return password request reset form
    page = make_response(
        render_template(
            'password_reset_request.html',
            form=form))
    page = cookieSwitch(page)
    return page


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):

    # Do not allow logged in user to reset password
    if current_user.is_authenticated:
        flash(
            'You do not need to reset your password as you are logged in already',
            'warning')
        return sendoff('index')

    # Verify user reset token
    try:
        user = User.verify_reset_token(token)
    except BaseException:
        db.session.rollback()
        user = User.verify_reset_token(token)

    # Token not verified with any users
    if user is None:
        flash('That is an invalid or expired token', 'error')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():

        # Check that password contains a number
        pattern = re.compile('^[^0-9]*$')
        if pattern.search(form.password.data) is not None:
            flash('Password must contain a number', 'warning')
            return render_template('password_change.html', form=form)

        # Check that password contains special character
        pattern = re.compile('^.*[^A-Za-z0-9]+.*')
        if pattern.search(form.password.data) is None:
            flash('Password must contain a special character', 'warning')
            return render_template('password_change.html', form=form)

        # Hash new password
        hashed_password = bcrypt.generate_password_hash(
            sha256(
                (form.password.data +
                 form.email.data +
                 app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')

        # Set password to new hashed password
        user.password = hashed_password

        # Save to database
        db.session.commit()

        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))

    # Return page with password change form
    page = make_response(render_template('password_change.html', form=form))
    page = cookieSwitch(page)
    return page


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def passwordChange():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        # Check user password
        if bcrypt.check_password_hash(
            current_user.password,
            sha256(
                (form.password.data +
                 current_user.email +
                 app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

            # Check that password contains a number
            pattern = re.compile('^[^0-9]*$')
            if pattern.search(form.passwordNew.data) is not None:
                flash('Password must contain a number', 'warning')
                return render_template('password_change.html', form=form)

            # Check that password contains special character
            pattern = re.compile('^.*[^A-Za-z0-9]+.*')
            if pattern.search(form.passwordNew.data) is None:
                flash('Password must contain a special character', 'warning')
                return render_template('password_change.html', form=form)

            # Hash new password
            hashed_password = bcrypt.generate_password_hash(
                sha256(
                    (form.passwordNew.data +
                     current_user.email +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')

            # Set password to new hashed password
            current_user.password = hashed_password

            # Save to database
            db.session.commit()

            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))

        flash('Your current password is incorrect', 'error')

    # Return page with password change form
    page = make_response(
        render_template(
            'password_change_logged.html',
            form=form))
    page = cookieSwitch(page)
    return page


@app.route('/logout', methods=['GET'])
def logout():

    # If user is logged in, log them out
    if current_user.is_authenticated:
        logout_user()
        flash('Logout successful', 'success')

    return redirect(url_for('index'))


'''
SEO
'''


@app.route('/robots.txt', methods=['GET'])
def robots():

    # Return static robots.txt file for any web crawlers that use it
    return send_file('templates/seo/robots.txt')


@app.route('/favicon.ico', methods=['GET'])
def favicon():

    # Return static favicon.ico
    return send_file('static/img/jyl.ico')


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():

    # Return static sitemap XML file for SEO
    sitemap_xml = render_template('seo/sitemap.xml')
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


'''
Error Handlers
'''


@app.errorhandler(404)
def page_not_found(e):

    # 404 error page
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_for_server(e):

    # 500 error page
    return render_template('500.html')
