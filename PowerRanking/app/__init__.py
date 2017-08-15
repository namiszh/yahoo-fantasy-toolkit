# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings Application

    :copyright: (c) 2017 by Marvin Huang
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class Status():

    def __init__(self, current_league = 0, current_team = 0, current_week = 0, max_week=25, type=0):
        self.current_league = current_league
        self.current_team = current_team
        self.current_week = current_week
        self.max_week = max_week

        # type = 0: show data by week
        # type = 1: show data by team
        self.type = type

status = Status()

from app import views, models

