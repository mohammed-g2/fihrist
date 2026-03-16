from datetime import datetime
from app.ext import db


class Post(db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), index=True)
  content = db.Column(db.Text())
  slug = db.Column(db.String())
  status = db.Column(db.String()) # draft - published
  created_at = db.Column(db.DateTime(), default=datetime.utcnow)
  updated_at = db.Column(db.DateTime())
  blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  blog = db.relationship('Blog', back_populates='posts')
  user = db.relationship('User', back_populates='posts')
  
  def __repr__(self):
    return f'<Post { self.title }>'
