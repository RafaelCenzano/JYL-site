from jyl import app, forms, db, bcrypt, login_manager
from flask import render_template, request, flash, make_response
from jyl.forms import BugReportForm, FeatureRequestForm
from jyl.models import User
from flask_mail import Mail, Message
from flask_login import current_user, login_required
from jyl.helpers import sendoff, cookieSwitch


@app.route('/bugreport', methods=['GET', 'POST'])
@app.route('/bugreport/', methods=['GET', 'POST'])
@login_required
def bugreport():

    form = BugReportForm()
    if form.validate_on_submit():

        html = render_template(
            'userform_email.html',
            type='Bug Report',
            name=form.name.data,
            email=form.email.data,
            text=form.bug.data)

        text = f'''
Hi,

A Bug Report for JYL Toolbox has been submitted

Name: {form.name.data}

Email: {form.email.data}

{form.bug.data}

- JYL Toolbox
        '''

        '''
        recipients = User.query.filter_by(admin=True, currentmember=True).all()

        msg = Message('Bug Report - JYL Toolbox',
          sender='email@gmail.com',
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


@app.route('/featurerequest', methods=['GET', 'POST'])
@app.route('/featurerequest/', methods=['GET', 'POST'])
@login_required
def featurerequest():

    form = FeatureRequestForm()
    if form.validate_on_submit():

        html = render_template(
            'userform_email.html',
            type='Feature request',
            name=form.name.data,
            email=form.email.data,
            text=form.bug.data)

        text = f'''
Hi,

A Feature Request for JYL Toolbox has been submitted

Name: {form.name.data}

Email: {form.email.data}

{form.bug.data}

- JYL Toolbox
        '''

        '''
        recipients = User.query.filter_by(admin=True, currentmemner=True).all()

        msg = Message('Feature Request - JYL Toolbox',
          sender='email@gmail.com',
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

