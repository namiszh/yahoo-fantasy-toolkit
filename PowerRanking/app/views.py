# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings views

    :copyright: (c) 2017 by Marvin Huang
"""

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
import pandas as pd
# from bokeh.charts import Histogram
# from bokeh.embed import components
from datetime import datetime
from app import app, db, lm, oid, status
from .models import User, Team, League, Record
from .forms import LoginForm
from .compute import compute_png_svg as compute
from .compute import get_week_score_png
from .scrape import scrape_user_teams

@app.route('/')
@app.route('/index')
# @login_required
def index():

    user = User.query.filter_by(name='husthsz').first()
    if user is None:
        scrape_user_teams('husthsz', 'Xiaom!613')

    url = url_for('league', league_id=status.current_league)
    return redirect(url,)


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

# @app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     # if g.user is not None and g.user.is_authenticated:
#     #     return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#             flash('Login requested for OpenID="%s", remember_me=%s' %
#                   (form.openid.data, str(form.remember_me.data)))
#             return redirect('/index')
#     return render_template('login.html', 
#                            form=form,
#                            providers=app.config['OPENID_PROVIDERS'])
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    print("g.user:", g.user)
    # if g.user is not None and g.user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', 
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
        
@app.before_request
def before_request():
    g.user = current_user
    print(g.user)
    # if g.user.is_authenticated:
    #     g.user.last_seen = datetime.utcnow()
    #     db.session.add(g.user)
    #     db.session.commit()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
