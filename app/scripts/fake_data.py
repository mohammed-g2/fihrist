from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app.ext import db
from app.models import User, Blog, Post


def create_users(count: int=100) -> None:
  """
  Create users
  
  :param count: total number of users to be created
  """
  fake = Faker()
  i = 0
  while i < count: 
    user = User(
      username=fake.user_name(),
      password='123456*',
      email=fake.name(),
      bio=fake.text(),
      created_at=fake.past_date())
    
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
  db.session.commit()


def create_posts(count: int=100) -> None:
  """
  Create posts
  
  :param count: total number of posts created
  """
  fake = Faker()
  user_count = User.query.count()
  for i in range(user_count):
    user = User.query.offset(randint(0, user_count - 1)).first()
    post = Post(
      title=fake.sentence(nb_words=10),
      content=fake.text(),
      status='published',
      created_at=fake.past_date(),
      blog=user.blog,
      user=user)
    post.create_slug()
    db.session.add(post)
  db.session.commit()

