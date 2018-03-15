# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Data base manager:

    :copyright: (c) 2018 by Marvin Huang
"""

from app import db
from app.models import User, Team, League, Category
from app.yahoo_api import yahoo_api

class DatabaseManager(object):
    def __init__(self, yahoo_api):
        self.yahoo = yahoo_api
        self.current_user = None

    def update_basic_info(self):
        '''
        Update basic information, such as:
          o. teams of the signed in user
          o. leagues of the signed in user
          o. teams of each league
          o. stat categories of each user
        '''
        db.session.remove()
        db.drop_all()
        db.create_all()

        current_user, user_teams = self.yahoo.get_current_user_teams()

        # update user
        user = User.query.get(current_user['guid'])
        if user:
            user.name = current_user['name']
            user.image_url = current_user['image_url']
        else:
            user = User(current_user['guid'], current_user['name'], current_user['image_url'])
            db.session.add(user)
        print('current user', user)
        db.session.commit()

        # set current user
        self.current_user = User.query.get(current_user['guid'])

        # get all leagues of current user, and update league table
        user_leagues = self.yahoo.get_current_user_leagues()
        print('user leagues')
        for user_league in user_leagues:
            league_key = user_league['league_key']
            league = League.query.get(league_key)
            if league:
                league.league_id    = user_league['league_id']
                league.name         = user_league['name']
                league.num_teams    = user_league['num_teams']
                league.scoring_type = user_league['scoring_type']
                league.start_week   = user_league['start_week']
                league.end_week     = user_league['end_week']
                league.current_week = user_league['current_week']
            else:
                league = League(user_league['league_key'], user_league['league_id'],
                                user_league['name'], user_league['num_teams'],
                                user_league['scoring_type'], user_league['start_week'],
                                user_league['end_week'], user_league['current_week'])
                db.session.add(league)
            print(league)
        db.session.commit()

        # get teams of each league, and update Team table
        for user_league in user_leagues:
            league_key = user_league['league_key']
            league = League.query.get(league_key)   # must not be 'None' now

            league_teams = self.yahoo.get_league_teams(league_key)
            print('Teams of league', user_league['name'])
            for league_team in league_teams:
                team_key = league_team['team_key']
                team = Team.query.get(team_key)
                if team:
                    team.team_id   = league_team['team_id']
                    team.name      = league_team['name']
                    team.team_logo = league_team['team_logo']
                else:
                    team = Team(league_team['team_key'], league_team['team_id'], league_team['name'], league_team['team_logo'])
                db.session.add(team)
                print(team)

                # update team league relationship
                league.teams.append(team)
        db.session.commit()

        # build relationship between user and teams
        for user_team in user_teams:
            team_key = user_team['team_key']
            team = Team.query.get(team_key)     # must not be 'None' now
            user.teams.append(team)
        db.session.commit()


    def import_stat(self, league_key, week):
        pass


    def get_current_user(self):

        if self.current_user is None:
            user_guid = self.yahoo.get_current_user_guid()
            self.current_user = User.query.get(user_guid)

        return self.current_user


# initialize database manager instance
db_manager = DatabaseManager(yahoo_api)
