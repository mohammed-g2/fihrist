from flask import Flask
from app.ext import db, migrate, mail, csrf, babel
from config import options

def create_app(config_name):
  conf = options[config_name]
  
  app = Flask(__name__)
  
  app.config.from_object(conf)
  conf.init_app(app)
  
  db.init_app(app)
  mail.init_app(app)
  csrf.init_app(app)
  babel.init_app(app)
  
  if app.config.get('ENV') != 'production':
    migrate.init_app(app, db)
    
  with app.app_context():
    from app.models import User
    
  
    @app.context_processor
    def create_template_context():
      return dict(db=db, User=User)
  
  
  from app.blueprints import (
    admin_bp, auth_bp, blog_bp, main_bp, post_bp, user_bp)
  
  app.register_blueprint(main_bp)
  app.register_blueprint(admin_bp, url_prefix='/admin')
  app.register_blueprint(auth_bp, url_prefix='/auth')
  app.register_blueprint(blog_bp, url_prefix='/blog')
  app.register_blueprint(post_bp, url_prefix='/post')
  app.register_blueprint(user_bp, url_prefix='/user')

  return app
