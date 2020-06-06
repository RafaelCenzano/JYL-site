from jyl import db
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateTimeField, TextAreaField
from datetime import datetime
from flask_wtf import FlaskForm
from jyl.models import User
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional


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
    password = PasswordField(
    'Password',
    validators=[
        DataRequired(),
        Length(
            min=10,
            max=100,
             message='Password must be within 10 and 100 characters')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UserRequestForm(FlaskForm):
    text = TextAreaField(
    'Message',
    widget=TextArea(),
    validators=[
        DataRequired(),
        Length(
            max=1000,
             message='Message must be 1000 characters or less')])
    submit = SubmitField('Submit')


class CreateUser(FlaskForm):
    first = StringField(
    'First name', validators=[
        DataRequired(), Length(
            max=30)])
    last = StringField(
    'Last name', validators=[
        DataRequired(), Length(
            max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    school = StringField(
    'School', validators=[
        DataRequired(), Length(
            max=100)])
    address = TextAreaField(
    'Address',
    widget=TextArea(),
    validators=[
        Length(
            max=500)])
    phone = StringField('Phone Number', validators=[Length(max=10)])
    grade = IntegerField('Grade Number', validators=[DataRequired()])
    leader = BooleanField('Leader')
    admin = BooleanField('Admin')
    submit = SubmitField('Submit')


class CreateEvent(FlaskForm):
    name = StringField(
    'Event name',
    validators=[
        DataRequired(),
        Length(
            max=100,
             message='Event name must not be over 100 characters')])
    description = TextAreaField(
    'Description', widget=TextArea(), validators=[
        DataRequired(), Length(
            max=500, message='Description must be 500 characters or less')])
    location = TextAreaField(
    'Location',
    widget=TextArea(),
    validators=[
        DataRequired(),
        Length(
            max=150,
             message='Location must be 150 characters or less')])
    starttime = DateTimeField('Start Time', validators=[DataRequired()])
    endtime = DateTimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CreateMeeting(FlaskForm):
    description = TextAreaField(
    'Description', widget=TextArea(), validators=[
        DataRequired(), Length(
            max=500, message='Message must be 500 characters or less')])
    location = TextAreaField(
    'Location',
    widget=TextArea(),
    validators=[
        DataRequired(),
        Length(
            max=150,
             message='Location must be 150 characters or less')])
    starttime = DateTimeField('Start Time', validators=[DataRequired()])
    endtime = DateTimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ConfirmPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserSettings(FlaskForm):
    bio = TextAreaField('Bio', widget=TextArea(), Length(max=500, message='Bio must be 500 characters or less')])
    showemail= BooleanField('Make your email public')
    showphone= BooleanField('Make your phone number public')
