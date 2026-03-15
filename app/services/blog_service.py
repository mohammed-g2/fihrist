import re
from app.ext import db
from app.models import User, Blog
from app.errors import DatabaseCommitError

 
class BlogService:
  
  @classmethod
  def create_blog(cls, user: User, name: str, description: str) -> bool:
    if not re.fullmatch(r'^[a-zA-Z0-9 ]+$', name):
      raise ValueError('Blog name can only contain letters, numbers and spaces')
    blog = Blog(
      name=name, description=description, user=user)
    blog.slag = name.replace(' ', '-')
    
    db.session.add(blog)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError()
    
    return True
