import enum
import bleach
from datetime import datetime
from app.ext import db


class Message(db.Model):
  __tablename__ = 'messages'
  id = db.Column(db.Integer, primary_key=True)
  _content = db.Column(db.String(128))
  is_read = db.Column(db.Boolean(), default=False)
  created_at = db.Column(db.DateTime(), default=datetime.utcnow)
  conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
  sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  conversation = db.relationship('Conversation', back_populates='messages')
  sender = db.relationship(
    'User', back_populates='sent_messages', foreign_keys=[sender_id])
  recipient = db.relationship(
    'User', back_populates='received_messages', foreign_keys=[recipient_id])
  
  
  def __repr__(self):
    return f'<Message { self.id }>'
  
  @property
  def content(self) -> str:
    return self._content
  
  @content.setter
  def content(self, value: str):
    self._content = bleach.clean(value, tags=[], strip=True)
