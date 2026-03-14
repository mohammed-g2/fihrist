import unittest
from app import create_app, db
from app.models import Role, User, Permission


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

  def insert_data(self) -> list:
    r_1 = Role(name='r_1')
    r_2 = Role(name='r_2')
    r_3 = Role(name='r_3')
    roles = [r_1, r_2, r_3]
    db.session.add_all(roles)
    db.session.commit()
    return roles
  
  def test_create_roles(self):
    roles = self.insert_data()
    self.assertListEqual(Role.query.all(), roles)
  
  def test_default_role_is_not_set(self):
    self.insert_data()
    self.assertIsNone(Role.query.filter_by(default=True).first())
    r_4 = Role(name='r_4', default=True)
    db.session.add(r_4)
    db.session.commit()
    self.assertTrue(Role.query.filter_by(name='r_4').first().default)
  
  def test_role_user_relation(self):
    r_1 = Role()
    r_2 = Role()
    db.session.add_all([r_1, r_2])
    db.session.commit()
    u_1 = User()
    u_1.role = r_1
    u_2 = User()
    u_2.role = r_1
    db.session.add_all([u_1, u_2])
    db.session.commit()
    
    self.assertListEqual(r_1.users.all(), [u_1, u_2])
    self.assertListEqual(r_2.users.all(), [])
    
  
  def test_permissions_equals_0(self):
    r = Role()
    db.session.add(r)
    db.session.commit()
    self.assertEquals(r.permissions, 0)
  
  def test_add_permission_method(self):
    r = Role()
    r.add_permission(Permission.WRITE)
    
    self.assertTrue(r.has_permission(Permission.WRITE))
    self.assertFalse(r.has_permission(Permission.FOLLOW))
  
  def test_remove_permission_method(self):
    r = Role()
    r.add_permission(Permission.WRITE)
    r.add_permission(Permission.FOLLOW)
    r.remove_permission(Permission.FOLLOW)
    
    self.assertTrue(r.has_permission(Permission.WRITE))
    self.assertFalse(r.has_permission(Permission.FOLLOW))
  
  def test_reset_permissions_method(self):
    r = Role()
    r.add_permission(Permission.WRITE)
    r.add_permission(Permission.FOLLOW)
    r.reset_permissions()
    
    self.assertEquals(r.permissions, 0)
  
  def test_has_permission_method(self):
    r = Role()
    r.add_permission(Permission.WRITE)
    r.add_permission(Permission.FOLLOW)
    
    self.assertTrue(r.has_permission(Permission.WRITE))
    self.assertTrue(r.has_permission(Permission.WRITE))
    self.assertFalse(r.has_permission(Permission.ADMIN))
    self.assertFalse(r.has_permission(Permission.MODERATE))
  
  def test_set_roles_method(self):
    Role.set_roles(
      roles={
        'role-1': [Permission.WRITE, Permission.FOLLOW],
        'role-2': [Permission.MODERATE],
        'role-3': [Permission.ADMIN, Permission.WRITE]
      },
      default='role-2')
    role_1 = Role.query.filter_by(name='role-1').first()
    role_2 = Role.query.filter_by(name='role-2').first()
    role_3 = Role.query.filter_by(name='role-3').first()
    default_role = Role.query.filter_by(default=True).first()
    
    # assert all roles exist
    self.assertIsNotNone(role_1)
    self.assertIsNotNone(role_1)
    self.assertIsNotNone(role_1)
    self.assertIsNotNone(default_role)
    
    # assert the correct number for roles exist
    self.assertCountEqual(Role.query.all(), [role_1, role_2, role_3])
    
    # assert roles have the correct permissions
    self.assertTrue(role_1.has_permission(Permission.WRITE))
    self.assertTrue(role_1.has_permission(Permission.FOLLOW))
    self.assertFalse(role_1.has_permission(Permission.ADMIN))
    
    self.assertTrue(role_2.has_permission(Permission.MODERATE))
    self.assertFalse(role_2.has_permission(Permission.ADMIN))
    
    self.assertTrue(role_3.has_permission(Permission.ADMIN))
    self.assertTrue(role_3.has_permission(Permission.WRITE))
    self.assertFalse(role_3.has_permission(Permission.FOLLOW))
    
    # assert default role is set
    self.assertEquals(role_2, default_role)
    
    
