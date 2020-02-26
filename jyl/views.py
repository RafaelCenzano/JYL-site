from jyl import app, forms, db, bcrypt, login_manager
from flask import render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, current_user, logout_user, login_required, current_user
from jyl.forms import LoginForm, RequestResetForm, ResetPasswordForm, BugReportForm
from jyl.models import User
from hashlib import sha256


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except:
        return None
        

'''
Views
'''
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/home/', methods=['GET'])
def index():

    page = make_response(render_template('home.html'))

    if 'current' in request.cookies:
        current = request.cookies['current']
        page.set_cookie('page', current, max_age=60 * 60 * 24 * 365)

    page.set_cookie('current', 'index', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('You are already logged in', 'warning')
        if 'current' in request.cookies:
            page = request.cookies['current']
            return redirect(url_for(page))
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(
                f'Login Unsuccessful. User dosen\'t exsist',
                'error')
        else:  
            confirm = user.confirmed
            confirmed = ''
            if not confirm:
                confirmed = ' and check to make sure you have activated your account'

            if user and confirm and bcrypt.check_password_hash(
                user.password,
                sha256(
                    (form.password.data +
                     form.email.data +
                     app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')

                flash(f'Logged in successfully.', 'success')
                return redirect(next_page) if next_page else redirect(
                    url_for('index'))

            else:
                flash(
                    f'Login Unsuccessful. Please check email and password{confirmed}',
                    'error')

    return render_template('login.html', form=form)
    

@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token):

    if current_user.is_authenticated:
        flash('You do not need to confirm your account as you are logged in already', 'warning')
        if 'current' in request.cookies:
            page = request.cookies['current']
            return redirect(url_for(page))
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        email = confirm_token(token) == form.email.data

        if user.confirmed:
            flash('Account already confirmed. Please login.', 'info')
            return redirect(url_for('login'))

        if user and email and bcrypt.check_password_hash(
            user.password,
            sha256(
                (form.password.data +
                 form.email.data +
                 app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()):

            user.confirmed = True

            db.session.add(user)
            db.session.commit()

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(
                url_for('index'))

        else:
            flash(
                'Activation Unsuccessful. Please check email and password',
                'danger')

    return render_template('login.html', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():

    if current_user.is_authenticated:
        flash('You do not need to reset your password as you are logged in already', 'warning')
        if 'current' in request.cookies:
            page = request.cookies['current']
            return redirect(url_for(page))
        return redirect(url_for('index'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(
                f'Password Reset Unsuccessful. User dosen\'t exsist',
                'error')
        else:

            token = user.get_reset_token()
            reset_url = url_for('reset_token', token=token, _external=True)

            subject = 'Password Reset Request'

            html = render_template('password_reset_email.html', url=reset_url)
            #send_email(user.email, subject, html)
            return html

            flash(
                f'An email has been sent to {form.email.data} with instructions to reset your password',
                'info')

            return redirect(url_for('login'))

    return render_template('password_reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):

    if current_user.is_authenticated:
        flash('You do not need to reset your password as you are logged in already', 'warning')
        if 'current' in request.cookies:
            page = request.cookies['current']
            return redirect(url_for(page))
        return redirect(url_for('index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'error')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            sha256(
                (form.password.data +
                 form.email.data +
                 app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')
        user.password = hashed_password

        db.session.commit()

        flash('Your password has been updated!', 'success')

        return redirect(url_for('login'))

    return render_template('password_change.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():

    if current_user.is_authenticated:
        logout_user()
        flash('Logout successful', 'success')
        
    return redirect(url_for('index'))


@app.route('/bugreport', methods=['GET', 'POST'])
def bugreport():

    if current_user.is_authenticated == False:
        flash('You need to be logged in to fill out this form', 'warning')
        if 'current' in request.cookies:
            page = request.cookies['current']
            return redirect(url_for(page))
        return redirect(url_for('index'))

    form = BugReportForm()


@app.route('/license', methods=['GET'])
def license():

    page = make_response(render_template('license.html'))

    if 'current' in request.cookies:
        current = request.cookies['current']
        page.set_cookie('page', current, max_age=60 * 60 * 24 * 365)
    
    page.set_cookie('current', 'license', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/back')
@app.route('/back/')
def back():

    if 'page' in request.cookies:
        page = request.cookies['page']
        return redirect(url_for(page))

    else:
        return redirect(url_for('index'))
        
