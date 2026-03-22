from datetime import datetime
from sqlalchemy import and_
from app.ext import db
from app.models import User, Message, Conversation
from app.models.value_objects import Username, Email, Password
from app.utils.security import decode_timed_token
from app.errors import (
  InvalidUsernameError, UsernameAlreadyExistsError, DatabaseCommitError,
  EmailAlreadyExistsError, TokenError, TokenPayloadError, InvalidEmailError,
  PasswordValidationError)
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
      _username = Username(data.get('username'))

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
    
    _email = Email(value=new_email)
    
    email_found = User.query.filter_by(email=_email.value).first()
    if email_found:
      raise EmailAlreadyExistsError()

    EmailService.send_email(
      user=user,
      email_type='update_email_address', 
      new_email=_email.value)

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

    decoded = decode_timed_token(token)

    email = decoded.get('new-email')
    if not email:
      raise TokenPayloadError()
    
    _email = Email(value=email)
    
    user.email = _email.value
    db.session.add(user)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  
  @classmethod
  def request_password_change(cls, user: User, password: str) -> bool:
    """
    Send an email to the user to confirm password change
    
    :param user: `User` model instance
    :param password: user's password
    :returns: True if successful
    
    :raises PasswordValidationError: if faild to validate password
    :raises Exception: if failed to send email
    """
    if not user.verify_password(password):
      raise PasswordValidationError()
    EmailService.send_email(email_type='change_password', user=user)
    
    return True
  
  @classmethod
  def change_password(cls, user: User, token: str, new_password: str) -> bool:
    """
    Change user's password
    
    :param user: `User` model instance
    :param token:
    :param new_password:
    :returns: True if change successful
    
    :raises InvalidPasswordError: from `app.models.value_objects.Password`
    :raises TokenError: if token in invalid
    :raises DatabaseCommitError: if failed to commit to database
    """
    _password = Password(value=new_password)
    decoded = decode_timed_token(token)

    if decoded.get('change-password') != user.id:
      raise TokenPayloadError()
    
    user.password = _password.value
    db.session.add(user)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  @classmethod
  def ping(cls, user: User) -> None:
    """
    Update user's last seen
    
    :param user: `User` model instance
    :raises DatabaseCommitError: if failed to commit to database
    """
    user.last_seen = datetime.utcnow()
    db.session.add(user)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
  
  @classmethod
  def send_message(cls, sender: User, recipient: User, content: str) -> bool:
    """"""
    conversation = Conversation.query.filter(
      and_(
        Conversation.members.contains(sender),
        Conversation.members.contains(recipient))).first()
    
    if not conversation:
      conversation = Conversation()
      conversation.members.append(sender)
      conversation.members.append(recipient)
      db.session.add(conversation)
      try:
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        raise DatabaseCommitError(e)
    
    message = Message(
      sender=sender, 
      recipient=recipient, 
      content=content, 
      conversation=conversation)
    db.session.add(message)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
  
  @classmethod
  def mark_as_read(cls, user:User, conversation: Conversation):
    """"""
    for message in conversation.messages:
      if message.recipient_id == user.id:
        message.is_read = True
        db.session.add(message)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)

