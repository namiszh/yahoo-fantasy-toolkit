from .yahoo_api import yahoo_api
from .models import User, Team, League, Category
from app import db

class DatabaseManager(object):
    def __init__(self, yahoo_api):
        self.yahoo = yahoo_api
        self.current_user = None

    def update_basic_info(self):
        '''
        Update basic information, such as:
          o. leagues of the signed in user
          o. teams of each league
          o. stat categories of each user
          o. managers of each team
        '''
        db.session.remove()
        db.drop_all()
        db.create_all()

        # get all leagues of current user
        user_leagues = self.yahoo.get_current_user_leagues()

        for league in user_leagues:
            league_key = league.league_key

            # get teams and managers of this league
            league_teams, managers = self.yahoo.get_league_teams(league_key)

            # update Team table
            for league_team in league_teams:
                team = Team.query.filter_by(team_key=league_team.team_key).first()
                if team:    # already exists, update
                    team = league_team
                else:
                    db.session.add(league_team)

            # update User table
            for manager in managers:
                user = User.query.filter_by(guid=manager.guid).first()
                if user:    # already exists, update
                    user = manager
                else:
                    db.session.add(manager)

            # get stat categories of this league
            league_categories = self.yahoo.get_league_stat_categories(league_key)

            # update category table
            for league_category in league_categories:
                category = Category.query.filter_by(stat_id=league_category.stat_id).first()
                if category:
                    category = league_category
                else:
                    db.session.add(league_category)

                # set league categories
                # league.categories.append(category)

            # check whether this league already exists in db
            l = League.query.filter_by(league_key=league_key).first()
            if l:    # already exists, update
                l = league
            else:
                db.session.add(league)

        db.session.commit()

        # get guid of current user
        user_guid = self.yahoo.get_current_user_guid()
        self.current_user = User.query.filter_by(guid=user_guid).first()
        # login_user(user, True)

    def import_stat(self, league_key, week):
        pass


    def get_current_user(self):

        if self.current_user is None:
            user_guid = self.yahoo.get_current_user_guid()
            self.current_user = User.query.filter_by(guid=user_guid).first()

        return self.current_user


    def get_user_teams(self, user):
        '''
        Get user teams and leagues
        '''
        pass

# initialize database manager instance
db_manager = DatabaseManager(yahoo_api)
