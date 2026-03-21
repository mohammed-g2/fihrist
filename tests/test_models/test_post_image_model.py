import unittest
from app import create_app, db
from app.models import User, Post, PostImage


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
  
  def test_create_post_image(self):
    pi1 = PostImage()
    pi2 = PostImage()
    db.session.add_all([pi1, pi2])
    db.session.commit()
    
    self.assertEquals(PostImage.query.all(), [pi1, pi2])
  
  def test_post_image_cascading(self):
    p = Post()
    db.session.add(p)
    db.session.commit()
    
    pi = PostImage(post=p)
    db.session.add(pi)
    db.session.commit()
    
    db.session.delete(p)
    db.session.commit()
    
    self.assertEquals(PostImage.query.all(), [pi])
