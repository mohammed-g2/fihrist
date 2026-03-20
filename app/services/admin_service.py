from app.ext import db
from app.models import User, Role
from app.errors import DatabaseCommitError

class AdminService:
  
  @classmethod
  def edit_user(cls, user: User, confirmed: bool, role_id: int) -> bool:
    """
    Edit given user
    
    :param user: `User` model instance
    :param confirmed: whether user's email is confirmed
    :param role_id: role chosen for the user
    :returns: True if successful
    :raises DatabaseCommitError: if failed to commit to database
    """
    role = Role.query.get(role_id)
    if not role:
      raise ValueError('Role does not exist')
    user.confirmed = confirmed
    user.role = role
    db.session.add(user)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
  
    return True

  @classmethod
  def delete_user(cls, user: User) -> bool:
    """
    Delete given user
    
    :param user: `User` model instance
    :returns: True if successful
    :raises DatabaseCommitError: if failed to commit to database
    """
    db.session.delete(user)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
