from jyl import app, forms, db, bcrypt
from flask import render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, current_user, logout_user, login_required, current_user
from jyl.forms import LoginForm, RequestResetForm, ResetPasswordForm


'''
Views
'''
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/home/', methods=['GET'])
def index():

    page = make_response(render_template('home.html'))
    page.set_cookie('page', 'index', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'warning')
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        confirm = user.confirmed
        confirmed = ''
        if not confirm:
            confirmed = ' and check to make sure you have activated your account'

        if user and confirm and bcrypt.check_password_hash(
            user.password,
            sha256(
                (form.password.data +
                 form.email.data +
                 app.config['SECURITY_PASSWORD_SALT']).encode()).hexdigest()):

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash(f'Logged in successfully.', 'success')
            return redirect(next_page) if next_page else redirect(
                url_for('home'))

        else:
            flash(
                f'Login Unsuccessful. Please check email and password{confirmed}',
                'error')

    page = make_response(render_template('login.html', form=form))
    page.set_cookie('page', 'login', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token):

    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
                 app.config['SECURITY_PASSWORD_SALT']).encode()).hexdigest()):

            user.confirmed = True

            db.session.add(user)
            db.session.commit()

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(
                url_for('home'))

        else:
            flash(
                'Activation Unsuccessful. Please check email and password',
                'danger')

    return render_template('login.html', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        reset_url = url_for('reset_token', token=token, _external=True)
        subject = 'Password Reset Request'
        html = render_template('reset_email.html', url=reset_url)
        send_email(user.email, subject, html)

        flash(
            'An email has been sent with instructions to reset your password',
            'info')

        return redirect(url_for('login'))

    return render_template('reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'error')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            sha256(
                (form.password.data +
                 app.config['SECURITY_PASSWORD_SALT']).encode()).hexdigest()).decode('utf-8')
        user.password = hashed_password

        db.session.commit()

        flash('Your password has been updated!', 'success')

        return redirect(url_for('login'))

    return render_template('reset_token.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logout successful', 'success')
    return redirect(url_for('index'))


@app.route('/license', methods=['GET'])
def license():

    page = make_response(render_template('license.html'))
    page.set_cookie('page', 'license', max_age=60 * 60 * 24 * 365)
    return page


@app.route('/back')
@app.route('/back/')
def back():

    if 'page' in request.cookies:
        page = request.cookies['page']
        return redirect(url_for(page))

    else:
        return redirect(url_for('index'))
        
