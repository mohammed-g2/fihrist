from datetime import datetime
from app.ext import db


class Blog(db.Model):
  __tablename__ = 'blogs'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), index=True)
  slug = db.Column(db.String(32))
  description = db.Column(db.String(128))
  created_at = db.Column(db.DateTime(), default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
  user = db.relationship('User', back_populates='blog')
  posts = db.relationship('Post', back_populates='blog')
  
  def __repr__(self):
    return f'<Blog { self.name }>'
