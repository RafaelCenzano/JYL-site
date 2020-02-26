from jyl import db
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from jyl.models import User
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


'''
Forms for jyl toolbox
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


class ResetPasswordForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UserForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    bug = StringField('Bug', validators=[DataRequired()])
    submit = SubmitField('Submit Bug Report')


class FeatureRequestForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    feature = StringField('Feature', validators=[DataRequired()])
    submit = SubmitField('Submit Feature Request')