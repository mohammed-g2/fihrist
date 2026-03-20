# Installation
instructions for linux systems

### Setting Environment
- Create an start virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools
```
- Install dependencies:
  - for development environment `pip install uv`
  - for production environment `uv sync --no-dev`
- Rename `.env-example` file to `.env`
- Edit the content of `.env` file, make sure to add secret key and 
correctly set the development/production related values
- Initialize the application `flask init dirs`
- Initialize database
```
flask db migrate
flask db upgrade
```
- (Note: flask-migrate not available if environment set to production)
- Initialize user roles `flask init roles` (found in `app.models.permission`)


### Translations
- initialize new translation `flask translate init <lang>`
- Edit `translations/<lang>/LC_MESSAGES/messages.po`
- Update and compile translations
```
flask translate update
flask translate compile
```

### Testing
- Running test suits `flask test`, default to in memory database for testing
- Create fake data `flask fake-data`
- Running testing email server `python app/scripts/mail_server.py`
