# -*- coding: utf-8 -*-
"""
    Yahoo fantasy basketball data analysis display

    copyright: (c) 2022 by Shaozuo Huang
"""

from flask import render_template, url_for, redirect
from flask_login import login_required
import pandas as pd
from pandas import DataFrame
from app import app, yHandler
from chart.compute import stat_to_score
from chart.radar_chart import league_radar_charts
from chart.bar_chart import league_bar_chart

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@login_required
@app.route('/main')
def main():
    leagues = yHandler.get_leagues()
    return render_template('main.html', leagues = leagues) # should be error for no league

@app.route('/<league_key>')
def league(league_key):

    display_week = None

    leagues = yHandler.get_leagues()
    for league in leagues:
        if (league_key == league['league_key']):
            current_week = int(league['current_week'])
            start_week = int(league['start_week'])
            end_week = int(league['end_week'])
            display_week = min(end_week, max(start_week, current_week -1))
            break

    return redirect(url_for('week', league_key=league_key, week=display_week))



@app.route('/<league_key>/week=<int:week>')
def week(league_key, week):
    print('route to league with league_key=', league_key, 'week=', week)
    leagues = yHandler.get_leagues()
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

    # use a pandas dataframe to cacluclate ranking value
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
    week_score = week_score.round(decimals=1).astype(object)

    total_score = stat_to_score(total_df, sort_orders)
    total_score = total_score.round(decimals=1).astype(object)  # remove trailing .0

    bar_chart = league_bar_chart(team_names, week_score['Total'], total_score['Total'], '战力榜', week)
    radar_charts = league_radar_charts(week_score, total_score, week)

    min_week = None
    max_week = None
    for league in leagues:
        if league['league_key'] == league_key:
            min_week = int(league['start_week'])
            max_week = int(league['current_week'])
            break

    return render_template('league.html', leagues = leagues, current_league_key=league_key, current_week=week, min_week = min_week, max_week = max_week, raw_stats=week_df, ranking_scores = week_score, bar_chart = bar_chart, radar_charts = radar_charts )

@app.route('/<league_key>/<team_id>')
def team(lid, tid):
    pass