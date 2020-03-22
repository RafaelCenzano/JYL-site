from jyl import db
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from jyl.models import User
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length


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
                        validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10, max=100)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class BugReportForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    bug = StringField('Bug', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit Bug Report')


class FeatureRequestForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    bug = StringField('Feature', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit Feature Request')


class CreateUser(FlaskForm):
    first = StringField('First name', validators=[DataRequired(), Length(max=30)])
    last = StringField('Last name', validators=[DataRequired(), Length(max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Create User')