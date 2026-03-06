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
#login_manager = LoginManager()
