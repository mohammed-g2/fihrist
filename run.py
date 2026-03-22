import os
from dotenv import load_dotenv
from config import basedir

load_dotenv(os.path.join(basedir, '.env'))

COV = None
if os.environ.get('COVERAGE'):
  import coverage
  COV = coverage.coverage(branch=True, include='app/*')
  COV.start()

from app import create_app
from app.ext import migrate, db
from app.utils.cli import create_shell_context, init_cli

app = create_app(os.environ.get('ENV'))
migrate.init_app(app, db)

init_cli(app, COV)
create_shell_context(app)
