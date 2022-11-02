# -*- coding: utf-8 -*-
"""
    Yahoo fantasy basketball data analysis display

    copyright: (c) 2022 by Shaozuo Huang
"""

ENV='development'
DEBUG=True


# SECRET_KEY = 'you-will-never-guess'

# SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

# project root directory
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# print('project Root', PROJECT_ROOT)
# # data directory
# DATA_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'data'))

# # web application directory
# WEB_APP_ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'app'))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(PROJECT_ROOT, 'db_repository')

CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, 'credentials')
# print(CREDENTIALS_FILE)
CHINESE_FONT_FILE = os.path.join(PROJECT_ROOT, 'static/fonts/SimSun-01.ttf')
# print(CHINESE_FONT_FILE)




