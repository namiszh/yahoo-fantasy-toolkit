import csv
from app import db


class Team(db.Model):
    '''
    Represents a team.
    '''
    id = db.Column(db.Integer, primary_key=True) 
    idx = db.Column(db.Integer)     # the team index in the league
    name = db.Column(db.String(120))
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'))
    league = db.relationship('League', backref=db.backref('teams', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('teams', lazy='dynamic'))

    def __init__(self, team_idx, team_name, league, user=None):
        self.idx = team_idx
        self.name = team_name
        self.league = league
        self.user = user

    def __repr__(self):
        username = 'Unkown'
        if self.user:
            username = self.user.name
        return '<Team id={}, idx={}, name={}, league name={}, belongs to {}>'.format(self.id, self.idx, self.name, self.league.name, username)

class League(db.Model):
    '''
    Represents a league.
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<League id={}, name={}>'.format(self.id, self.name)


class User(db.Model):
    '''
    Represents a user playing yahoo fantasy basketball.
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User id={}, user name={}>'.format(self.id, self.name)
        

class Record(db.Model):
    '''
    Represents the data of a team for a week(week > 0) or the entire season (week=0).
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

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    team = db.relationship('Team', backref=db.backref('records', lazy='dynamic'))

    def __init__(self, week, fg, ft, pts, _3pm, oreb, reb, ast, stl, blk, to, at, team):
        self.week = week
        self.fg = fg
        self.ft = ft
        self.pts = pts
        self._3pm = _3pm
        self.oreb = oreb
        self.reb  = reb 
        self.ast  = ast 
        self.stl  = stl 
        self.blk  = blk 
        self.to = to
        self.at = at
        self.team = team

    def __repr__(self):
        return '<Week={}, league={}, team={}, fg={}, ft={}, pts={}, 3pm={}, oreb={}, reb={}, ast={}, stl={}, blk={}, to={}, at={}>'.format(self.week,
            self.team.league.name, self.team.name, self.fg, self.ft, self.pts, self._3pm, self.oreb, self.reb, self.ast, self.stl, self.blk, self.to, self.at)

