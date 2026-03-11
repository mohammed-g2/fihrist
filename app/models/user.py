from werkzeug.security import generate_password_hash, check_password_hash
from app.ext import db


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  email = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String)
  
  def __repr__(self):
    return f'<User { self.username }>'
  
  @property
  def password(self):
    raise AttributeError('Password is not readable.')
  
  @password.setter
  def password(self, value: str):
    self.password_hash = generate_password_hash(value)
  
  def verify_password(self, password: str) -> bool:
    return check_password_hash(self.password_hash, password)
