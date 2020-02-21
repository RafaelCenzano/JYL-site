from app import db
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf import FlaskForm, RecaptchaField
from app.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


def model_exists(model_class):
    try:
        model_class.query.first()
        return True
    except Exception as e:
        print(e)
        return False


'''
Create a registation form
'''


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        if model_exists(User):
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                raise ValidationError(
                    'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
