import os
import click
from flask import Flask


def init_cli(app: Flask) -> None:
  """
  Initialize cli, commands added:
  - <init> initialize the application
  - <translate init|update|compile> translation commands
  - <test> run unit tests
  
  :param app: application instance
  """
  
  @app.cli.command()
  def init():
    """Initialize the application."""
    from config import basedir
    from app.models import Role
    from app.models.permission import roles, default_role
    from app.errors import DatabaseCommitError
    
    os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
    click.echo('> Created data directory.')
    os.makedirs(os.path.join(basedir, 'tmp'), exist_ok=True)
    click.echo('> Created temporary directory.')
    try:
      Role.set_roles(roles=roles, default=default_role)
      click.echo('> Created new roles and updated existing ones.')
    except Exception as e:
      app.logger.exception(e)
      click.echo('> Failed to create roles.')
  
  @app.cli.command()
  def fake_data():
    """Populate the database with fake data."""
    from app.ext import db
    from app.models import Role
    from app.models.permission import roles, default_role
    from app.scripts.fake_data import (
      create_users, create_blogs, create_posts)
    count = 100
    if app.config['ENV'] != 'development':
      click.echo('> Not in development environment.')
    db.drop_all()
    db.create_all()
    click.echo('> Dropped and recreated database.')
    Role.set_roles(roles=roles, default=default_role)
    click.echo('> Created user roles.')
    create_users(count)
    click.echo(f'> Created users, count: { count }')
    create_blogs()
    click.echo(f'> Created blogs, count: { count }')
    create_posts(count)
    click.echo(f'> Created posts, count: { count }')
  
  @app.cli.command()
  def test():
    """Run unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
  
  @app.cli.group()
  def translate():
    """Translation commands."""
  
  @translate.command()
  @click.argument('lang')
  def init(lang):
    """Initialize language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
      raise RuntimeError('Extracting "messages.pot" failed.')
    if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
      raise RuntimeError('Initializing language failed.')
    os.remove('messages.pot')
    click.echo('> Language initialized.')
  
  @translate.command()
  def update():
    """Update language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
      raise RuntimeError('Extracting "messages.pot" failed.')
    if os.system('pybabel update -i messages.pot -d app/translations'):
      raise RuntimeError('Updating translation faild.')
    os.remove('messages.pot')
    click.echo('> Translation updated.')
  
  @translate.command()
  def compile():
    """Compile language"""
    if os.system('pybabel compile -d app/translations'):
      raise RuntimeError('Compiling language failed.')
    click.echo('> Translation compiled.')


def create_shell_context(app: Flask) -> None:
  """Create shell context with database models available."""
  @app.shell_context_processor
  def shell_context():
    from app.ext import db
    from app.models import User, Role, Permission, Blog, Post
    return dict(
      db=db, User=User, Role=Role, Permission=Permission, Blog=Blog,
      Post=Post)
