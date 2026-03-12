from flask import render_template, redirect, url_for, current_app, flash
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _
from app.services import AuthenticationService, EmailService
from app.errors import (
  LoginError, UsernameAlreadyExistsError, EmailAlreadyExistsError,
  DatabaseCommitError, InvalidPasswordError, InvalidUsernameError,
  UserNotFoundError, TokenError, TokenPayloadError)
from . import auth_bp
from .forms import (
  LoginForm, RegisterForm, VerifyUserEmailForm, ResetPasswordForm)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  
  form = LoginForm()
  srv = AuthenticationService
  if form.validate_on_submit():
    try:
      user = srv.login_user(
        email=form.email.data, 
        password=form.password.data)
      login_user(user)
      return redirect(url_for('main.index'))
    except LoginError:
      flash(_('Wrong Username or Password.'), category='warning')
  return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  
  form = RegisterForm()
  srv = AuthenticationService
  
  if form.validate_on_submit():
    try:
      srv.register_user(
        username=form.username.data,
        email=form.email.data,
        password=form.password.data)
      flash(_('You can login now.'), category='info')
      return redirect(url_for('auth.login'))
    except UsernameAlreadyExistsError:
      form.username.errors.append(_('Username already exists.'))
    except EmailAlreadyExistsError:
      form.email.errors.append(_('Email already exists.'))
    except InvalidPasswordError:
      form.password.errors.append(_('Invalid password'))
    except InvalidUsernameError:
      form.username.errors.append(_('Invalid username'))
    except Exception as e:
      flash(_('Something went wrong, please try again later.'), category='warning')

  return render_template('auth/register.html', form=form)


@auth_bp.route('/confirm-account/<token>')
@login_required
def confirm(token):
  srv = AuthenticationService
  try:
    srv.confirm_user(current_user, token)
    flash(_('Account Confirmed.'), category='info')
  except Exception as e:
    flash(_('Something went wrong, please try again later.'), category='warning')
    
  return redirect(url_for('main.index'))


@auth_bp.route('/confirm-account')
@login_required
def request_confirmation_email():
  srv = EmailService
  try:
    srv.send_email(user=current_user, email_type='confirm_account')
    flash(
      _('A new confirmation email has been sent. Please check your inbox.'),
      category='info')
  except Exception as e:
    flash(_('Something went wrong, please try again later.'), category='warning')

  return redirect(url_for('user.settings'))


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def request_password_reset():
  srv = AuthenticationService
  form = VerifyUserEmailForm()
  
  if form.validate_on_submit():
    try:
      srv.request_password_reset(form.email.data)
      flash(
        _('An email will been sent to reset you password. Please check your inbox.'),
        category='info')
      return redirect(url_for('main.index'))
    except UserNotFoundError:
      flash(
        _('An email will been sent to reset you password. Please check your inbox.'),
        category='info')
      return redirect(url_for('main.index'))
    except Exception as e:
      print('*' * 20, e)
      flash(_('Something went wrong, please try again later.'), category='warning')
  
  return render_template('auth/forgot-password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
  form = ResetPasswordForm()
  srv = AuthenticationService
  
  if form.validate_on_submit():
    try:
      srv.reset_password(
        token=token,
        new_password=form.password.data)
      flash(_('Password has been reset. You can login now.'), category='info')
      return redirect(url_for('auth.login'))
    except TokenError:
      flash(_('Invalid Token'), category='danger')
    except TokenPayloadError:
      flash(_('Invalid Token'), category='danger')
    except InvalidPasswordError:
      form.password.errors.append(_('Invalid Password'))
      
  return render_template('auth/reset-password.html', form=form)
