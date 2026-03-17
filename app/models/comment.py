import re
import bleach
from datetime import datetime
from app.ext import db


class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  content_raw = db.Column(db.Text())
  created_at = db.Column(db.DateTime(), default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
  user = db.relationship('User', back_populates='comments')
  post = db.relationship('Post', back_populates='comments')
  
  def __repr__(self):
    return f'<Comment {self.id} >'
  
  @property
  def content(self):
    return self.content_html
  
  @content.setter
  def content(self, value: str):
    self.content_raw = value
    self.content_html = self.clean(value)
  
  def clean(self, text: str) -> None:
    """
    Remove unwanted tags from the content
    """
    ALLOWED_TAGS = [
      'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 
      'li', 'ol', 'ul', 'strong', 'p', 'br', 'span', 'h1', 'h2', 'h3', 
      'h4', 'h5', 'h6', 'img', 'pre', 's', 'u', 'strike', 'sub', 'sup', 
      'video', 'div']

    ALLOWED_ATTRIBUTES = {
      'a': ['href', 'title', 'target', 'rel'],
      'img': ['src', 'alt', 'width', 'height'],
      'video': ['src', 'controls', 'width', 'height'],
      '*': ['class'], 
    }
    
    return bleach.clean(
      text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
  
  def plain_content(self) -> str:
    """
    Provide the content without tags
    """
    if self.content:
      return bleach.clean(self.content[:80], tags=[], strip=True)
    return ''
