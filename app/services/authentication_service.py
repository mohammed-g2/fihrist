from app.ext import db
from app.models import User
from app.models.value_objects import Username, Password
from app.errors import (
  UserNotFoundError, PasswordValidationError, EmailAlreadyExistsError,
  UsernameAlreadyExistsError, DatabaseCommitError)

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
    
    return True
