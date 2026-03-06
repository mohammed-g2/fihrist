from flask import url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
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
login_manager.login_message  = 'Please login to view this page.'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

def init_flask_login(user_service):
  from app.models import User
  @login_manager.user_loader
  def load_user(id):
    return User.get(id)

  @login_manager.unauthorized_handler
  def unauthorized():
    if request.blueprint == 'api':
      abort(400)
    return redirect(url_for('auth.login'))
