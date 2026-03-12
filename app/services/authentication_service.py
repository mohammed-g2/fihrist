from flask import current_app
from email_validator import validate_email, EmailNotValidError
from app.ext import db
from app.utils.security import decode_timed_token
from app.models import User
from app.models.value_objects import Username, Password
from app.errors import (
  UserNotFoundError, PasswordValidationError, EmailAlreadyExistsError,
  UsernameAlreadyExistsError, DatabaseCommitError, TokenError,
  TokenPayloadError, InvalidPasswordError)
from .email_service import EmailService


class AuthenticationService:
  
  @classmethod
  def login_user(cls, email: str, password: str) -> User:
    """
    Check if user is able to login, raises `LoginError`.
    
    :param username: user's username
    :param password: user's password
    :returns: User instance if user can login
    :raises UserNotFoundError: if couldn't find user with given email
    :raises PasswordValidationError: if password is incorrect
    """
    user = User.query.filter_by(email=email).first()
    if user is None:
      raise UserNotFoundError()
    if not user.verify_password(password):
      raise PasswordValidationError()
    return user
  
  @classmethod
  def register_user(cls, username: str, email: str, password: str) -> bool:
    """
    Register a new user and commit to database, raises 
    `RegistrationError` or `DatabaseCommitError`.
    
    :param username: user's username
    :param email: user's email
    :param password: user's password
    :returns: True if registeration complete
    :raises EmailAlreadyExistsError: if email already exists
    :raises UsernameAlreadyExistsError: if username already exists
    :raises DatabaseCommitError: if failed to commit to database
    :raises InvalidUsernameError: if username is invalid
    :raises InvalidPasswordError: if password is invalid
    """
    username_found = User.query.filter_by(username=username).first()
    if username_found:
      raise UsernameAlreadyExistsError()
    email_found = User.query.filter_by(email=email).first()
    if email_found:
      raise EmailAlreadyExistsError()
    
    
    _username = Username(value=username)
    _password = Password(value=password)
    
    user = User(
      username=_username.value, 
      email=email, 
      password=_password.value)
    db.session.add(user)
    try:
      db.session.commit()
    except Exception as e:
      raise DatabaseCommitError(e)
    
    EmailService.send_email(user, 'confirm_account')
    try:
      EmailService
    except Exception as e:
      current_app.logger.error(e)
  
    return True

  @classmethod
  def confirm_user(cls, user: User, token: str) -> bool:
    """
    Changes `User.confirmed` flag
    
    :param user: `User` model instance
    :returns: True if change is successful
    :raises DatabaseCommitError: if error occurred while committing to database
    """
    try:
      decoded = decode_timed_token(token)
    except TokenError as e:
      raise TokenError(e)
    
    if decoded.get('confirm') != user.id:
      raise TokenPayloadError()
    
    user.confirmed = True
    db.session.add(user)
    
    try:
      db.session.commit()
    except Exception as e:
      raise DatabaseCommitError(e)
    
    return True

  @classmethod
  def request_password_reset(cls, email: str) -> bool:
    """
    Request password change for users who forgot their passwords
    
    :param email: user's email address
    :returns: True if reset password email is sent
    :raises UserNotFoundError: if user with given email not found
    :raises Exception: if failed to send email
    """
    user = User.query.filter_by(email=email).first()
    if not user:
      raise UserNotFoundError()
    try:
      EmailService.send_email(email_type='reset_password_request', user=user)
    except Exception as e:
      raise Exception(e)
    
    return True
  
  @classmethod
  def reset_password(cls, token: str, new_password: str) -> bool:
    """
    Reset user password
    
    :param token:
    :param new_password:
    :returns: True if password changed
    
    :raises TokenError: if token missing 'reset-password'
    :raises InvalidPasswordError: if new_password doesn't match `Password` value object  
    :raises TokenPayloadError: if email in 'reset-password' is invalid
    :raises TokenPayloadError: if user with given not found in database
    :raises DatabaseCommitError: if failed to commit to database
    """
    decoded = decode_timed_token(token)
    email = decoded.get('reset-password')
    if email is None:
      raise TokenError()
    
    try:
      _password = Password(new_password)
    except InvalidPasswordError:
      raise InvalidPasswordError()
    
    try:
      email_info = validate_email(email, check_deliverability=False)
      email = email_info.normalized
    except EmailNotValidError as e:
      raise TokenPayloadError(e)
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
      raise TokenPayloadError()
    
    user.password = _password.value
    db.session.add(user)
    try:
      db.session.commit()
    except Exception as e:
      raise DatabaseCommitError(e)
    
    return True
