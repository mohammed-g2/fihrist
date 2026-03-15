import unittest
from app import create_app, db
from app.models import User, Blog


class TestUserModel(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.ctx = self.app.app_context()
    self.ctx.push()
    db.create_all()
  
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.ctx.pop()
  
  def test_create_blog(self):
    u = User()
    db.session.add(u)
    db.session.commit()
    
    b = Blog(user=u)
    db.session.add(b)
    db.session.commit()
    
    self.assertListEqual(Blog.query.all(), [b])
    self.assertIsNotNone(u.blog)
    
    # one to one relationship test
    b2 = Blog(user=u)
    db.session.add(b2)
    db.session.commit()
    
    self.assertEquals(u.blog, b2)
    self.assertIsNone(b.user)
  
  def test_blog_cascading(self):
    # blog is deleted however users are not
    u = User()
    db.session.add(u)
    db.session.commit()
    
    b = Blog(user=u)
    db.session.add(b)
    db.session.commit()
    
    db.session.delete(b)
    db.session.commit()
    
    self.assertListEqual(Blog.query.all(), [])
    self.assertListEqual(User.query.all(), [u])
    
    # blog is deleted if user is deleted
    b = Blog(user=u)
    db.session.add(b)
    db.session.commit()
    
    db.session.delete(u)
    db.session.commit()
    
    self.assertListEqual(User.query.all(), [])
    self.assertListEqual(User.query.all(), [])
