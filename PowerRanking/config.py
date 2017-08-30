WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


import os

# project root directory
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# data directory
DATA_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'data'))

# web application directory
WEB_APP_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'app'))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(PROJECT_ROOT, 'db_repository')

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']


