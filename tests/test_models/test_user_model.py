import unittest
import hashlib
from app import create_app, db
from app.models import User, Role, Permission


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
  
  def insert_users(self) -> list:
    u_1 = User(username='u_1', email='email_1@example.com')
    u_2 = User(username='u_2', email='email_2@example.com')
    u_3 = User(username='u_3', email='email_3@example.com')
    db.session.add_all([u_1, u_2, u_3])
    db.session.commit()
    return [u_1, u_2, u_3]
    
  def test_create_users(self):
    users = self.insert_users()
    self.assertListEqual(User.query.all(), users)

  def test_password_is_not_readable(self):
    user = User(password='pass')
    with self.assertRaises(AttributeError):
      user.password

  def test_password_is_hashed(self):
    user = User(password='pass1')
    self.assertNotEqual(user.password_hash, 'pass1')

  def test_password_salts_are_random(self):
    user_1 = User(password='pass1')
    user_2 = User(password='pass2')
    self.assertNotEqual(user_1.password_hash, user_2.password_hash)

  def test_verify_password_method(self):
    user = User(password='pass1')

    self.assertFalse(user.verify_password('pass2'))
    self.assertTrue(user.verify_password('pass1'))
  
  def test_role_cascading(self):
    role = Role(name='r1')
    db.session.add(role)
    db.session.commit()
    u_1 = User(username='u1')
    u_2 = User(username='u2')
    u_1.role = role
    u_2.role = role
    db.session.add_all([u_1, u_2])
    db.session.commit()
    
    self.assertCountEqual(role.users.all(), [u_1, u_2])
    
    db.session.delete(role)
    db.session.commit()
    
    self.assertIsNotNone(User.query.filter_by(username='u1').first())
    self.assertIsNotNone(User.query.filter_by(username='u2').first())
    
    self.assertIsNone(User.query.filter_by(username='u1').first().role)
  
  def test_can_method(self):
    u = User()
    self.assertFalse(u.can(Permission.WRITE))
    
    r = Role()
    r.add_permission(Permission.WRITE)
    u.role = r
    
    self.assertTrue(u.can(Permission.WRITE))
    self.assertFalse(u.can(Permission.FOLLOW))
  
  def test_is_admin_method(self):
    u = User()
    self.assertFalse(u.is_admin())
    
    r = Role()
    r.add_permission(Permission.WRITE)
    u.role = r
    self.assertFalse(u.is_admin())
    
    r.add_permission(Permission.ADMIN)
    self.assertTrue(u.is_admin())
  
  def test_is_mod_method(self):
    u = User()
    self.assertFalse(u.is_mod())
    
    r = Role()
    r.add_permission(Permission.WRITE)
    u.role = r
    self.assertFalse(u.is_mod())
    
    r.add_permission(Permission.MODERATE)
    self.assertTrue(u.is_mod())
  
  def test_md5_hash_method(self):
    u = User(email='user@email.com')
    hash = hashlib.md5('user@email.com'.encode('utf-8')).hexdigest()
    
    self.assertEquals(u.md5_hash(), hash)
  
  def test_gavatar_method(self):
    u = User(email='user@email.com')
    u.avatar_hash = u.md5_hash()
    url = f'http://www.gravatar.com/avatar/{u.avatar_hash}?s=50&d=default&r=pg'
    
    with self.app.test_request_context('/'):
      self.assertEquals(u.gavatar(50, 'default', 'pg'), url)
