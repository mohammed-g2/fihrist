from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from flask_babel import _
from app.models import User
from app.services import UserService
from app.errors import (
  InvalidUsernameError, UsernameAlreadyExistsError, TokenError,
  EmailAlreadyExistsError, InvalidEmailError, PasswordValidationError,
  InvalidPasswordError)
from . import user_bp
from .forms import (
  ChangePasswordForm, UpdateUserProfileForm, UpdateEmailForm,
  VerifyUserPasswordForm)


def profile_form_handler(form):
  if form.validate_on_submit():
    srv = UserService
    try:
      srv.update_profile(
        user=current_user._get_current_object(),
        data={'username': form.username.data, 'bio': form.bio.data})
      flash(_('Profile Updated'))
    except InvalidUsernameError:
      flash(_('Invalid Username'))
    except UsernameAlreadyExistsError:
      flash(_('Username Already Exists'))
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')


def email_form_handler(form):
  if form.validate_on_submit():
    srv = UserService
    try:
      srv.request_email_update(
        user=current_user._get_current_object(),
        new_email=form.email.data)
      flash(_('An email have been sent to confirm change. Please check your inbox'), category='info')
    except EmailAlreadyExistsError:
      flash(_('Email already exists'), category='warning')
    except InvalidEmailError:
      flash(_('Invalid Email.'), category='warning')
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')


def password_form_handler(form):
  if form.validate_on_submit():
    srv = UserService
    try:
      srv.request_password_change(
        user=current_user._get_current_object(),
        password=form.password.data)
      flash(_('A new email have been sent to change your password. Please check your inbox'))
    except PasswordValidationError:
      flash(_('Password is not correct'), category='danger')
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')


@user_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
  profile_form = UpdateUserProfileForm()
  email_form = UpdateEmailForm()
  password_form = VerifyUserPasswordForm()
  
  if request.method == 'POST':
    # check which form was submitted
    if profile_form.submit_profile.data:
      profile_form_handler(profile_form)
    elif email_form.submit_email.data:
      email_form_handler(email_form)
    elif password_form.submit_password.data:
      password_form_handler(password_form)
    return redirect(url_for('user.settings'))
  else:
    profile_form.bio.data = current_user.bio
  
  return render_template(
    'user/settings.html',
    profile_form=profile_form,
    email_form=email_form,
    password_form=password_form)


@user_bp.route('/update-email/<token>')
@login_required
def update_email(token):
  srv = UserService
  try:
    srv.update_email(
      user=current_user._get_current_object(),
      token=token)
    flash(_('Email Updated'), category='success')
  except TokenError:
    flash(_('Invalid Token'))
  except Exception as e:
    current_app.logger.exception(e)
    flash(_('Something went wrong, please try again later'), category='warning')
  return redirect(url_for('user.settings'))


@user_bp.route('/change-password/<token>', methods=['GET', 'POST'])
@login_required
def change_password(token):
  srv = UserService
  form = ChangePasswordForm()
  
  if form.validate_on_submit():
    try:
      srv.change_password(
        user=current_user._get_current_object(),
        token=token,
        new_password=form.password.data)
      flash(_('Password Changed'), category='success')
      return redirect(url_for('main.index'))
    except InvalidPasswordError:
      form.password.errors.append(
      _('Password must be 6 characters long, contain at least one number and one symbol'))
    except TokenError:
      flash(_('Invalid Token'), category='danger')
    except Exception as e:
      current_app.logger.exception(e)
      flash(_('Something went wrong, please try again later'), category='warning')
  
  return render_template('user/change-password.html', form=form)


@user_bp.route('/profile/<username>')
def profile(username):
  user = User.query.filter_by(username=username).first_or_404()
  
  return render_template('user/profile.html', user=user)
