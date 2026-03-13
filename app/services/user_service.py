from email_validator import validate_email, EmailNotValidError
from app.ext import db
from app.models import User
from app.models.value_objects import Username
from app.utils.security import decode_timed_token
from app.errors import (
  InvalidUsernameError, UsernameAlreadyExistsError, DatabaseCommitError,
  EmailAlreadyExistsError, TokenError, TokenPayloadError, InvalidEmailError)
from .email_service import EmailService


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
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  
  @classmethod
  def request_email_update(cls, user: User, new_email: str) -> bool:
    """
    Sends an email to the new email address to confirm change.
    
    :param user: `User` model instance
    :param new_email: new email address
    :returns: True if email is sent, False if not
    
    :raises EmailAlreadyExistsError: if email already exists in database
    :raises InvalidEmailError: if email is invalid
    :raises DatabaseCommitError: if failed to commit to database
    """
    if new_email == user.email:
      return False
    
    try:
      email_info = validate_email(new_email, check_deliverability=False)
      email = email_info.normalized
    except EmailNotValidError as e:
      raise InvalidEmailError(e)
    
    email_found = User.query.filter_by(email=email).first()
    if email_found:
      raise EmailAlreadyExistsError()
    
    try:
      EmailService.send_email(
        user=user,
        email_type='update_email_address', 
        new_email=email)
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  @classmethod
  def update_email(cls, user: User, token: str) -> bool:
    """
    Update user's email address using the `new-email` stored in token
    
    :param user: `User` model instance
    :param token: 
    :returns: True if change successful
    
    :raises TokenError: if failed to decode the token
    :raises TokenPayloadError: if `new-email` not in the token
    :raises DatabaseCommitError: if failed to commit to database
    """
    try:
      decoded = decode_timed_token(token)
    except TokenError as e:
      raise TokenError(e)
    
    email = decoded.get('new-email')
    if not email:
      raise TokenPayloadError()
    
    user.email = email
    db.session.add(user)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
