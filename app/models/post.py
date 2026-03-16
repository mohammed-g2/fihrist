import re
from datetime import datetime
from app.ext import db


class Post(db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), index=True, unique=True)
  content = db.Column(db.Text())
  slug = db.Column(db.String(), index=True)
  status = db.Column(db.String()) # draft - published
  created_at = db.Column(db.DateTime(), default=datetime.utcnow)
  updated_at = db.Column(db.DateTime())
  blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  blog = db.relationship('Blog', back_populates='posts')
  user = db.relationship('User', back_populates='posts')
  
  def __repr__(self):
    return f'<Post { self.title }>'
  
  def create_slug(self) -> None:
    # remove all special characters, keep letters, numbers and spaces
    slug = re.sub(r'[^a-zA-Z0-9 ]', '', self.title.strip())
    # replace spaces with hyphens
    slug = slug.replace(' ', '-').lower()
    self.slug = slug
