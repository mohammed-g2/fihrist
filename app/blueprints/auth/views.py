from flask import render_template, redirect, url_for, current_app, flash
from flask_login import current_user, login_user, logout_user
from flask_babel import _
from app.services import AuthenticationService
from app.errors import (
  LoginError, UsernameAlreadyExistsError, EmailAlreadyExistsError,
  DatabaseCommitError, InvalidPasswordError, InvalidUsernameError)
from . import auth_bp
from .forms import LoginForm, RegisterForm



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
def logout():
  if current_user.is_authenticated:
    logout_user()
  return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  
  form = RegisterForm()
  srv = AuthenticationService
  
  if form.validate_on_submit():
    current_app.logger.error('*' * 20 + 'Submited' + '*' * 20)
    try:
      srv.register_user(
        username=form.username.data,
        email=form.email.data,
        password=form.password.data)
      flash(_('You can login now.'), category='info')
      redirect(url_for('main.index'))
    except UsernameAlreadyExistsError:
      form.username.errors.append(_('Username already exists.'))
    except EmailAlreadyExistsError:
      form.email.errors.append(_('Email already exists.'))
    except InvalidPasswordError:
      form.password.errors.append(_('Invalid password'))
    except InvalidUsernameError:
      form.username.errors.append(_('Invalid username'))
    except Exception as e:
      flash(e)
      flash(_('Something went wrong, please try again later.'))

  return render_template('auth/register.html', form=form)
