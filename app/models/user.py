from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.ext import db
from app.models.value_objects import Password

class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  email = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String)
  confirmed = db.Column(db.Boolean(), default=False)
  
  def __repr__(self):
    return f'<User { self.username }>'
  
  @property
  def password(self):
    raise AttributeError('Password is not readable.')
  
  @password.setter
  def password(self, value: Password):
    self.password_hash = generate_password_hash(value)
  
  def verify_password(self, password: str) -> bool:
    return check_password_hash(self.password_hash, password)
