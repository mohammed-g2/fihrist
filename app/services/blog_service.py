import os
import re
import string
import random
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app, url_for
from app.ext import db
from app.models import User, Blog, Post, Comment, Category, PostImage
from app.errors import DatabaseCommitError, InvalidBlogName, InvalidPostTitle

 
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
      raise InvalidBlogName('Blog name can only contain letters, numbers and spaces')
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
  def save_post_image(cls, image, user, post):
    allowed_ext = current_app.config['ALLOWED_EXTENSIONS']
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    code = ''.join(random.choices(string.ascii_letters, k=4))
    filename = f'{ user.username }-{ code }-{secure_filename(image.filename)}'
    image_path = os.path.join(uploads_dir, filename)
    url = url_for('static', filename=f'uploads/{ filename }')
    
    if not '.' in filename or not filename.rsplit('.', 1)[1].lower() in allowed_ext:
      raise ValueError('Wrong image extension')
    
    all_images = post.images.all()
    if all_images != []:
      previous_image = all_images[0]
      if previous_image.url == url:
        return
      os.remove(post.images.all()[0].path)
      db.session.delete(previous_image)
      db.session.commit()
    
    image.save(image_path)
    
    post_image = PostImage(
      url=url,
      path=image_path,
      order=1,
      user=user,
      post=post)
    db.session.add(post_image)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    return True

  @classmethod
  def create_post(cls, user: User, title: str, content: str, status: str, category: Category, image) -> bool:
    """
    Create post
    
    :param user: `User` model instance
    :param title: post title, will be used to create slug
    :param content: post content
    :param status: post status `draft - published`
    :returns: True if successful
    
    :raises DatabaseCommitError: if failed to commit to database
    """
    if not re.fullmatch(r'^[a-zA-Z0-9 ]+$', title):
      raise InvalidPostTitle(
        'Post title can only contain letters, numbers and spaces')
      
    post_found = Post.query.filter_by(title=title).first()
    if post_found:
      raise ValueError('Title already exists in database')
    
    post = Post(
      user=user, 
      title=title.strip(), 
      content=content.strip(), 
      status=status,
      category=category)
    post.blog = user.blog
    post.create_slug()
    
    db.session.add(post)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    if image.filename:
      cls.save_post_image(image, user, post)

    return True
  
  @classmethod
  def update_post(cls, user: User, post: Post, title: str, content: str, category: Category, image) -> bool:
    """
    Update given post
    
    :param post: `Post` model instance
    :param title: post title
    :param content: post content
    :returns: True if update successful
    
    :raises InvalidPostTitle: if title contains illegal characters
    :raises ValueError: if title already exists in database
    :raises DatabaseCommitError: if failed to commit to database
    """
    if not re.fullmatch(r'^[a-zA-Z0-9 ]+$', title):
      raise InvalidPostTitle(
        'Post title can only contain letters, numbers and spaces')
    
    if title != post.title:
      post_found = Post.query.filter_by(title=title).first()
      if post_found:
        raise ValueError('Title already exists in database')
    
    post.title = title.strip()
    post.content = content.strip()
    post.updated_at = datetime.utcnow()
    post.category = category
    post.create_slug()
    
    db.session.add(post)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    if image.filename:
      cls.save_post_image(image, user, post)
    
    return True
    
  @classmethod
  def delete_post(cls, post: Post) -> bool:
    """
    Delete give post
    
    :param post: `Post` model instance
    :returns: True if successful
    :raises DatabaseCommitError: if failed to commit to database
    """
    db.session.delete(post)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  @classmethod
  def change_post_status(cls, post: Post) -> bool:
    """
    Change given post status between `draft` and `published`
    
    :param post: `Post` model instance
    :returns: True if successful
    :raises DatabaseCommitError: if failed to commit to database
    """
    post.status = 'published' if post.status == 'draft' else 'draft'
    db.session.add(post)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  @classmethod
  def create_comment(cls, user: User, post: Post, content: str) -> bool:
    """
    Create comment for given user and post
    
    :param user: `User` model instance
    :param post: `Post` model instance
    :param content: comment's content
    :returns: True if successful
    :raises ValueError: if comment is empty
    :raises DatabaseCommitError: if failed to commit to database
    """
    if content == '':
      raise ValueError('Empty comment')
    comment = Comment(content=content, user=user, post=post)
    db.session.add(comment)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError()
    return True

  @classmethod
  def delete_comment(cls, comment: Comment) -> bool:
    """
    Delete given comment
    
    :param comment: `Comment` model instance
    :returns: True if successful
    :raises DatabaseCommitError: if failed to commit to database
    """
    db.session.delete(comment)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError()
    return True
  
  @classmethod
  def create_category(cls, name: str) -> bool:
    """
    Create category
    
    :param name: category name
    :returns: True if successful
    :raises DatabaseCommitError: if failed to commit to database
    """
    category = Category(name=name)
    category.create_slug()
    db.session.add(category)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  @classmethod
  def delete_cateory(cls, category: Category) -> bool:
    """
    Delete category
    
    :param category: `Category` model instance
    :returns: True if successful
    :raises DatabaseCommitError: if failed to commit to database
    """
    db.session.delete(category)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
  
  @classmethod
  def edit_category(cls, category: Category, name: str) -> bool:
    """
    Edit category
    
    :param category: `Category` model instance
    :param name: category's new name
    :returns: True if successful
    :raises DatabaseCommitError: if failed to commit to database
    """
    category.name = name
    db.session.add(category)
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise DatabaseCommitError(e)
    
    return True
