# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Basketball Data base manager:

    :copyright: (c) 2018 by Marvin Huang
"""

from app import db, yahoo_api
from app.models import User, Team, League, Category, Stat

class DataManager(object):
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
        # db.session.remove()
        # db.drop_all()
        # db.create_all()

        current_user, user_teams = self.yahoo.get_current_user_teams()

        # update user
        user = User.query.get(current_user['guid'])
        if user:
            user.name = current_user['name']
            user.image_url = current_user['image_url']
        else:
            user = User(current_user['guid'], current_user['name'], current_user['image_url'])
            db.session.add(user)
        # print('current user', user)
        db.session.commit()

        # set current user
        self.current_user = User.query.get(current_user['guid'])

        # get all leagues of current user, and update league table
        user_leagues = self.yahoo.get_current_user_leagues()
        # print('user leagues')
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
            # print(league)
        db.session.commit()

        # get teams of each league, and update Team table
        for user_league in user_leagues:
            league_key = user_league['league_key']
            league = League.query.get(league_key)   # must not be 'None' now

            league_teams = self.yahoo.get_league_teams(league_key)
            # print('Teams of league', user_league['name'])
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
                # print(team)

                # update team league relationship
                league.teams.append(team)
        db.session.commit()

        # build relationship between user and teams
        for user_team in user_teams:
            team_key = user_team['team_key']
            team = Team.query.get(team_key)     # must not be 'None' now
            user.teams.append(team)
        db.session.commit()


    def import_stats(self):
        guid = self.yahoo.get_current_user_guid()
        user = User.query.get(guid)
        if user:
            for team in user.teams:
                league = team.league
                self.import_league_stats(league)
        else:
            print('current user is None')

    def import_league_stats(self, league):

        # We don't need to import all past weeks' stats every time
        # we need to import stats. Because some stats are already
        # correct.
        # 
        # First, we need to find the last imported week, then
        # we can import stats from it to the current week.
        # 
        # For example, current week is 9, last imported week is
        # 6. Then this time we only need to import stats from
        # week 6 to week 9. Please note, we cannot start from
        # week 7, but still need to start from week 6, because
        # when we imported stat last time, week 6 may not had
        # completed thus the stats may change later.
        # 
        for team in league.teams:
            last_imported_week = self._get_last_imported_week(team)

            for week in range(last_imported_week,league.current_week + 1):
                self.import_team_stats_by_week(team, week)

            # always need to update season stats
            self.import_team_stats_by_week(team, 0)


    def import_team_stats_by_week(self, team, week):
        print('import stat for team {} week = {}'.format(team.team_key, week))
        team_stats = self.yahoo.get_team_stat(team, week)
        for team_stat in team_stats:
            stat_id = int(team_stat['stat_id'])
            value = team_stat['value']
            stat = Stat.query.filter_by(team_key=team.team_key, week=week, stat_id=stat_id).first()
            if stat:
                stat.value = value
            else:
                stat = Stat(team.team_key, week, stat_id, value)
                db.session.add(stat)
            # print(stat)
        db.session.commit()


    def get_current_user(self):

        if self.current_user is None:
            user_guid = self.yahoo.get_current_user_guid()
            self.current_user = User.query.get(user_guid)

        return self.current_user

    def get_initial():
        pass

    def _get_last_imported_week(self, team):
        week = db.session.query(Stat.week.distinct()).filter_by(team_key=team.team_key).order_by(Stat.week.desc()).first()
        if week:
            # print('========== stats of team {} has been imported to week {} =========='.format(team.name , week) )
            return week[0]
        else:
            # print('============ no stat has been imported for team {} yet ============'.format(team.name) )
            return team.league.start_week


