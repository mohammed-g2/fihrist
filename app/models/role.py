from app.ext import db
from app.errors import DatabaseCommitError

class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  default = db.Column(db.Boolean, default=False)
  permissions = db.Column(db.Integer)
  users = db.relationship('User', back_populates='role', lazy='dynamic')
  
  def __repr__(self):
    return f'<Role { self.name }>'
  
  def __init__(self, **kwargs):
    super(Role, self).__init__(**kwargs)
    if self.permissions is None:
      self.permissions = 0
  
  def add_permission(self, permission: int) -> None:
    """Add given permission to the role"""
    if not self.has_permission(permission):
      self.permissions += permission
    
  def remove_permission(self, permission: int) -> None:
    """Remove given permission from the role"""
    if self.has_permission(permission):
      self.permissions -= permission
  
  def reset_permissions(self) -> None:
    """Remove all permissions from the role"""
    self.permissions = 0
  
  def has_permission(self, permission: int) -> bool:
    """Check if role has the given permission"""
    return self.permissions & permission == permission
  
  @staticmethod
  def set_roles(roles: dict, default: str) -> None:
    """
    Create new roles or update existing ones
    
    :param roles: a dictionary of role names and permissions
    :param default: the default role for users
    """
    for role_name, permissions in roles.items():
      role = Role.query.filter_by(name=role_name).first()
      if role:
        role.reset_permissions()
      else:
        role = Role(name=role_name)
      
      if role.name == default:
        role.default = True
      
      for perm in permissions:
        role.add_permission(perm)
      
      db.session.add(role)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
