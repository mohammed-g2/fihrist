import re
from datetime import datetime
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
      name=name.strip(), description=description.strip(), user=user)
    blog.create_slug()
    
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
    post_found = Post.query.filter_by(title=title).first()
    if post_found:
      raise ValueError('Title already exists in database')
    
    post = Post(
      user=user, 
      title=title.strip(), 
      content=content.strip(), 
      status=status)
    post.blog = user.blog
    post.create_slug()
    
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
    if title != post.title:
      post_found = Post.query.filter_by(title=title).first()
      if post_found:
        raise ValueError('Title already exists in database')
    
    post.title = title.strip()
    post.content = content.strip()
    post.updated_at = datetime.utcnow()
    post.create_slug()
    
    db.session.add(post)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True

