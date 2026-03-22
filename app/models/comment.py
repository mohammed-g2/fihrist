import re
import bleach
from datetime import datetime
from app.ext import db


class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  _content = db.Column(db.Text())
  created_at = db.Column(db.DateTime(), default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
  user = db.relationship('User', back_populates='comments')
  post = db.relationship('Post', back_populates='comments')
  
  def __repr__(self):
    return f'<Comment {self.id} >'
  
  @property
  def content(self) -> str:
    return self._content
  
  @content.setter
  def content(self, value: str):
    self._content = bleach.clean(value, tags=[], strip=True)
