# -*- coding: utf-8 -*-
"""
    Yahoo Fantasy Sports API

    :copyright: (c) 2018 by Marvin Huang
"""

from app.yahoo_oauth import yahoo_oauth
# from app.models import User, Team, League, Category

class YahooAPI(object):
    def __init__(self, yahoo_oauth):
        self.oauth = yahoo_oauth


    def get_current_user_guid(self):
        '''
        Return user guid
        '''
        uri = 'users;use_login=1'
        resp = self._get(uri)

        #  Cannot get user nick name and image_url from this uri,
        #  workaround: 
        #   from user's team's manager we can get user nickname
        #  and image url. But there could be multiple managers, so
        #  we still need the user guid to identify the correct manager.
        return resp['fantasy_content']['users']['0']['user'][0]['guid']


    def get_current_user_teams(self):
        '''
        Return the current user and all owning teams
        '''
        current_user = {}
        current_user['guid'] = self.get_current_user_guid()

        # user owing teams
        teams = []
        uri = 'users;use_login=1/games;game_keys=nba/teams'
        resp = self._get(uri)
        teams_content = resp['fantasy_content']['users']['0']['user'][1]['games']['0']['game'][1]['teams']
        team_count = int(teams_content['count'])
        for idx in range(0, team_count):
            team_content = teams_content[str(idx)]['team'][0]

            team = {} # team is a dict, only retrieve data we needed
            team['team_key']  =     team_content[0]['team_key']
            team['team_id']   = int(team_content[1]['team_id'])
            team['name']      =     team_content[2]['name']
            team['team_logo'] =     team_content[5]['team_logos'][0]['team_logo']['url']
            teams.append(team)

            # search team managers to find current user's nick name and image url
            managers_content = team_content[19]['managers']
            for manager_content in managers_content:
                guid = manager_content['manager']['guid']
                if guid == current_user['guid']:
                    current_user['name'] = manager_content['manager']['nickname']
                    current_user['image_url'] = manager_content['manager']['image_url']

        return current_user,teams

    def get_current_user_leagues(self):
        '''
        Return all leagues of a user
        '''
        uri = 'users;use_login=1/games;game_keys=nba/leagues'
        resp = self._get(uri)
        leagues_content = resp['fantasy_content']['users']['0']['user'][1]['games']['0']['game'][1]['leagues']
        league_count = int(leagues_content['count'])

        leagues = []
        for idx in range(0,league_count):
            league_content = leagues_content[str(idx)]['league'][0]

            league = {} # league is a dict, only retrieve data we needed
            league['league_key'] = league_content['league_key']
            league['league_id'] = int(league_content['league_id'])
            league['name'] = league_content['name']
            league['num_teams'] = int(league_content['num_teams'])
            league['scoring_type'] = league_content['scoring_type']
            league['start_week'] = int(league_content['start_week'])
            league['end_week'] = int(league_content['end_week'])
            league['current_week'] = int(league_content['current_week'])
            leagues.append(league)

        return leagues


    def get_league_teams(self, league_key):
        '''
        Return all teams and managers in a league
        '''
        uri = 'league/{}/teams'.format(league_key)
        resp = self._get(uri)
        teams_content = resp['fantasy_content']['league'][1]['teams']
        team_count = int(teams_content['count'])

        teams = []
        for idx in range(0, team_count):
            team_content = teams_content[str(idx)]['team'][0]

            team = {}
            team['team_key']  =     team_content[0]['team_key']
            team['team_id']   = int(team_content[1]['team_id'])
            team['name']      =     team_content[2]['name']
            team['team_logo'] =     team_content[5]['team_logos'][0]['team_logo']['url']
            teams.append(team)

        return teams


    def get_league_stat_categories(self, league_key):
        '''
        Return all stat categories used in this league
        '''
        uri = 'game/nba/leagues;league_keys={}/settings'.format(league_key)
        resp = self._get(uri)
        settings = resp['fantasy_content']['game'][1]['leagues']['0']['league'][1]['settings'][0]
        stat_categories = settings['stat_categories']['stats']

        categories = []
        for stat_category in stat_categories:
            stat_content = stat_category['stat']

            stat_id = int(stat_content['stat_id'])
            display_name = stat_content['display_name']
            name = stat_content['name']
            sort_order = int(stat_content['sort_order'])
            if 'is_only_display_stat' in stat_content:
                display_only = int(stat_content['is_only_display_stat'])
            else:
                display_only = 0
            
            category = Category(stat_id, display_name, name, sort_order, display_only)
            print(category)
            categories.append(category)

        return categories


    def get_game_stat_categories(self):
        '''
        Return all available stat categories of the game(NBA),
        used to dynamically create the stat table.
        '''
        uri = 'game/nba/stat_categories'
        resp = self._get(uri)


    def get_team_stat(self, team_key, week):
        '''
        Return the stats of a team for a certain week
        '''
        uri = 'team/{}/stats;type=week;week={}'.format(team_key, week)
        resp = self._get(uri)



    def _get(self, uri):
        base_url = 'https://fantasysports.yahooapis.com/fantasy/v2/'
        uri = base_url + uri
        # print('request', uri)
        resp = self.oauth.request(uri, params={'format': 'json'}).json()
        # print('resp', resp)
        return resp

# initialize yahoo api object
yahoo_api = YahooAPI(yahoo_oauth)
