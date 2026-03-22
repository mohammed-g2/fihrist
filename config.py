import os
import secrets
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
  # App config
  ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
  ENV = os.environ.get('ENV')
  LANGUAGES = ['en', 'ar']
  ITEMS_PER_PAGE = 5
  SSL_REDIRECT = os.environ.get('SSL_REDIRECT')
  # Mail Server config
  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT'))
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
  # Mail Sender config
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  MAIL_SUBJECT_PREFIX = '[Fihrist]'
  MAIL_SENDER = 'Fihrist Admin <Ghusn@email.com>'
  # Database config
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_RECORD_QUERIES = os.environ.get('RECORD_QUERIES') == 'true'
  SLOW_DB_QUERY_TIME = 0.5
  # Image upload
  UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
  ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
  MAX_CONTENT_LENGTH = 10 * 1024 * 1024 # 10MB
  
  @staticmethod
  def init_app(app: Flask) -> None:
    pass


class DevelopmentConfig(Config):
  DEBUG = True
  ENV = 'development'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or\
    f'sqlite:///{os.path.join(basedir, "data", "dev.sqlite")}'
    
  @staticmethod
  def init_app(app: Flask) -> None:
    import logging
    import sys
    
    Config.init_app(app)
    app.logger.handlers.clear()
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
      '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s')
    handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = False


class TestingConfig(Config):
  TESTING = True
  WTF_CSRF_ENABLED = False
  ENV = 'testing'
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or\
    'sqlite://'


class ProductionConfig(Config):
  ENV = 'production'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or\
    f'sqlite:///{os.path.join(basedir, "data", "data.sqlite")}'
  
  def init_app(app: Flask) -> None:
    import logging
    from logging.handlers import RotatingFileHandler
    
    Config.init_app(app)
    
    logs_dir = os.path.join(basedir, 'tmp', 'logs')
    if not os.path.exists(logs_dir):
      os.mkdir(logs_dir)
    
    file_handler = RotatingFileHandler(
      os.path.join(logs_dir, 'app.log'), maxBytes=10240, backupCount=10)
    formatter = logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application start')


options = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig
}
