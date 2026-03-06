from flask import Flask


def create_app():
  app = Flask(__name__)
  
  
  from app.blueprints import (
    admin_bp, auth_bp, blog_bp, main_bp, post_bp, user_bp)
  
  app.register_blueprint(main_bp)
  app.register_blueprint(admin_bp, url_prefix='/admin')
  app.register_blueprint(auth_bp, url_prefix='/auth')
  app.register_blueprint(blog_bp, url_prefix='/blog')
  app.register_blueprint(post_bp, url_prefix='/post')
  app.register_blueprint(user_bp, url_prefix='/user')

  return app
