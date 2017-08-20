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
from .compute import compute_png_svg as compute
from .compute import get_week_score_png

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
    status.type = 1
    status.current_team = team_id

    teams = [
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

    figdata_png = compute()
    return render_template('index.html', status=status, teams=teams, result=figdata_png)


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

    figdata_png = get_week_score_png(league_id, week)

    return render_template('index.html', status=status, result=figdata_png)

# @app.route("/chart")
# def chart():
#     title = "Week 1"
#     labels = [
#         "B3-Jordan",
#         "B1-pippo",
#         "A5-Gray Potato",
#         "A3-Marsmnky",
#         "C5-unbe",
#         "B4-????????",
#         "xiuxian",
#         "C3-??????",
#         "D5 - ????",
#         "C4-lebronjames",
#         "C1-Lydia",
#         "D4-????",
#         "10,000.00",
#         "A2-??????????",
#         "A4-??????",
#         "C2-Stephen",
#         "D3 - ?U?U",
#         "D1-????",
#         "B2-Sin",
#         "B5-dragonball"
#     ]

#     values = [104.5, 158, 70, 139, 126.5, 145.5, 80, 117, 113, 127.5, 52.5, 113.5, 161, 128, 103, 90.5, 126, 138.5, 126.5, 89.5]
#     return render_template('barchart.html', chart_title=title, values=values, labels=labels)

# # Load the Iris Data Set
# iris_df = pd.read_csv("data/iris.data", names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
# feature_names = iris_df.columns[0:-1].values.tolist()
# print(feature_names)

# # Create the main plot
# def create_figure(current_feature_name, bins):

#     p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species', 
#         bins=bins, legend='top_right', width=600, height=400)

#     # Set the x axis label
#     p.xaxis.axis_label = current_feature_name

#     # Set the y axis label
#     p.yaxis.axis_label = 'Count'
#     return p

# @app.route("/bokeh")
# def bokeh():

#     # Determine the selected feature
#     current_feature_name = request.args.get("feature_name")
#     if current_feature_name == None:
#         current_feature_name = "Sepal Length"

#     # Create the plot
#     plot = create_figure(current_feature_name, 10)
        
#     # Embed plot into HTML via Flask Render
#     script, div = components(plot)
#     return render_template("bokeh.html", script=script, div=div,
#         feature_names=feature_names,  current_feature_name=current_feature_name)
