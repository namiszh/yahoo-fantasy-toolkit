# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings views

    :copyright: (c) 2017 by Marvin Huang
"""

from flask import render_template, redirect, url_for
from app import app

CURRENT_LEAGUE_ID = 1
CURRENT_WEEK = 1

curLeagueId=1
curWeek=1
curTeam=1

@app.route('/')
@app.route('/index')
def show_index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html', user=user)


# @app.route('/league=<league_id>')
# def show_league(league_id):

#     # if CURRENT_LEAGUE_ID != league_id:
#         # CURRENT_LEAGUE_ID = league_id
#         # CURRENT_WEEK = 0    # show total

#     url = url_for('show_week', league_id=league_id, week=0)
#     print(url)
#     return redirect(url)


@app.route('/league=<league_id>/team=<team_id>')
def show_team(league_id, team_id):
    '''
    Show trend chart of a team.
    
    x axis is the weeks
    y axis is the individual score

    each category (PTS, AST...) has a curve
    '''
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html', menu_type="team")

# @app.route('/', defaults={'league_id' :curLeagueId, 'week': curWeek})
# @app.route('/league=<league_id>', defaults={'week': 1})
@app.route('/league=<league_id>/week=<week>')
def show_week(league_id, week):
    '''
    Show power ranking bar graph of the week.

    x axis is teams
    y axis is the total score

    week=0 means the season total
    '''
    print(week)
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html', menu_type="week")

@app.route("/chart")
def chart():
    labels = [
        "B3-Jordan",
        "B1-pippo",
        "A5-Gray Potato",
        "A3-Marsmnky",
        "C5-unbe",
        "B4-????????",
        "xiuxian",
        "C3-??????",
        "D5 - ????",
        "C4-lebronjames",
        "C1-Lydia",
        "D4-????",
        "10,000.00",
        "A2-??????????",
        "A4-??????",
        "C2-Stephen",
        "D3 - ?U?U",
        "D1-????",
        "B2-Sin",
        "B5-dragonball"
    ]

    values = [104.5, 158, 70, 139, 126.5, 145.5, 80, 117, 113, 127.5, 52.5, 113.5, 161, 128, 103, 90.5, 126, 138.5, 126.5, 89.5]
    return render_template('barchart.html', values=values, labels=labels)
