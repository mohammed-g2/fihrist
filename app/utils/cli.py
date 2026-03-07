import os
import click
from flask import Flask


def init_cli(app: Flask):
  @app.cli.command()
  def init():
    """Initialize the application."""
    from config import basedir
    os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
    print('> Created data directory.')
    os.makedirs(os.path.join(basedir, 'tmp'), exist_ok=True)
    print('> Created temporary directory.')
    
  @app.cli.group()
  def translate():
    """Translation commands."""
  
  @translate.command()
  def init():
    """Initialize language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
      raise RuntimeError('Extracting "messages.pot" failed.')
    if os.system('pybabel init -i messages.pot -d app/translations -l ar'):
      raise RuntimeError('Initializing language failed.')
    os.remove('messages.pot')
    print('> Language initialized.')
  
  @translate.command()
  def update():
    """Update language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
      raise RuntimeError('Extracting "messages.pot" failed.')
    if os.system('pybabel update -i messages.pot -d app/translations'):
      raise RuntimeError('Updating translation faild.')
    os.remove('messages.pot')
    print('> Translation updated.')
  
  @translate.command()
  def compile():
    """Compile language"""
    if os.system('pybabel compile -d app/translations'):
      raise RuntimeError('Compiling language failed.')
    print('> Translation compiled.')
