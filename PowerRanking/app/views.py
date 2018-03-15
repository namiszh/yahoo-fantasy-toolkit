# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings views

    :copyright: (c) 2017 by Marvin Huang
"""

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
import pandas as pd
import os
# from bokeh.charts import Histogram
# from bokeh.embed import components
from datetime import datetime
from app import app, db, lm, oid, status
from app.models import User, Team, League
from app.compute import compute_png_svg as compute
from app.compute import get_week_score_png
from app.yahoo_oauth import yahoo_oauth
from app.db_manager import db_manager


@app.route('/')
@app.route('/index')
# @login_required
def index():

    status.current_league = 573
    status.type = 1
    status.current_team = 2



    # figdata_png = compute()
    return render_template('index.html', 
        status=status)

    # user = User.query.filter_by(name='husthsz').first()
    # if user is None:
    #     scrape_user_teams('husthsz', 'Xiaom!613')

    # url = url_for('league', league_id=status.current_league)
    # return redirect(url,)


@app.route('/type=<int:type_id>')
def type(type_id):
    status.type = type_id
    url = url_for('league', league_id=status.current_league)
    return redirect(url)


@app.route('/lid=<int:league_id>')
def league(league_id):

    status.current_league = league_id
    if status.type == 0:
        url = url_for('week', league_id=league_id, week=status.current_week)
    else:
        url = url_for('team', league_id=league_id, team_id=status.current_team)

    return redirect(url)



@app.route('/lid=<int:league_id>/tid=<int:team_id>')
def team(league_id, team_id):
    '''
    Show trend chart of a team.
    
    x axis is the weeks
    y axis is the individual score

    each category (PTS, AST...) has a curve
    '''
    status.current_league = league_id
    print("league id", league_id)
    status.type = 1
    status.current_team = team_id

    user_team_records = Team.query.join(User, (User.id == Team.user_id)).filter(User.name=='husthsz').order_by(Team.league_id).all()
    user_teams = [[team.name, team.league.name, team.league.id] for team in user_team_records ]
    print(user_teams)

    league_team_records = Team.query.filter(Team.league_id==league_id).order_by(Team.name).all()
    league_teams = [ [team.name, team.id] for team in league_team_records]

    figdata_png = compute()
    return render_template('index.html', 
        status=status, 
        user_teams = user_teams,
        league_teams=league_teams, 
        result=figdata_png)


@app.route('/lid=<int:league_id>/week=<int:week>')
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

    user_team_records = Team.query.join(User, (User.id == Team.user_id)).filter(User.name=='husthsz').order_by(Team.league_id).all()
    user_teams = [[team.name, team.league.name, team.league.id] for team in user_team_records ]
    print(user_teams)

    figdata_png = get_week_score_png(league_id, week)

    return render_template('index.html', 
        status=status, 
        user_teams = user_teams,
        result=figdata_png)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
        


@lm.user_loader
def load_user(id):
    return User.query.get(id)


##########################################################################
@app.route('/authorize')
def oauth_authorize():
    '''
      This method is called when user clicks 'login in'
    '''

    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    return yahoo_oauth.authorize()


@app.route('/callback')
def oauth_callback():
    '''
      This method is called after the authorize completes.
    '''
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    yahoo_oauth.callback()
    # if social_id is None:
    #     return redirect(url_for('index'))

    db_manager.update_basic_info()

    # get_current_user
    user = db_manager.get_current_user()
    if user:
        login_user(user, True)
    else:
        flash('Authentication failed.')
        

    # for team in user.teams:
    #     print('team', team.name)

    # user = User.query.filter_by(name=username).first()
    # if user is None:
    #     # print('adding user {} to db.'.format(username))
    #     user = User(username)
    #     db.session.add(user)
    # user = User.query.filter_by(id=social_id).first()
    # if not user:
    #     user = User(id=social_id, name=username)
    #     db.session.add(user)
    #     db.session.commit()
    # login_user(user, True)
    return redirect(url_for('index'))

##########################################################################
