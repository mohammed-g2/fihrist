import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_login import UserMixin
from app.ext import db
from .permission import Permission

class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  email = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String)
  confirmed = db.Column(db.Boolean(), default=False)
  bio = db.Column(db.Text())
  member_since = db.Column(db.DateTime, default=datetime.utcnow)
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  avatar_hash = db.Column(db.String(64))
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  role = db.relationship('Role', back_populates='users')
  blog = db.relationship('Blog', back_populates='user', uselist=False)
  posts = db.relationship('Post', back_populates='user', lazy='dynamic')
  
  def __repr__(self):
    return f'<User { self.username }>'
  
  @property
  def password(self):
    raise AttributeError('Password is not readable.')
  
  @password.setter
  def password(self, value: str):
    self.password_hash = generate_password_hash(value)
  
  def verify_password(self, password: str) -> bool:
    """Check if given password is the same of the user's."""
    return check_password_hash(self.password_hash, password)
  
  def can(self, permission: int) -> bool:
    """Check if user have the given permission."""
    if self.role is not None:
      return self.role.has_permission(permission)
    return False
  
  def is_admin(self) -> bool:
    """Check if user have admin permission."""
    return self.can(Permission.ADMIN)
  
  def is_mod(self) -> bool:
    """Check if user have moderator permission."""
    return self.can(Permission.MODERATE)
  
  def md5_hash(self) -> str:
    """Generate md5 hash using user's email."""
    return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
  
  def gavatar(self, size: int=100, generator: str='identicon', rating: str='g') -> str:
    """
    Generate Gravatar image url
    
    :param size: the image size, default 100
    :param generator: default image generator for users without avatar in
    Gravatar service, options:
    '404'|'mm'|'identicon'|'monsterid'|'wavatar'|'retro'|'blank'
    :param rating: image rating, options: 'g'|'pg'|'r'|'x'
    """
    if request.is_secure:
      url = 'https://secure.gravatar.com/avatar'
    else:
      url = 'http://www.gravatar.com/avatar'
    
    return f'{url}/{self.avatar_hash}?s={size}&d={generator}&r={rating}'
