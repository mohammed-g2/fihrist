import os
import sys
import click
from dotenv import load_dotenv
from app import create_app
from app.utils.cli import init_cli, create_shell_context
from config import basedir


load_dotenv(os.path.join(basedir, '.env'))

COV = None
if os.environ.get('COVERAGE'):
  import coverage
  COV = coverage.coverage(branch=True, include='app/*')
  COV.start()

app = create_app('development')

init_cli(app, COV)
create_shell_context(app)
