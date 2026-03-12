from app.ext import db
from app.models import User
from app.models.value_objects import Username
from app.errors import (
  InvalidUsernameError, UsernameAlreadyExistsError, DatabaseCommitError)


class UserService:
  
  @classmethod
  def update_profile(cls, user: User, data: dict) -> bool:
    """
    Update user profile info
    
    :param user: `User` model instance
    :param data: user profile data to be updated
    :returns: True if update is successful
    
    :raises InvalidUsernameError: if username doesn't confirm to `app.models.value_objects.Username`
    :raises UsernameAlreadyExistsError: if username already registered in the database
    :raises DatabaseCommitError: if failed to commit to database 
    """
    if data.get('username') and data.get('username') != user.username:
      try:
        _username = Username(data.get('username'))
      except InvalidUsernameError:
        raise InvalidUsernameError()
      
      username_found = User.query.filter_by(username=_username.value).first()
      if username_found:
        raise UsernameAlreadyExistsError()
      
      user.username = _username.value
      
    if data.get('bio'):
      user.bio = data.get('bio')
    
    db.session.add(user)
    try:
      db.session.commit()
    except Exception as e:
      raise DatabaseCommitError(e)
    
    return True
