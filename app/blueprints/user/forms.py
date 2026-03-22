from flask_wtf import FlaskForm
from wtforms import (
  EmailField, StringField, PasswordField, SubmitField, TextAreaField,
  HiddenField)
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask_babel import lazy_gettext as _l

class ChangePasswordForm(FlaskForm):
  password = PasswordField(_l('New Password'), validators=[
    DataRequired(), Length(min=6, max=64), 
    EqualTo('confirm_password', message='Password must match.')])
  confirm_password = PasswordField(_l('Confirm password'), validators=[DataRequired()])
  submit = SubmitField(_l('Change Password'))


class UpdateUserProfileForm(FlaskForm):
  username = StringField(_l('Username'), validators=[
    DataRequired(), Length(3, 36)])
  bio = TextAreaField(_l('Bio'), validators=[Length(max=256)])
  submit_profile = SubmitField(_l('Update'))


class UpdateEmailForm(FlaskForm):
  email = EmailField(_l('Email'), validators=[DataRequired(), Length(max=64), Email()])
  submit_email = SubmitField(_l('Submit'))


class VerifyUserPasswordForm(FlaskForm):
  password = PasswordField(_l('Current Password'), validators=[DataRequired(), Length(min=6)])
  submit_password = SubmitField(_l('Submit'))


class SendMessageForm(FlaskForm):
  recipient = HiddenField('to', validators=[DataRequired()])
  content = TextAreaField(_l('Content'), validators=[DataRequired(), Length(max=128)])
  submit = SubmitField(_l('Send'))
