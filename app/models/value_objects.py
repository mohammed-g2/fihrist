import re
from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError
from app.errors import (
  InvalidUsernameError, InvalidPasswordError, InvalidEmailError)

@dataclass(frozen=True)
class Username:
  value: str
  
  def __post_init__(self):
    if not re.match('^[A-Za-z][A-Za-z0-9_.]*$', self.value) or\
        len(self.value) > 36 or\
        len(self.value) < 3:
      raise InvalidUsernameError(
        'Username must have only letters, numbers, dots or underscores.')
  
  def __str__(self):
    return self.value


@dataclass(frozen=True)
class Password:
  value: str
  
  def __post_init__(self):
    if not re.match('^(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>])(?=.{6,}).*$', self.value)\
        or len(self.value) > 64:
      raise InvalidPasswordError(
        'Password must be 6 characters long, contain one number and one symbol.')
  
  def __str__(self):
    return '<Password>'
