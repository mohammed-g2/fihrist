from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_babel import _
from app.services import UserService
from app.errors import (
  InvalidUsernameError, UsernameAlreadyExistsError, DatabaseCommitError,
  EmailAlreadyExistsError, InvalidEmailError, TokenError)
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
    except InvalidUsernameError:
      flash(_('Invalid Username.'))
    except UsernameAlreadyExistsError:
      flash(_('Username Already Exists.'))
    except DatabaseCommitError:
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
      flash(_('Email already exists.'), category='warning')
    except InvalidEmailError:
      flash(_('Invalid Email.'), category='warning')
    except Exception as e:
      flash(_('Something went wrong, please try again later'), category='warning')


def password_form_handler(form):
  pass


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
  except TokenError:
    flash(_('Invalid Token'))
  except DatabaseCommitError:
    flash(_('Something went wrong, please try again later'), category='warning')
  return redirect(url_for('user.settings'))
