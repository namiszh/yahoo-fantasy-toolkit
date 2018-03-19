# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings Application

    :copyright: (c) 2017 by Marvin Huang
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from app import views, models


