from random import randint, choice
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app.ext import db
from app.models import User, Blog, Post, Category, Comment, Role


def create_users(count: int=100) -> None:
  """
  Create users
  
  :param count: total number of users to be created
  """
  fake = Faker()
  i = 0
  role = Role.query.filter_by(default=True).first()
  while i < count: 
    user = User(
      username=fake.user_name(),
      password='123456*',
      email=fake.name(),
      bio=fake.text(),
      created_at=fake.past_date(),
      role=role)
    
    db.session.add(user)
    
    try:
      db.session.commit()
      i += 1
    except IntegrityError:
      db.session.rollback()


def create_blogs() -> None:
  """
  Create a blog per user
  """
  fake = Faker()
  users = User.query.all()
  for user in users:
    blog = Blog(
      name=' '.join(fake.words(randint(1, 5))),
      description=fake.sentence(nb_words=10),
      created_at=fake.past_date(),
      user=user)
    blog.create_slug()
    db.session.add(blog)
  try:
    db.session.commit()
  except IntegrityError:
    db.session.rollback()


def create_categories(count: int=10) -> None:
  """
  Create categories
  
  :param count: total number of categories to be created
  """
  fake = Faker()
  i = 0
  while i < count:
    c = Category(name=' '.join(fake.words(randint(1, 3))))
    c.create_slug()
    db.session.add(c)
    try:
      db.session.commit()
      i += 1
    except IntegrityError:
      db.session.rollback()


def create_posts(count: int=100) -> None:
  """
  Create posts
  
  :param count: total number of posts created
  """
  fake = Faker()
  user_count = User.query.count()
  categories = Category.query.all()
  for i in range(count):
    user = User.query.offset(randint(0, user_count - 1)).first()
    post = Post(
      title=fake.sentence(nb_words=10),
      content=fake.text(max_nb_chars=400),
      status='published',
      created_at=fake.past_date(),
      blog=user.blog,
      user=user,
      category=choice(categories))
    post.create_slug()
    db.session.add(post)
  try:
    db.session.commit()
  except IntegrityError:
    db.session.rollback()


def create_comments(count: int=100) -> None:
  """
  Create comments
  
  :param count: total number of comments created
  """
  fake = Faker()
  post_count = Post.query.count()
  user_count = User.query.count()
  for i in range(count):
    post = Post.query.offset(randint(0, post_count - 1)).first()
    user = User.query.offset(randint(0, user_count - 1)).first()
    
    comment = Comment(
      content=fake.text(max_nb_chars=400),
      created_at=fake.past_date(),
      user=user,
      post=post)
    
    db.session.add(comment)
  db.session.commit()
