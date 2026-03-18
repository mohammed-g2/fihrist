import re
from app.ext import db


class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  slug = db.Column(db.String(32), index=True, unique=True)
  posts = db.relationship('Post', back_populates='category', lazy='dynamic')
  
  def __repr__(self):
    return f'<Category { self.name }>'
  
  def create_slug(self) -> None:
    # remove all special characters, keep letters, numbers and spaces
    slug = re.sub(r'[^a-zA-Z0-9 ]', '', self.name.strip())
    # replace spaces with hyphens
    slug = slug.replace(' ', '-').lower()
    self.slug = slug
 
