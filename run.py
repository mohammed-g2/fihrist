import os
from dotenv import load_dotenv
from app import create_app
from app.utils.cli import init_cli
from config import basedir


load_dotenv(os.path.join(basedir, '.env'))

app = create_app('development')

init_cli(app)
