from app.ext import db


participants = db.Table(
  'participants',
  db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
  db.Column('conversation_id', db.Integer, db.ForeignKey('conversations.id'), primary_key=True)
)
