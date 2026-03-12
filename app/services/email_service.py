from dataclasses import dataclass, field
from app.models import User
from app.utils.security import generate_timed_token
from app.utils.send_email import send_email
from app.errors import (
  EmailAlreadyExistsError, PasswordValidationError, UserNotFoundError)


@dataclass
class EmailMessage:
  to: str
  subject: str
  template: str
  context: dict = field(default_factory=dict)


class EmailService:
  
  @classmethod
  def confirm_account(cls, user: User, **kwargs) -> EmailMessage:
    token = generate_timed_token({'confirm': user.id})
    return EmailMessage(
      to=user.email,
      subject='Confirm Your Email',
      template='emails/auth/confirm',
      context=dict(user=user, token=token))
  
  @classmethod
  def update_email_address(cls, user: User, **kwargs) -> EmailMessage:
    email_found = User.get_by_email(email=kwargs.get('new_email'))
    if email_found:
      raise EmailAlreadyExistsError()

    token = generate_timed_token({
      'email': user.email,
      'new-email': kwargs.get('new_email')
    })
    return EmailMessage(
      to=kwargs.get('new_email'),
      subject='Change Email Address',
      template='emails/user/update-email',
      context=dict(token=token))
  
  @classmethod
  def update_password(cls, user: User, **kwargs) -> EmailMessage:
    if not user.verify_password(kwargs.get('password')):
        raise PasswordValidationError()
    
    token = generate_timed_token({'change-password': user.id})
    return EmailMessage(
      to=user.email,
      subject='Change Password',
      template='emails/user/change-password',
      context=dict(token=token))
  
  @classmethod
  def reset_password_request(cls, user: User, **kwargs) -> EmailMessage:
    user_found = User.get_by_email(kwargs.get('email'))
    if not user_found:
      raise UserNotFoundError()

    token = generate_timed_token({'reset-password': kwargs.get('email')})
    return EmailMessage(
      to=kwargs.get('email'),
      subject='Reset Password',
      template='emails/auth/reset-password',
      context=dict(token=token))
  
  @classmethod
  def send_email(cls, user: User, email_type: str, **kwargs) -> None:
    """
    Send email to user's email address, if type is update_email_address,
    email is sent to the new email address 
    
    :param user: User class instance
    :param type: is one of 
      - confirm_account
      - update_email_address
      - update_password
      - reset_password_request
    
    :param new_email: required if type is update_email_address
    :param email: required if type is reset_password_request
    :param password: required if type is update_password
    
    :raises EmailAlreadyExistsError: if type is update_email_address
    :raises PasswordValidationError: if type is update_password
    :raises UserNotFoundError: if type is reset_password_request
    """
    types = {
      'confirm_account': cls.confirm_account,
      'update_email_address': cls.update_email_address,
      'update_password': cls.update_password,
      'reset_password_request': cls.reset_password_request
    }
    
    msg = types.get(email_type)
    if not msg:
      raise ValueError('Incorrect email type.')
    
    data = msg(user=user, **kwargs)
    
    send_email(
      to=data.to, 
      subject=data.subject, 
      template=data.template, 
      **data.context)
