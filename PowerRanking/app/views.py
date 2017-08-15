# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings views

    :copyright: (c) 2017 by Marvin Huang
"""

from flask import render_template, redirect, url_for, request
import pandas as pd
from bokeh.charts import Histogram
from bokeh.embed import components
from app import app, status


@app.route('/')
@app.route('/index')
def index():
    # goto current league
    url = url_for('league', league_id=status.current_league)
    return redirect(url)

@app.route('/type=<int:type_id>')
def type(type_id):
    status.type = type_id
    url = url_for('league', league_id=status.current_league)
    return redirect(url)


@app.route('/league=<int:league_id>')
def league(league_id):

    status.current_league = league_id
    if status.type == 0:
        url = url_for('week', league_id=league_id, week=status.current_week)
    else:
        url = url_for('team', league_id=league_id, team_id=status.current_team)

    return redirect(url)



@app.route('/league=<int:league_id>/team=<int:team_id>')
def team(league_id, team_id):
    '''
    Show trend chart of a team.
    
    x axis is the weeks
    y axis is the individual score

    each category (PTS, AST...) has a curve
    '''
    status.current_league = league_id
    status.type = 1
    status.current_team = team_id
    return render_template('index.html', status=status)


@app.route('/league=<int:league_id>/week=<int:week>')
def week(league_id, week):
    '''
    Show power ranking bar graph of the week.

    x axis is teams
    y axis is the total score

    week=0 means the season total
    '''
    status.current_league = league_id
    status.type = 0
    if int(week) > status.max_week:
        week = status.max_week
    status.current_week = week
    return render_template('index.html', status=status)


