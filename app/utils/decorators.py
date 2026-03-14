from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from app.models import Permission


def permission_required(permission):
  def decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      srv = current_app.authorization_service
      if not srv.has_permission(current_user.role, permission):
        abort(403)
      return f(*args, **kwargs)
    return decorated
  return decorator


def admin_required(f):
  return permission_required(Permission.ADMIN)(f)


def mod_required(f):
  return permission_required(Permission.MODERATE)(f)
