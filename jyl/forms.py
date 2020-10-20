from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, IntegerField, PasswordField,
                     RadioField, StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)
from wtforms.widgets import TextArea

'''
Forms for jyl toolbox
'''


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=100,
                message='Password must be within 6 and 100 characters')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):
    passwordNow = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=100,
                message='Password must be within 6 and 100 characters')])
    confirm_password = PasswordField(
        'Confirm New Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')


class UserRequestForm(FlaskForm):
    text = TextAreaField(
        'Message',
        widget=TextArea(),
        validators=[
            DataRequired(),
            Length(
                max=500,
                message='Message must be 500 characters or less')])
    submit = SubmitField('Submit')


class CreateUser(FlaskForm):
    first = StringField(
        'First name', validators=[
            DataRequired(), Length(
                max=30, message='First name must be 30 characters or less')])
    last = StringField(
        'Last name', validators=[
            DataRequired(), Length(
                max=30, message='Last name must be 30 characters or less')])
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


class CreateEventMeeting(FlaskForm):
    name = StringField(
        'Event name',
        validators=[
            DataRequired(),
            Length(
                max=100,
                message='Event name must not be over 100 characters')])
    description = TextAreaField(
        'Description',
        widget=TextArea(),
        validators=[
            DataRequired(),
            Length(
                max=500,
                message='Description must be 500 characters or less')])
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
    email = BooleanField('Email update to members')
    submit = SubmitField('Submit')


class ConfirmPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ConfirmPasswordConfirm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = BooleanField('I confirm', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserSettings(FlaskForm):
    bio = TextAreaField(
        'Bio',
        widget=TextArea(),
        validators=[
            Length(
                max=500,
                message='Bio must be 500 characters or less')])
    showemail = BooleanField('Make your email public')
    showphone = BooleanField('Make your phone number public')
    meetingAlertoneday = BooleanField('Meeting email reminder 1 day before')
    meetingAlertthreeday = BooleanField('Meeting email reminder 3 days before')
    meetingAlertoneweek = BooleanField('Meeting email reminder 1 week before')
    eventAlertoneday = BooleanField('Event email reminder 1 day before')
    eventAlertthreeday = BooleanField('Event email reminder 3 days before')
    eventAlertoneweek = BooleanField('Event email reminder 1 week before')
    submit = SubmitField('Submit')


class LeaderSetting(FlaskForm):
    bio = TextAreaField(
        'Bio',
        widget=TextArea(),
        validators=[
            Length(
                max=500,
                message='Bio must be 500 characters or less')])
    showemail = BooleanField('Make your email public')
    showphone = BooleanField('Make your phone number public')
    submit = SubmitField('Submit')


class RequestNickname(FlaskForm):
    nickname = StringField(
        'Nickname', validators=[
            DataRequired(), Length(
                max=30, message='Nickname must be 30 characters or less')])
    understand = BooleanField('I am aware')
    # that my nickname request is sent to the leaders to be approved and if I
    # submit a new nickame it will be have to be re-approved
    submit = SubmitField('Submit')


class CreateReview(FlaskForm):
    reaction = RadioField(
        'Label', choices=[
            ('happy', 'description'), ('meh', 'whatever'), ('down', 'other')], validators=[
            DataRequired()])
    review = TextAreaField(
        'Review',
        widget=TextArea(),
        validators=[
            DataRequired(),
            Length(
                max=500,
                message='Description must be 500 characters or less')])
    submit = SubmitField('Submit')
