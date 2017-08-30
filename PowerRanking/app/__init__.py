# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings Application

    :copyright: (c) 2017 by Marvin Huang
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import PROJECT_ROOT, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(PROJECT_ROOT, 'tmp'))

# if not app.debug:
#     import logging
#     from logging.handlers import RotatingFileHandler
#     file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
#     file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('microblog startup')

class Status():

    def __init__(self, current_league = 0, current_team = 0, current_week = 0, max_week=18, type=0):
        self.username = None
        self.current_league = current_league
        self.current_team = current_team
        self.current_week = current_week
        self.max_week = max_week


        # type = 0: show data by week
        # type = 1: show data by team
        self.type = type

status = Status()

from app import views, models


