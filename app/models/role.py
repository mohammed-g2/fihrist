from app.ext import db


class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  default = db.Column(db.Boolean, default=False)
  permissions = db.Column(db.Integer)
  users = db.relationship('User', backref='role', lazy='dynamic')
  
  def __repr__(self):
    return f'<Role { self.name }>'
  
  def __init__(self, **kwargs):
    super(Role, self).__init__(**kwargs)
    if self.permissions is None:
      self.permissions = 0
  
