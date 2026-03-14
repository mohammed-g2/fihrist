from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app.ext import mail
from app.errors import EmailSendingError

def _send_async_mail(app, msg: str) -> None:
  with app.app_context():
    mail.send(msg)


def send_email(to: str, subject: str, template: str, **kwargs) -> None:
  """
  :param to: the recipient, user's email account
  :param subject: email subject
  :param template: email template without file extension, should have 2 versions
  ".txt" and ".html"
  """
  msg = Message(
    current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
    sender=current_app.config['MAIL_SENDER'],
    recipients=[to])
  msg.body = render_template(template + '.txt', **kwargs)
  msg.html = render_template(template + '.html', **kwargs)
  
  with ThreadPoolExecutor() as executor:
    send = executor.submit(
      _send_async_mail, current_app._get_current_object(), msg)
    try:
      return send.result()
    except Exception as e:
      raise EmailSendingError(e)
