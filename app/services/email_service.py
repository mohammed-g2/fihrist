from dataclasses import dataclass, field
from app.models import User
from app.utils.security import generate_timed_token
from app.utils.send_email import send_email
from app.errors import PasswordValidationError, EmailSendingError


@dataclass
class EmailMessage:
  to: str
  subject: str
  template: str
  context: dict = field(default_factory=dict)


class EmailService:
  
  @classmethod
  def confirm_account(cls, user: User) -> EmailMessage:
    token = generate_timed_token({'confirm': user.id})
    return EmailMessage(
      to=user.email,
      subject='Confirm Your Email',
      template='emails/auth/confirm',
      context=dict(user=user, token=token))
  
  @classmethod
  def update_email_address(cls, user: User, new_email: str) -> EmailMessage:
    token = generate_timed_token({
      'email': user.email,
      'new-email': new_email
    })
    return EmailMessage(
      to=new_email,
      subject='Change Email Address',
      template='emails/user/update-email',
      context=dict(token=token))
  
  @classmethod
  def change_password(cls, user: User) -> EmailMessage:
    token = generate_timed_token({'change-password': user.id})
    return EmailMessage(
      to=user.email,
      subject='Change Password',
      template='emails/user/change-password',
      context=dict(token=token))
  
  @classmethod
  def reset_password_request(cls, user: User) -> EmailMessage:
    token = generate_timed_token({'reset-password': user.email})
    return EmailMessage(
      to=user.email,
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
      - change_password
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
      'change_password': cls.change_password,
      'reset_password_request': cls.reset_password_request
    }
    
    msg = types.get(email_type)
    if not msg:
      raise ValueError('Incorrect email type.')
    
    data = msg(user=user, **kwargs)
    try:
      send_email(
        to=data.to, 
        subject=data.subject, 
        template=data.template, 
        **data.context)
    except Exception as e:
      raise EmailSendingError(e)
