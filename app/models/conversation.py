from datetime import datetime
from app.ext import db
from .participants import participants


class Conversation(db.Model):
  __tablename__ = 'conversations'
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  messages = db.relationship('Message', back_populates='conversation')
  members = db.relationship(
    'User', secondary=participants, back_populates='conversations')
  
  def __repr__(self):
    return f'<Conversation { self.id }>'
