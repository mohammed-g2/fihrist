import re
from app.ext import db
from app.models import User, Blog, Post
from app.errors import DatabaseCommitError

 
class BlogService:
  
  @classmethod
  def create_blog(cls, user: User, name: str, description: str) -> bool:
    """
    Create a blog
    
    :param user: `User` model instance
    :param name: blog name, will be used to create slug
    :param description: blog description
    :returns: True if successful
    
    :raises ValueError: if blog name contains special characters
    :raises DatabaseCommitError: if failed to commit to database
    """
    if not re.fullmatch(r'^[a-zA-Z0-9 ]+$', name):
      raise ValueError('Blog name can only contain letters, numbers and spaces')
    blog = Blog(
      name=name, description=description, user=user)
    blog.slug = name.replace(' ', '-').strip('-').lower()
    
    db.session.add(blog)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError()
    
    return True
  
  @classmethod
  def create_post(cls, user: User, title: str, content: str, status: str) -> bool:
    """
    Create post
    
    :param user: `User` model instance
    :param title: post title, will be used to create slug
    :param content: post content
    :param status: post status `draft - published`
    :returns: True if successful
    
    :raises DatabaseCommitError: if failed to commit to database
    """
    post = Post(
      user=user, 
      title=title.strip(), 
      content=content.strip(), 
      status=status)
    # remove all special characters, keep letters, numbers and spaces
    slug = re.sub(r'[^a-zA-Z0-9 ]', '', title.strip())
    # replace spaces with hyphens
    slug = slug.replace(' ', '-').lower()
    post.slug = slug
    post.blog = user.blog
    
    db.session.add(post)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  @classmethod
  def update_post(cls, post: Post, title: str, content: str) -> bool:
    """"""
    slug = re.sub(r'[^a-zA-Z0-9 ]', '', title.strip())
    slug = slug.replace(' ', '-').lower()
    post.title = title.strip()
    post.content = content.strip()
    post.slug = slug
    
    db.session.add(post)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True

