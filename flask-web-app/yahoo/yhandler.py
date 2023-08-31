#!/bin/python

import objectpath
import datetime

YAHOO_ENDPOINT = 'https://fantasysports.yahooapis.com/fantasy/v2'


class YHandler:
    """Class that constructs the APIs to send to Yahoo"""

    def __init__(self, yOauth):
        self.oauth = yOauth

    def get_user_id(self):
        '''
        Return information of current user
        '''
        uri = 'users;use_login=1'
        resp = self._get(uri)
        t = objectpath.Tree(resp)
        jfilter = t.execute('$..users..user..(guid)')
        ids = []
        for i in jfilter:
            ids.append(i)

        return ids[0]
    

    def get_leagues(self):
        '''
        Return all leagues of current user for the recent season
        '''
        today = datetime.date.today()
        season = today.year
        if today.month < 10 or (today.month == 10 and today.day < 25): # nba season usually starts at the end of Oct
            season -= 1

        print('=== get leagues for season', season)
        uri = 'users;use_login=1/games;game_codes=nba;seasons={}/leagues'.format(season)
        resp = self._get(uri)
        t = objectpath.Tree(resp)
        jfilter = t.execute('$..leagues..(league_key, league_id, name, logo_url, current_week, start_week, end_week)')

        leagues = []
        for l in jfilter:
            leagues.append(l)

        # sort by league id
        leagues.sort(key = lambda league : int(league['league_id']))

        # print(leagues)
        # [{
        #     'league_key': '418.l.23727',
        #     'league_id': '23727',
        #     'name': 'Never Ending',
        #     'logo_url': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/56477424891_aa0cec.png',
        #     'current_week': 2,
        #     'start_week': '1',
        #     'end_week': '23'
        # }, {
        #     'league_key': '418.l.35600',
        #     'league_id': '35600',
        #     'name': 'Hupu Kappa 22-23',
        #     'logo_url': False,
        #     'current_week': 2,
        #     'start_week': '1',
        #     'end_week': '24'
        # }]

        return leagues


    def get_league_stat_categories(self, league_key):
        '''
        Return all stat categories used in this league
        '''
        uri = 'league/{}/settings'.format(league_key)
        resp = self._get(uri)
        t = objectpath.Tree(resp)
        jfilter = t.execute('$..stat_categories..(stat_id, display_name, sort_order)')

        categories = []
        for c in jfilter:
            categories.append(c)

        # sort by league id
        categories.sort(key = lambda stat : int(stat['stat_id']))

        # print(categories)
        # [{
        #     'stat_id': 5,
        #     'display_name': 'FG%',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 8,
        #     'display_name': 'FT%',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 10,
        #     'display_name': '3PTM',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 12,
        #     'display_name': 'PTS',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 13,
        #     'display_name': 'OREB',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 15,
        #     'display_name': 'REB',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 16,
        #     'display_name': 'AST',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 17,
        #     'display_name': 'ST',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 18,
        #     'display_name': 'BLK',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 19,
        #     'display_name': 'TO',
        #     'sort_order': '0'
        # }, {
        #     'stat_id': 20,
        #     'display_name': 'A/T',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 9004003,
        #     'display_name': 'FGM/A',
        #     'sort_order': '1'
        # }, {
        #     'stat_id': 9007006,
        #     'display_name': 'FTM/A',
        #     'sort_order': '1'
        # }]

        return categories
    
    def get_league_teams(self, league_key):
        '''
        Return all teams and managers in a league
        '''
        uri = 'league/{}/teams'.format(league_key)
        resp = self._get(uri)
        t = objectpath.Tree(resp)
        jfilter = t.execute('$..teams..team..(team_key, team_id, name, team_logos)')

        teams = []
        t = {}
        for p in jfilter:
            if ('team_logos' in p):
                t['team_logos'] = p['team_logos'][0]['team_logo']['url']
            else:
                t.update(p)

            # team logo is the last property
            if ('team_logos' in t):
                teams.append(t)
                t = {} 

        # # sort by team id
        teams.sort(key = lambda team : int(team['team_id']))

        # print(teams)
        # [{
        # 'team_key': '418.l.23727.t.1',
        # 'team_id': '1',
        # 'name': 'szrocky',
        # 'team_logos': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/25942278979_a8f154.jpg'
        # }, {
        # 'team_key': '418.l.23727.t.2',
        # 'team_id': '2',
        # 'name': '黄花菜',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_10.png'
        # }, {
        # 'team_key': '418.l.23727.t.3',
        # 'team_id': '3',
        # 'name': 'CP9',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_1.png'
        # }, {
        # 'team_key': '418.l.23727.t.4',
        # 'team_id': '4',
        # 'name': 'makexi niubi',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_1.png'
        # }, {
        # 'team_key': '418.l.23727.t.5',
        # 'team_id': '5',
        # 'name': 'Jordan',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_1.png'
        # }, {
        # 'team_key': '418.l.23727.t.6',
        # 'team_id': '6',
        # 'name': 'lebronjames',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_1_t.png'
        # }, {
        # 'team_key': '418.l.23727.t.7',
        # 'team_id': '7',
        # 'name': 'Lydia',
        # 'team_logos': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/a7853ab8f5eeaa7c05e534ca800a6225f4a572607807e1ed8aabb3e343766836.jpg'
        # }, {
        # 'team_key': '418.l.23727.t.8',
        # 'team_id': '8',
        # 'name': 'Mr. Big',
        # 'team_logos': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/663025769178c72a5997fbf22c12649886995da2110ede3953e2828fadd960ed.jpg'
        # }, {
        # 'team_key': '418.l.23727.t.9',
        # 'team_id': '9',
        # 'name': 'Patrick Mahomes',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_5_m.png'
        # }, {
        # 'team_key': '418.l.23727.t.10',
        # 'team_id': '10',
        # 'name': 'Sin',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_1.png'
        # }, {
        # 'team_key': '418.l.23727.t.13',
        # 'team_id': '13',
        # 'name': 'xinxiu',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_8.png'
        # }, {
        # 'team_key': '418.l.23727.t.14',
        # 'team_id': '14',
        # 'name': '天王',
        # 'team_logos': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/38943109226_e41e32.jpg'
        # }, {
        # 'team_key': '418.l.23727.t.15',
        # 'team_id': '15',
        # 'name': '香菜花',
        # 'team_logos': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/29900025029_d778ee.png'
        # }, {
        # 'team_key': '418.l.23727.t.16',
        # 'team_id': '16',
        # 'name': '毛豆豆健健康康幸福永久',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_4_l.png'
        # }, {
        # 'team_key': '418.l.23727.t.17',
        # 'team_id': '17',
        # 'name': '海棠依旧',
        # 'team_logos': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/c912234a345df2e3b4408c587646d99f21493bb8e6f527a05d1c3fdca91e443b.jpg'
        # }, {
        # 'team_key': '418.l.23727.t.18',
        # 'team_id': '18',
        # 'name': '苏打绿',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_9_f.png'
        # }, {
        # 'team_key': '418.l.23727.t.19',
        # 'team_id': '19',
        # 'name': '苦菜花',
        # 'team_logos': 'https://s.yimg.com/cv/apiv2/default/nba/nba_5.png'
        # }, {
        # 'team_key': '418.l.23727.t.20',
        # 'team_id': '20',
        # 'name': '阿木',
        # 'team_logos': 'https://yahoofantasysports-res.cloudinary.com/image/upload/t_s192sq/fantasy-logos/57361001784_23825b.jpg'
        # }]

        return teams

    
    def get_team_stat(self, team_key, game_stat_categories, week=0):
        '''
        Return the stats of a team for a certain week, or the season(week==0)
        '''
        if week==0:
            uri = 'team/{}/stats;type=season'.format(team_key)
        else:
            uri = 'team/{}/stats;type=week;week={}'.format(team_key, week)
        # print(uri)
        resp = self._get(uri)
        # print(resp)
        t = objectpath.Tree(resp)
        jfilter = t.execute('$..team_stats..stats..(stat_id, value)')

        stats = {}
        data_types = {}
        sort_orders = []
        for s in jfilter:
            stat_id = int(s['stat_id'])

            # make sure stat_id in game stat categories to filter out display only stat
            if stat_id in game_stat_categories:
                stat_name = game_stat_categories[stat_id]['display_name']
                v = s['value']
                if isinstance(v, str) and '.' in v:
                    v = float(v)
                    data_types[stat_name] ='float'
                else:
                    data_types[stat_name] = 'int'

                stats[stat_name] = v

                sort_order = game_stat_categories[stat_id]['sort_order']
                sort_orders.append(sort_order)

        # print(stats)
        # {'FG%': 0.455, 'FT%': 0.746, '3PTM': 32, 'PTS': 322, 'OREB': 48, 'REB': 177, 'AST': 82, 'ST': 17, 'BLK': 17, 'TO': 38, 'A/T': 2.16}
        # print(data_types)
        # {'FG%': 'float', 'FT%': 'float', '3PTM': 'int', 'PTS': 'int', 'OREB': 'int', 'REB': 'int', 'AST': 'int', 'ST': 'int', 'BLK': 'int', 'TO': 'int', 'A/T': 'float'}
        # print(sort_orders)
        # ['1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1']

        return stats, data_types, sort_orders


    def get_game_stat_categories(self):
        '''
        Return all available stat categories of the game(NBA),
        used to dynamically create the stat table.
        '''
        uri = 'game/nba/stat_categories'
        resp = self._get(uri)
        t = objectpath.Tree(resp)
        jfilter = t.execute('$..stat_categories..stats..(stat_id, display_name, sort_order)')

        categories = {}
        for c in jfilter:
            categories[c['stat_id']] = c

        # print(categories)
        # {
        # 0: {
        #     'stat_id': 0,
        #     'display_name': 'GP',
        #     'sort_order': '1'
        # },
        # 1: {
        #     'stat_id': 1,
        #     'display_name': 'GS',
        #     'sort_order': '1'
        # },
        # 2: {
        #     'stat_id': 2,
        #     'display_name': 'MIN',
        #     'sort_order': '1'
        # },
        # 3: {
        #     'stat_id': 3,
        #     'display_name': 'FGA',
        #     'sort_order': '1'
        # },
        # 4: {
        #     'stat_id': 4,
        #     'display_name': 'FGM',
        #     'sort_order': '1'
        # },
        # 5: {
        #     'stat_id': 5,
        #     'display_name': 'FG%',
        #     'sort_order': '1'
        # },
        # '3': {
        #     'stat_id': '3'
        # },
        # '4': {
        #     'stat_id': '4'
        # },
        # 6: {
        #     'stat_id': 6,
        #     'display_name': 'FTA',
        #     'sort_order': '1'
        # },
        # 7: {
        #     'stat_id': 7,
        #     'display_name': 'FTM',
        #     'sort_order': '1'
        # },
        # 8: {
        #     'stat_id': 8,
        #     'display_name': 'FT%',
        #     'sort_order': '1'
        # },
        # '6': {
        #     'stat_id': '6'
        # },
        # '7': {
        #     'stat_id': '7'
        # },
        # 9: {
        #     'stat_id': 9,
        #     'display_name': '3PTA',
        #     'sort_order': '1'
        # },
        # 10: {
        #     'stat_id': 10,
        #     'display_name': '3PTM',
        #     'sort_order': '1'
        # },
        # 11: {
        #     'stat_id': 11,
        #     'display_name': '3PT%',
        #     'sort_order': '1'
        # },
        # '9': {
        #     'stat_id': '9'
        # },
        # '10': {
        #     'stat_id': '10'
        # },
        # 12: {
        #     'stat_id': 12,
        #     'display_name': 'PTS',
        #     'sort_order': '1'
        # },
        # 13: {
        #     'stat_id': 13,
        #     'display_name': 'OREB',
        #     'sort_order': '1'
        # },
        # 14: {
        #     'stat_id': 14,
        #     'display_name': 'DREB',
        #     'sort_order': '1'
        # },
        # 15: {
        #     'stat_id': 15,
        #     'display_name': 'REB',
        #     'sort_order': '1'
        # },
        # 16: {
        #     'stat_id': 16,
        #     'display_name': 'AST',
        #     'sort_order': '1'
        # },
        # 17: {
        #     'stat_id': 17,
        #     'display_name': 'ST',
        #     'sort_order': '1'
        # },
        # 18: {
        #     'stat_id': 18,
        #     'display_name': 'BLK',
        #     'sort_order': '1'
        # },
        # 19: {
        #     'stat_id': 19,
        #     'display_name': 'TO',
        #     'sort_order': '0'
        # },
        # 20: {
        #     'stat_id': 20,
        #     'display_name': 'A/T',
        #     'sort_order': '1'
        # },
        # '16': {
        #     'stat_id': '16'
        # },
        # '19': {
        #     'stat_id': '19'
        # },
        # 21: {
        #     'stat_id': 21,
        #     'display_name': 'PF',
        #     'sort_order': '0'
        # },
        # 22: {
        #     'stat_id': 22,
        #     'display_name': 'DISQ',
        #     'sort_order': '0'
        # },
        # 23: {
        #     'stat_id': 23,
        #     'display_name': 'TECH',
        #     'sort_order': '0'
        # },
        # 24: {
        #     'stat_id': 24,
        #     'display_name': 'EJCT',
        #     'sort_order': '0'
        # },
        # 25: {
        #     'stat_id': 25,
        #     'display_name': 'FF',
        #     'sort_order': '0'
        # },
        # 26: {
        #     'stat_id': 26,
        #     'display_name': 'MPG',
        #     'sort_order': '1'
        # },
        # 27: {
        #     'stat_id': 27,
        #     'display_name': 'DD',
        #     'sort_order': '1'
        # },
        # 28: {
        #     'stat_id': 28,
        #     'display_name': 'TD',
        #     'sort_order': '1'
        # }
        # }


        return categories    

    def _get(self, uri):
        """Send an API request to the URI and return the response as JSON

        :param uri: URI of the API to call
        :type uri: str
        :return: JSON document of the response
        :raises: RuntimeError if any response comes back with an error
        """
        response = self.oauth.request("{}/{}".format(YAHOO_ENDPOINT, uri),
                                       params={'format': 'json'})
        if response.status_code != 200:
            raise RuntimeError(response.content)
        jresp = response.json()
        return jresp
