from jyl import app, forms
from flask import render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, current_user, logout_user, login_required


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

    '''
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
                'danger')

    return render_template('login.html', form=form)
    '''
    return 'LOGIN'