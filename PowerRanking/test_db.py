#!/usr/bin/env python
#
import csv
from app import db
from app.models import League, Team, Record

print('Test data base...')
db.session.remove()
db.drop_all()
db.create_all()


l1 = League(id=817, name='Never Ending', my_team=11)
db.session.add(l1)
print ('add league Never Ending')

l2 = League(id=818, name='Alpha', my_team=9)
db.session.add(l2)
print ('add league Alpha')


with open('./data/data_817_1.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate (reader):
        t1= Team(id=i+1, name=row['Team Name'], league_id=817)
        db.session.add(t1)

        t2= Team(id=i+1, name=row['Team Name'], league_id=818)
        db.session.add(t2)

        r1 = Record(week=1, fg=row['FG%'], ft=row['FT%'], pts=row['PTS'],
            _3pm=row['3PTM'], oreb=row['OREB'], reb=row['REB'], ast=row['AST'],
            stl=row['ST'], blk=row['BLK'], to=row['TO'], at=row['A/T'], 
            league_id=817, team_id = i+1)
        db.session.add(r1)

        r2 = Record(week=1, fg=row['FG%'], ft=row['FT%'], pts=row['PTS'],
            _3pm=row['3PTM'], oreb=row['OREB'], reb=row['REB'], ast=row['AST'],
            stl=row['ST'], blk=row['BLK'], to=row['TO'], at=row['A/T'], 
            league_id=818, team_id = i+1)
        db.session.add(r2)

db.session.commit()
print ('add league teams')

# print (db.get_tables_for_bind())

print ('all leagues')
leauges = League.query.all()
for league in leauges:
    print (league)

print ('all teams')
teams = Team.query.all()
for team in teams:
    print (team)

print ('all records')
records = Record.query.all()
for record in records:
    print (record)

