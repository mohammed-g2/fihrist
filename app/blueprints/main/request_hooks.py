from datetime import datetime, timedelta
from flask import request
from flask_login import current_user
from app.services import UserService
from . import main_bp


@main_bp.before_app_request
def before_request():
  # check for users activity
  # update users' last_seen every 5 minutes
  if current_user.is_authenticated and\
      request.endpoint == 'main.index' and\
      current_user.last_seen + timedelta(minutes=5) > datetime.utcnow():
    UserService.ping(current_user._get_current_object())
