import re
import bleach
from datetime import datetime
from app.ext import db


class Post(db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), index=True, unique=True)
  content_raw = db.Column(db.Text())
  content_html = db.Column(db.Text())
  slug = db.Column(db.String(), index=True)
  status = db.Column(db.String()) # draft - published
  created_at = db.Column(db.DateTime(), default=datetime.utcnow)
  updated_at = db.Column(db.DateTime())
  blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  blog = db.relationship('Blog', back_populates='posts')
  user = db.relationship('User', back_populates='posts')
  comments = db.relationship('Comment', back_populates='post', lazy='dynamic')
  
  def __repr__(self):
    return f'<Post { self.title }>'
  
  @property
  def content(self):
    return self.content_html
  
  @content.setter
  def content(self, value: str):
    self.content_raw = value
    self.content_html = self.clean(value)
  
  def create_slug(self) -> None:
    """
    Create slug for the post using the title
    """
    # remove all special characters, keep letters, numbers and spaces
    slug = re.sub(r'[^a-zA-Z0-9 ]', '', self.title.strip())
    # replace spaces with hyphens
    slug = slug.replace(' ', '-').lower()
    self.slug = slug
  
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
