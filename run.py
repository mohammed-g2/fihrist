import os
from dotenv import load_dotenv
from app import create_app
from config import basedir


load_dotenv(os.path.join(basedir, '.env'))

app = create_app('development')
