from flask import Flask, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel, _
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
babel = Babel()
mail = Mail()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message  = _('Please login to view this page.')
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

def init_flask_login() -> None:
  """
  Initialize the flask-login extension, attach user_loader and
  unauthorized_handler
  """
  from app.models import User
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(id)

  @login_manager.unauthorized_handler
  def unauthorized():
    if request.blueprint == 'api':
      abort(400)
    return redirect(url_for('auth.login'))


def get_locale(languages: list) -> str:
  """
  return locale stored in session, defaults to browser's choice
  
  :param languages: list of accepted languages
  :returns: locale string
  """
  def inner():
    locale = None
    if session and 'ar' in session.get('LANGUAGE'):
      locale = 'ar'
    elif session and 'en' in session.get('LANGUAGE'):
      locale = 'en'
    else:
      locale = request.accept_languages.best_match(languages)
    return locale
  return inner 
