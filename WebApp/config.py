SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

# project root directory
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# data directory
DATA_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'data'))

# web application directory
WEB_APP_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'app'))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(PROJECT_ROOT, 'db_repository')

CREDENTIALS_FILE = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'yahoo_credentials.txt'))



