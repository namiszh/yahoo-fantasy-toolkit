# -*- coding: utf-8 -*-
"""
    Yahoo fantasy basketball data analysis display

    copyright: (c) 2022 by Shaozuo Huang
"""

from calendar import weekday
from flask import render_template, url_for, redirect
from flask_login import login_required
import pandas as pd
import datetime
import pytz
from pandas import DataFrame
from app import app, yHandler
from chart.compute import stat_to_score, roto_score_to_battle_score
from chart.radar_chart import league_radar_charts
from chart.bar_chart import league_bar_chart

def remove_trailing_zero(df):
    df1 = df.astype(str).replace(to_replace=r'\.0*$', value='', regex=True).replace('nan', '')
    return df1


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@login_required
@app.route('/main')
def main():
    leagues = yHandler.get_leagues()
    return render_template('main.html', leagues = leagues) # should be error for no league

@login_required
@app.route('/<league_key>')
def league(league_key):

    display_week = None

    leagues = yHandler.get_leagues()
    for league in leagues:
        if (league_key == league['league_key']):
            start_week = int(league['start_week'])
            end_week = int(league['end_week'])

            current_week = int(league['current_week'])

            weekday = datetime.datetime.now(pytz.timezone('US/Pacific')).weekday()
            # if it is first half week (Mon/Tue/Wed/Thu), display previous week as default
            if weekday <= 3:
                current_week -= 1
            display_week = min(end_week, max(start_week, current_week))
            break

    return redirect(url_for('week', league_key=league_key, week=display_week))



@login_required
@app.route('/<league_key>/<int:week>')
def week(league_key, week):
    print('=== route to league with league_key=', league_key, 'week=', week)

    print('=== retrieving data from yahoo')
    # get league information
    leagues = yHandler.get_leagues()
    min_week = None
    max_week = None
    league_name = None
    for league in leagues:
        if league['league_key'] == league_key:
            min_week = int(league['start_week'])
            max_week = int(league['current_week'])
            weekday = datetime.datetime.now(pytz.timezone('US/Pacific')).weekday()
            # in case there is no match on Monday, and it is earlier morning Tuesday now, no match has been played yet.
            # then there is no stat available yet for this week.
            if weekday <= 1:
                max_week -= 1
            league_name = league['name']
            break

    teams = yHandler.get_league_teams(league_key)
    stat_categories = yHandler.get_game_stat_categories()
    team_names = []
    week_stats = []
    total_stats = []
    stat_names = []
    sort_orders = []
    for team in teams:
        # also include team info in the team stats
        team_names.append(team['name'])

        team_key = team['team_key']
        week_stat, data_types, sort_orders = yHandler.get_team_stat(team_key, stat_categories, week)
        total_stat, data_types, sort_orders = yHandler.get_team_stat(team_key, stat_categories, 0)
        # print(week_stat)
        # print(total_stat)
        stat_names = week_stat.keys()
        # stat_values = week_stat.values()

        week_stats.append(week_stat)
        total_stats.append(total_stat)

    print('=== Analyzing data')
    tie_score = len(stat_names) / 2

    # use a pandas dataframe to calculate ranking value
    week_df = pd.DataFrame(columns=stat_names, index=team_names)
    week_df.columns.name = 'Team Name'
    total_df = pd.DataFrame(columns=stat_names, index=team_names)
    total_df.columns.name = 'Team Name'

    idx = 0
    for team_name in team_names:
        team_stat = week_stats[idx]
        total_stat = total_stats[idx]
        idx += 1
        week_df.loc[team_name] = pd.Series(team_stat)
        total_df.loc[team_name] = pd.Series(total_stat)

    # print(data_types)
    week_df = week_df.astype(data_types)
    total_df = total_df.astype(data_types)

    week_score = stat_to_score(week_df, sort_orders)
    total_score = stat_to_score(total_df, sort_orders)

    battle_score = roto_score_to_battle_score(week_score)

    bar_chart = league_bar_chart(team_names, week_score['Total'], total_score['Total'], league_name, week)
    radar_charts = league_radar_charts(week_score, total_score, week)

    # format output
    week_score = remove_trailing_zero(week_score)
    total_score = remove_trailing_zero(total_score)
    battle_score = remove_trailing_zero(battle_score)


    team_number = len(team_names)
    # highligh max and min
    week_score = week_score.style.apply(
    lambda x: [ 'background: linear-gradient(90deg, #5fba7d 100.0%, transparent 100.0%)'if float(value) == 1 else
          ('background: linear-gradient(90deg, #d65f5f 100.0%, transparent 100.0%)' if float(value) == team_number else 
        '') for value in x])
    # highlight max and min
    total_score = total_score.style.apply(
    lambda x: [ 'background: linear-gradient(90deg, #5fba7d 100.0%, transparent 100.0%)'if float(value) == 1 else
          ('background: linear-gradient(90deg, #d65f5f 100.0%, transparent 100.0%)' if float(value) == team_number else 
        '') for value in x])
    
    # make ithe table pretty with different background color for win/lose/tie
    battle_score = battle_score.style.apply(
    lambda x: [ '' if value=='' else
        ('background: linear-gradient(90deg, #5fba7d 100.0%, transparent 100.0%)'if float(value) < tie_score else
          ('background: linear-gradient(90deg, #d65f5f 100.0%, transparent 100.0%)' if float(value) > tie_score else 
           'background-color: #ffffd9')) for value in x])

    print('=== Generating charts for visualization')
    print('=== rendering page')
    return render_template('league.html', leagues = leagues, current_league_key=league_key, current_week=week, min_week = min_week, max_week = max_week, week_stats=week_df, week_rank = week_score, total_stats=total_df, total_rank = total_score, battle_score= battle_score, bar_chart = bar_chart, radar_charts = radar_charts )

@login_required
@app.route('/<league_key>/<team_id>')
def team(lid, tid):
    pass
