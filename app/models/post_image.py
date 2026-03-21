from datetime import datetime
from app.ext import db


class PostImage(db.Model):
  __tablename__ = 'post_images'
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String())
  path = db.Column(db.String())
  thumbnail_url = db.Column(db.String())
  alt_text = db.Column(db.String(128))
  caption = db.Column(db.String(128))
  order = db.Column(db.Integer)
  created_at = db.Column(db.DateTime(), default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
  user = db.relationship('User', back_populates='post_images')
  post = db.relationship('Post', back_populates='images')
  
  def __repr__(self):
    return f'<PostImage { self.id }>'
