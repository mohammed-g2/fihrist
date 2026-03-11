from flask import render_template
from flask_wtf.csrf import CSRFError
from . import main_bp


@main_bp.app_errorhandler(404)
def page_not_found(e):
  return render_template('errors/404.html'), 404


@main_bp.app_errorhandler(400)
def bad_request(e):
  return render_template('errors/400.html'), 400

@main_bp.app_errorhandler(CSRFError)
def csrf_error(e):
  return render_template('errors/400.html'), 400


@main_bp.app_errorhandler(401)
def unauthorized(e):
  return render_template('errors/401.html'), 401


@main_bp.app_errorhandler(403)
def forbidden(e):
  return render_template('errors/403.html'), 403


@main_bp.app_errorhandler(405)
def method_not_allowed(e):
  return render_template('errors/405.html'), 403


@main_bp.app_errorhandler(500)
def internal_server_error(e):
  return render_template('errors/500.html'), 500


@main_bp.app_errorhandler(503)
def service_unavailable(e):
  return render_template('errors/503.html'), 503
