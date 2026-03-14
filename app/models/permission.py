
class Permission:
  FOLLOW = 1
  COMMENT = 2
  WRITE = 4
  MODERATE = 8
  ADMIN = 16

roles = {
  'banned': [],
  'user': [
    Permission.FOLLOW, Permission.COMMENT
  ],
  'writer': [
    Permission.FOLLOW, Permission.COMMENT, Permission.WRITE
  ],
  'moderator': [
    Permission.FOLLOW, Permission.COMMENT, Permission.WRITE,
    Permission.MODERATE
  ],
  'admin': [
    Permission.FOLLOW, Permission.COMMENT, Permission.WRITE,
    Permission.MODERATE, Permission.ADMIN
  ]
}

default_role = 'user'
