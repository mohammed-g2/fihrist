
# Authentication Errors
class AuthError(Exception):
  """Base class for authentication errors."""
  def __init__(self, message='Authentication failed', status_code=401):
    super().__init__(message)
    self.status_code = status_code


class LoginError(AuthError):
  """Base class for user login errors."""
  pass


class UserNotFoundError(LoginError): pass


class PasswordValidationError(LoginError): pass


class RegistrationError(AuthError):
  """Base class for user registration errors."""
  def __init__(self, message='Registration Failed', status_code=409):
    super().__init__(message, status_code)


class EmailAlreadyExistsError(RegistrationError): pass


class UsernameAlreadyExistsError(RegistrationError): pass


class InvalidUsernameError(RegistrationError): pass


class InvalidPasswordError(RegistrationError): pass


class InvalidEmailError(RegistrationError): pass

# Token Errors
class TokenError(AuthError):
  """Base class for all token related errors."""
  def __init__(self, message='Invalid Token', status_code=401):
    super().__init__(message, status_code)


class TokenExpiredError(TokenError):
  def __init__(self, message='Token Expired'):
    super().__init__(message)


class TokenInvalidSignatureError(TokenError):
  def __init__(self, message='Invalid Signature Error'):
    super().__init__(message)


class TokenMalformedError(TokenError):
  def __init__(self, message='Malformed Token'):
    super().__init__(message)


class TokenPayloadError(TokenError):
  def __init__(self, message='Payload does not match the context'):
    super().__init__(self, message)


# General process errors
class ProcessError(Exception):
  """Base class for all process failure related errors."""
  def __init__(self, message='Process failed.', status_code=500):
    super().__init__(message)


# Database Error
class DatabaseCommitError(ProcessError):
  """Raised when failed to commit to database"""
  def __init__(self, message='Failed to commit to database'):
    super().__init__(message)

class EmailSendingError(ProcessError):
  """Raised when failed to send email"""
  def __init__(self, message='Failed to send email'):
    super().__init__(message)

# General errors
class InvalidPostTitle(Exception): pass

class InvalidBlogName(Exception): pass
