# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Power Rankings models

    :copyright: (c) 2018 by Marvin Huang
"""
from flask_login import UserMixin
from app import db

# User and Team are many-to-many relationship,
# A user can have many teams, and a team can have
# many managers(co-manager). So we need to define
# a helper table that is used for the relationship. 
# For this helper table it is strongly recommended
# to not use a model but an actual table
user_team_association_table = db.Table('user_team', db.Model.metadata,
    db.Column('user_guid', db.String(64), db.ForeignKey('user.guid'), primary_key=True),
    db.Column('team_key',  db.String(30), db.ForeignKey('team.team_key'), primary_key=True)
)


class User(db.Model, UserMixin):
    '''
    Represents a user playing yahoo fantasy basketball.
    '''
    guid = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(80))
    image_url = db.Column(db.String(80))

    # many-to-many relation ship with user
    teams = db.relationship("Team", secondary=user_team_association_table, backref="managers")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # override method
    def get_id(self):
        return self.guid

    def update(other):
        pass

    def __init__(self, guid, name, image_url):
        self.guid = guid
        self.name = name
        self.image_url = image_url

    def __repr__(self):
        return '<User guid={}, name={}>'.format(self.guid, self.name)


class Team(db.Model):
    '''
    Represents a team.

     fields:

           'team_key': '375.l.15031.t.5',
           'team_id': '5',
           'name': '八菜鸟',
           'team_logo': 'https://ct.yimg.com/cy/4619/37855982573_bd3af4_192sq.jpg?ct=fantasy',
           'managers': maybe multiple - use user's guid
    '''
    team_key = db.Column(db.String(30), primary_key=True)
    team_id = db.Column(db.Integer) 
    name = db.Column(db.String(120))
    team_logo = db.Column(db.String(120))

    league_key = db.Column(db.String, db.ForeignKey('league.league_key'))

    def get_team_key(self):
        return self.team_key

    def __init__(self, team_key, team_id, name, team_logo):
        self.team_key = team_key
        self.team_id = team_id
        self.name = name
        self.team_logo = team_logo

    def __repr__(self):
        return '<Team key={}, id={}, name={}>'.format(
            self.team_key, self.team_id, self.name)


class League(db.Model):
    '''
    Represents a league.

     fields:

           'league_key': '375.l.573',
           'league_id': '573',
           'name': 'Never Ending',
           'num_teams': 20,
           'scoring_type': 'head',
           'start_week': '1',
           'end_week': '23',
           'current_week': 20,
    '''
    league_key = db.Column(db.String(20), primary_key=True)
    league_id = db.Column(db.Integer)
    name = db.Column(db.String(120))
    num_teams = db.Column(db.Integer)
    scoring_type = db.Column(db.String(30)) 
    start_week = db.Column(db.Integer)
    end_week = db.Column(db.Integer)
    current_week = db.Column(db.Integer)

    # league and team are one-to-many relationship.
    # 
    # This is not an actual database field, but a high-level view of the relationship
    # between leagues and teams, and for that reason it isn't in the database diagram.
    # For a one-to-many relationship, a db.relationship field is normally defined
    # on the "one" side, and is used as a convenient way to get access to the "many". 
    teams = db.relationship('Team', backref="league", order_by="Team.team_id")

    # different league can have different stat categories, no back reference is defined.
    # categories = db.relationship('Category')

    def get_league_key(self):
        return self.league_key

    def __init__(self, league_key, league_id, name, num_teams, scoring_type, 
        start_week, end_week, current_week):
        self.league_key = league_key
        self.league_id = league_id
        self.name = name
        self.num_teams = num_teams
        self.scoring_type = scoring_type
        self.start_week = start_week
        self.end_week = end_week
        self.current_week = current_week

    def __repr__(self):
        return '<League key={}, id={}, name={}, num_teams={}, scoring_type={}, start_week={}, end_week={}, current_week={}>'.format(
                 self.league_key, self.league_id, self.name, self.num_teams, 
                 self.scoring_type, self.start_week, self.end_week, self.current_week)


class Category(db.Model):
    '''
        Represents available stat categories of nba game.
        This table should only be updated once

        fields:

              'stat_id': '5',
              'display_name': 'FG%',
              'name': 'Field Goal Percentage',
              'sort_order': '1'
    '''
    stat_id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(10))
    name = db.Column(db.String(40))
    sort_order = db.Column(db.Integer)  # 0: ascending; 1: decending   ('Turn Over' should be ascending, the less, the better)
    display_only = db.Column(db.Integer)    # FGM/FGA and FTM/FTA are display only, don't need to calculate score

    def __init__(self, stat_id, display_name, name, sort_order, display_only=0):
        self.stat_id = stat_id
        self.display_name = display_name
        self.name = name
        self.sort_order = sort_order
        self.display_only = display_only

    def __repr__(self):
        return '<stat id={}, display name={}, name={}, sort order={}>'.format(
            self.stat_id, self.display_name, self.name, self.sort_order)

