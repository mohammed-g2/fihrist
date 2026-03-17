import unittest
from app import create_app, db
from app.models import User, Post, Comment


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
  
  def test_create_comment(self):
    c = Comment()
    db.session.add(c)
    db.session.commit()
    self.assertCountEqual(Comment.query.all(), [c])
  
  def test_post_content(self):
    c = Comment()
    html = '<script>here</script><p>hello</p>'
    result = 'here<p>hello</p>'
    c.content = html
    db.session.add(c)
    db.session.commit()
    self.assertEquals(c.content, result)
    self.assertEquals(c.content_html, result)
    self.assertEquals(c.content_raw, html)
  
  def test_plain_content_method(self):
    c = Comment()
    c.content = '<p>Hello</p><p>World</p>'
    self.assertEquals(c.plain_content(), 'Hello\nWorld')
  
  def test_clean_method(self):
    c = Comment()
    html = '<script>here</script><p>hello</p>'
    result = 'here<p>hello</p>'
    self.assertEquals(c.clean(html), result)
  
  def test_comment_cascading(self):
    # user and post stay if comment deleted
    u = User()
    db.session.add(u)
    db.session.commit()
    
    p = Post()
    p.user = u
    db.session.add(p)
    db.session.commit()
    
    c = Comment()
    c.user = u
    c.post = p
    db.session.add(c)
    db.session.commit()
    
    self.assertEquals(u.comments.all(), [c])
    self.assertEquals(p.comments.all(), [c])
    
    db.session.delete(c)
    db.session.commit()
    self.assertEquals(u.comments.all(), [])
    self.assertEquals(p.comments.all(), [])
    
    # comment stays if post deleted
    c = Comment()
    c.user = u
    c.post = p
    db.session.add(c)
    db.session.commit()
    
    db.session.delete(p)
    db.session.commit()
    
    self.assertEquals(Comment.query.all(), [c])
