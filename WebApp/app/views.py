# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings views

    :copyright: (c) 2017 by Marvin Huang
"""

from flask import render_template, flash, redirect, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
# import pandas as pd
# import os
# from bokeh.charts import Histogram
# from bokeh.embed import components
# from datetime import datetime
from app import app, lm
from app.models import User, League, Team
from app.chart import *

from app.yahoo_oauth import YahooOAuth
from app.yahoo_api import YahooAPI
from app.db_manager import DataManager

# Initialize a YahooOAuth object
yahoo_oauth = YahooOAuth(app.config['CREDENTIALS_FILE'])

# initialize yahoo api object
yahoo_api = YahooAPI(yahoo_oauth)

# initialize database manager instance
dm = DataManager(yahoo_api)


@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template('index.html')


@app.route('/<show_type>')
def showtype(show_type):
    session['show_type'] = show_type
    url = url_for('league', lid=session['current_league'])
    return redirect(url)


@app.route('/<int:lid>')
def league(lid):
    session['league_id'] = lid

    if session['show_type'] == 'week':
        url = url_for('week', lid=lid, week=session['current_week'])
    else:
        url = url_for('team', lid=lid, tid=session['current_team'])

    return redirect(url)


@app.route('/<int:lid>/<int:tid>')
def team(lid, tid):
    '''
    Show trend chart of a team.
    
    x axis is the weeks
    y axis is the individual score

    each category (PTS, AST...) has a curve
    '''
    session['current_league'] = lid
    session['current_team'] = tid

    league = League.query.filter(League.league_id==lid).first()
    team = Team.query.filter(Team.team_id==tid).first()

    weeks, stat_scores = dm.get_stat_scores_by_team(team)
    figdata_png = get_team_stats_chart(weeks, stat_scores)
    return render_template('index.html', current_league=league, result=figdata_png)


@app.route('/<int:lid>/week=<int:week>')
def week(lid, week):
    '''
    Show power ranking bar graph of the week.

    x axis is teams
    y axis is the total score

    week=0 means the season total
    '''
    session['current_league'] = lid
    session['current_week'] = week

    league = League.query.filter(League.league_id==lid).first()
    title = league.name
    if week==0:
        title +=  '总战力榜'
    else:
        title += '第{}周战力榜'.format(week)
    team_names, team_total_scores = dm.get_league_total_scores_by_week(league, week)
    figdata_png = get_week_score_bar_chart(team_names, team_total_scores, title)

    team_names, team_stat_scores = dm.get_league_stat_scores_by_week(league, week)
    return render_template('index.html', current_league=league, result=figdata_png, stats=None, scores=None)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(id)



@app.route('/login')
def login():
    '''
      This method is called when user clicks 'Sign in'
    '''
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    elif not yahoo_oauth.is_authorized():
        return redirect(url_for('oauth_authorize', oauth_source='login'))
    else:
        # get_current_user
        user = dm.get_current_user()
        if user:
            login_user(user, True)
        else:
            flash('Authentication failed.')

        session['show_type'] = 'week'
        session['current_league'] = 15031
        session['current_team'] = 16
        session['start_week'] = 1
        session['end_week'] = 23
        session['current_week'] = 21

        return redirect(url_for('index'))


@app.route('/import')
def import_stats():
    '''
      This method is called when user clicks 'Import Stats'
    '''
    if not yahoo_oauth.is_authorized():
        return redirect(url_for('oauth_authorize', oauth_source='import'))
    else:
        dm.import_stats()

    return redirect(url_for('index'))

@app.route('/authorize?<oauth_source>')
def oauth_authorize(oauth_source):
    '''
      This method can be called when user clicks 'login in' or 'import data'
      the parameter 'source' indicates where it is from
    '''
    return yahoo_oauth.authorize(oauth_source)

@app.route('/callback?<oauth_source>')
def oauth_callback(oauth_source):
    '''
      This method is called after the authorize completes.
    '''
    yahoo_oauth.callback()

    if oauth_source == 'login':

        dm.update_basic_info()

        # get_current_user
        user = dm.get_current_user()
        if user:
            login_user(user, True)
        else:
            flash('Authentication failed.')

        session['show_type'] = 'week'
        session['current_league'] = 15031
        session['current_team'] = 16
        session['start_week'] = 1
        session['end_week'] = 23
        session['current_week'] = 21

        # session['team']   = user.teams[0]
        # session['league'] = user.teams[0].league
        # session['week']   = user.teams[0].league.current_week
    elif oauth_source == 'import':
        dm.import_stats()

    return redirect(url_for('index'))
