from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_babel import _
from app.services import UserService
from app.errors import (
  InvalidUsernameError, UsernameAlreadyExistsError, DatabaseCommitError)
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
      flash(_('Something went wrong, please try again later.'), category='warning')


def email_form_handler(form):
  pass

  
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
