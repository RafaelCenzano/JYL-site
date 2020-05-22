from jyl import app, forms, db, bcrypt, login_manager
from flask import render_template, request, flash, make_response
from jyl.forms import UserRequestForm
from jyl.models import User
from flask_mail import Mail, Message
from flask_login import current_user, login_required
from jyl.helpers import sendoff, cookieSwitch


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

    page = make_response(render_template('userform.html', form=form, type='Bug Report'))
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

    page = make_response(render_template('userform.html', form=form, type='Feature Request'))
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

    page = make_response(render_template('userform.html', form=form, type='Help Request'))
    page = cookieSwitch(page)
    page.set_cookie('current', 'helprequest', max_age=60 * 60 * 24 * 365)
    return page

