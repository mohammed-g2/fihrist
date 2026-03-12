from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
  email = EmailField(_l('Email'), validators=[DataRequired(), Email(), Length(max=64)])
  password = PasswordField(_l('Password'), validators=[DataRequired()])
  remember_me = BooleanField(_l('keep me logged in'))
  submit = SubmitField(_l('Login'))
  

class RegisterForm(FlaskForm):
  username = StringField(_l('Username'), validators=[DataRequired()])
  email = EmailField(_l('Email'), validators=[DataRequired(), Email(), Length(max=64)])
  password = PasswordField(_l('Password'), validators=[
      DataRequired(), 
      EqualTo('confirm_password', message=_l('Password must match.'))])
  confirm_password = PasswordField(
    _l('Confirm Password'), validators=[DataRequired()])
  terms = BooleanField(_l('I agree on terms & services'), validators=[DataRequired()])
  submit = SubmitField(_l('Sign up'))


class VerifyUserEmailForm(FlaskForm):
  email = EmailField('Email', validators=[DataRequired(), Length(max=64), Email()])
  submit_email = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
  password = PasswordField('New Password', validators=[
    DataRequired(), Length(min=6), 
    EqualTo('password2', message='Password must match.')])
  password2 = PasswordField('Confirm password', validators=[DataRequired()])
  submit = SubmitField('Change Password')
