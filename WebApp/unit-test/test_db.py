#!/usr/bin/env python
#

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
from app import db
from app.models import League, Team, Record, User

print('Test data base...')
db.session.remove()
db.drop_all()
db.create_all()

print('Adding users...')
u1 = User('husthsz')
u2 = User('namiszh')
db.session.add(u1)
db.session.add(u2)

print('Adding leagues...')
l1 = League(573, 'Never Ending')
l2 = League(id=818, name='Alpha')
db.session.add(l1)
db.session.add(l2)

print('Adding teams...')
t1 = Team(1, "A1", l1, u1)
t2 = Team(2, "AA", l1)
t3 = Team(1, "A1", l2, u1)
t4 = Team(2, "AA", l2, u2)
db.session.add(t1)
db.session.add(t2)
db.session.add(t3)
db.session.add(t4)

print('Adding records...')
r1 = Record(1, 0.47, 0.87, 23, 1, 1, 5, 3, 0, 0, 1, 2.0, t1)
r2 = Record(2, 0.47, 0.87, 23, 1, 1, 5, 3, 0, 0, 1, 2.0, t1)
r3 = Record(1, 0.47, 0.87, 23, 1, 1, 5, 3, 0, 0, 1, 2.0, t2)
r4 = Record(2, 0.47, 0.87, 23, 1, 1, 5, 3, 0, 0, 1, 2.0, t2)
r5 = Record(1, 0.47, 0.87, 23, 1, 1, 5, 3, 0, 0, 1, 2.0, t3)
r6 = Record(2, 0.47, 0.87, 23, 1, 1, 5, 3, 0, 0, 1, 2.0, t3)
r7 = Record(1, 0.47, 0.87, 23, 1, 1, 5, 3, 0, 0, 1, 2.0, t4)
r8 = Record(2, 0.47, 0.87, 23, 1, 1, 5, 3, 0, 0, 1, 2.0, t4)
db.session.add(r1)
db.session.add(r2)
db.session.add(r3)
db.session.add(r4)
db.session.add(r5)
db.session.add(r6)
db.session.add(r7)
db.session.add(r8)

db.session.commit()

print ('all users')
users = User.query.all()
for user in users:
    print (user)

print ('all leagues')
leagues = League.query.all()
for league in leagues:
    print (league)

print ('all teams')
teams = Team.query.all()
for team in teams:
    print (team)

print ('all records')
records = Record.query.all()
for record in records:
    print (record)


print("league teams")
league_teams = Team.query.filter(Team.league_id==573).order_by(Team.idx).all()
league_team_names = [team.name for team in league_teams]
print(league_team_names)

print("user teams")
user_team_records = Team.query.join(User, (User.id == Team.user_id)).filter(User.name=='husthsz').order_by(Team.league_id).all()
user_teams = [[team.name, team.league.name, team.league.id] for team in user_team_records ]
print(user_teams)

