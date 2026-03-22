from datetime import datetime, timedelta
from flask import request, current_app
from flask_sqlalchemy.record_queries import get_recorded_queries
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


@main_bp.after_app_request
def after_request(response):
  # log slow database queries
  for query in get_recorded_queries():
    if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
      current_app.logger.warning(
        f'Slow query: { query.statement }\n'
        f'Parameters: { query.parameters }\n'
        f'Duration: { query.duration }\n')
  
  return response
