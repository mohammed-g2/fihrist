from flask import Flask
from app.ext import (
  db, migrate, mail, csrf, babel, login_manager, init_flask_login, 
  get_locale)
from config import options


def create_app(config_name: str) -> Flask:
  """
  Create and configure the application.
  
  :param config_name: configuration choosen from config.options
  :returns: application instance
  """
  conf = options[config_name]
  
  app = Flask(__name__)
  
  app.config.from_object(conf)
  conf.init_app(app)
  locale_selector = get_locale(app.config['LANGUAGES'])
  
  db.init_app(app)
  mail.init_app(app)
  csrf.init_app(app)
  babel.init_app(app, locale_selector=locale_selector)
  login_manager.init_app(app)
  init_flask_login()
  
  if app.config.get('ENV') != 'production':
    migrate.init_app(app, db)
  
  with app.app_context():
    from app.models import (
      User, Role, Permission, Blog, Post, Comment, Category, PostImage)
  
  @app.context_processor
  def create_template_context():
    _locale = locale_selector()
    _dir = 'rtl' if 'ar' in _locale else 'ltr'
    return dict(_locale=_locale, _dir=_dir, Permission=Permission)
  
  
  from app.blueprints import (
    admin_bp, auth_bp, blog_bp, main_bp, user_bp)
  
  app.register_blueprint(main_bp)
  app.register_blueprint(admin_bp, url_prefix='/admin')
  app.register_blueprint(auth_bp, url_prefix='/auth')
  app.register_blueprint(blog_bp, url_prefix='/blog')
  app.register_blueprint(user_bp, url_prefix='/user')

  return app
