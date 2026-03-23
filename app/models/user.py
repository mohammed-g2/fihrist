import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_login import UserMixin
from app.ext import db
from .permission import Permission
from .message import Message
from .participants import participants


class Follow(db.Model):
  __tablename__ = 'follows'
  follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
  followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  email = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String)
  confirmed = db.Column(db.Boolean(), default=False)
  bio = db.Column(db.Text())
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  avatar_hash = db.Column(db.String(64))
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  role = db.relationship('Role', back_populates='users')
  blog = db.relationship('Blog', back_populates='user', uselist=False)
  posts = db.relationship('Post', back_populates='user', lazy='dynamic')
  comments = db.relationship('Comment', back_populates='user', lazy='dynamic')
  post_images = db.relationship('PostImage', back_populates='user', lazy='dynamic')
  sent_messages = db.relationship(
    'Message', back_populates='sender', lazy='dynamic', foreign_keys='Message.sender_id')
  received_messages = db.relationship(
    'Message', back_populates='recipient', lazy='dynamic', foreign_keys='Message.sender_id')
  conversations = db.relationship(
    'Conversation', secondary=participants, back_populates='members')
  followed = db.relationship(
    'Follow',
    foreign_keys=[Follow.follower_id], 
    backref=db.backref('follower', lazy='joined'),
    lazy='dynamic',
    cascade='all, delete-orphan')
  followers = db.relationship(
    'Follow',
    foreign_keys=[Follow.followed_id],
    backref=db.backref('followed', lazy='joined'),
    lazy='dynamic',
    cascade='all, delete-orphan')
  
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
  
  def has_unread_messages(self) -> bool:
    found_unread_msg = Message.query.filter_by(recipient_id=self.id, is_read=False).first()
    return found_unread_msg is not None
  
  def follow(self, user: 'User') -> None:
    if not self.is_following(user):
      f = Follow(follower=self, followed=user)
      db.session.add(f)
  
  def unfollow(self, user: 'User') -> None:
    f = self.followed.filter_by(followed_id=user.id).first()
    if f:
      db.session.delete(f)
  
  def is_following(self, user: 'User') -> bool:
    if user.id is None:
      return False
    return self.followed.filter_by(followed_id=user.id).first() is not None
  
  def is_followed_by(self, user: 'User') -> bool:
    if user.id is None:
      return False
    return self.followers.filter_by(follower_id=user.id).first() is not None
