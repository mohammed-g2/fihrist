import unittest
from app import create_app, db
from app.models import Category, Post


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
  
  def test_create_categories(self):
    c1 = Category(name='c1')
    c2 = Category(name='c2')
    db.session.add_all([c1, c2])
    db.session.commit()
    self.assertEquals(Category.query.all(), [c1, c2])
  
  def test_category_cascading(self):
    c = Category()
    db.session.add(c)
    db.session.commit()
    
    p1 = Post(category=c)
    p2 = Post(category=c)
    
    db.session.add_all([p1, p2])
    db.session.commit()
    
    db.session.delete(p1)
    db.session.commit()
    
    self.assertEquals(Category.query.all(), [c])
    
    db.session.delete(c)
    db.session.commit()
    
    self.assertEquals(Post.query.all(), [p2])
