import csv
from app import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(120))
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'), primary_key=True, index=True)
    # records = db.relationship('Record', backref='team', lazy='dynamic')

    def __repr__(self):
        return '<Team id={}, name={}, league name={}>'.format(self.id, self.name, self.league.name)

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(120))
    my_team = db.Column(db.Integer)
    teams = db.relationship('Team', backref='league', lazy='dynamic')
    records = db.relationship('Record', backref='league', lazy='dynamic')

    def __repr__(self):
        return '<League id={}, name={}, my team={}>'.format(self.id, self.name, self.my_team)


class Record(db.Model):
    '''
    Represents the data of a team for a week or the entire season.
    '''
    week = db.Column(db.Integer, primary_key=True)
    fg = db.Column(db.Float)
    ft = db.Column(db.Float)
    pts = db.Column(db.Integer)
    _3pm = db.Column(db.Integer)
    oreb = db.Column(db.Integer)
    reb = db.Column(db.Integer)
    ast = db.Column(db.Integer)
    stl = db.Column(db.Integer)
    blk = db.Column(db.Integer)
    to = db.Column(db.Integer)
    at = db.Column(db.Float)

    league_id = db.Column(db.Integer, db.ForeignKey('league.id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)

    def __repr__(self):
        return '<Week={}, league={}, team={}, fg={}, ft={}, pts={}, 3pm={}, oreb={}, reb={}, ast={}, stl={}, blk={}, to={}, at={}>'.format(self.week,
            self.league.name, self.team_id, self.fg, self.ft, self.pts, self._3pm, self.oreb, self.reb, self.ast, self.stl, self.blk, self.to, self.at)


#     def _ReadFromCSV(league_name, team_name, week):
#         if week == 0:
#             csv_file_name = '{}_all'.format(league_name)
#         else:
#             csv_file_name = '{}_week{}'.format(league_name, week)

#             with open(csv_file_name, 'r') as csvfile:
#                 reader = csv.DictReader(csvfile)
#                 for row in reader:
#                     if row['Team Name'] = team_name:
#                         pass

# class Team(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post %r>' % (self.body)


# class League() :
#     pass
