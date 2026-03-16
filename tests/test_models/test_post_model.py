import unittest
from app import create_app, db
from app.models import User, Post


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
  
  def test_create_posts(self):
    p1 = Post()
    p2 = Post()
    db.session.add_all([p1, p2])
    db.session.commit()
    self.assertCountEqual(Post.query.all(), [p1, p2])
  
  def test_post_content(self):
    p = Post()
    html = '<script>here</script><p>hello</p>'
    result = 'here<p>hello</p>'
    p.content = html
    db.session.add(p)
    db.session.commit()
    self.assertEquals(p.content, result)
    self.assertEquals(p.content_html, result)
    self.assertEquals(p.content_raw, html)
  
  def test_create_slug_method(self):
    p = Post()
    p.title = '#A Title new posT  '
    p.create_slug()
    self.assertEquals(p.slug, 'a-title-new-post')
  
  def test_plain_content_method(self):
    p = Post()
    p.content = '<p>Hello</p><p>World</p>'
    self.assertEquals(p.plain_content(), 'Hello\nWorld')
  
  def test_clean_method(self):
    p = Post()
    html = '<script>here</script><p>hello</p>'
    result = 'here<p>hello</p>'
    self.assertEquals(p.clean(html), result)

