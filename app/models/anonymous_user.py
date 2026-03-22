from flask_login import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):
  def can(self, permisison: int) -> bool:
    return False
  
  def is_admin(self) -> bool:
    return False
  
  def is_mod(self) -> bool:
    return False
  
  def has_unread_messages(self) -> bool:
    return False
