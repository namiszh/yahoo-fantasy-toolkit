#!/usr/bin/python

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re

from app import app, db, status
from app.models import User, League, Team, Record


def scrape_user_teams(username, password):
    """Scrape league and team info for a user."""

    DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
    driver = webdriver.PhantomJS()

    # login into yahoo
    driver.get('https://login.yahoo.com/?.src=fantasy&specId=usernameRegWithName&.intl=us&.lang=en-US&authMechanism=primary&yid=&done=https%3A%2F%2Fbasketball.fantasysports.yahoo.com%2Fnba%2F%3Futmpdku%3D1&eid=100&add=1')
    delay = 8 # seconds

    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'login-username'))).send_keys(username)
    driver.find_element_by_id('login-signin').click()

    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'login-passwd'))).send_keys(password)
    driver.find_element_by_id('login-signin').click()

    # make sure the 'My Teams and Leagues' Table is loaded
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "gamehome-teams")))

    # add user to db
    user = User.query.filter_by(name=username).first()
    if user is None:
        print('adding user {} to db.'.format(username))
        user = User(username)
        db.session.add(user)
    status.username = username

    # find all leagues and teams
    leagueElements = driver.find_elements_by_xpath("//div[@class='Grid-table']//dd[@class='Grid-u D-i']//a[@class='F-reset']")
    userTeamElements = driver.find_elements_by_xpath("//div[@class='Grid-table']//a[@class='Block Fz-sm Phone-fz-xs Pbot-xs']")
    
    # find all teams of the user, and the leagues, league urls, team urls.
    league_names = []
    league_urls = []
    user_team_names = []
    user_team_urls = []
    for leagueElement, teamElement in zip(leagueElements, userTeamElements):
        league_names.append(leagueElement.text)
        league_urls.append(leagueElement.get_attribute("href"))
        user_team_names.append(teamElement.text)
        user_team_urls.append(teamElement.get_attribute("href"))

    # get all teams for each leagues
    for i, (league_name, league_url, user_team_name, user_team_url) in enumerate( zip(league_names, league_urls, user_team_names, user_team_urls) ):
        match = re.search(r'/nba/(\d+)/(\d+)/?$', user_team_url)
        league_id = int(match.group(1))
        user_team_idx = int(match.group(2))

        # set league and team for current status
        if i==0:
            status.current_league = league_id
            status.current_team = user_team_idx

        # add league to db
        league = League.query.get(league_id)
        if league is None:
            # go to league url
            print('redirecting to ', league_url)
            driver.get(league_url)

            # wait until the standing tab present
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "leaguestandingstabs")))

            # click 'Schedule', we will get teams in the schedule table
            driver.find_element_by_link_text('Schedule').click()
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "schedsubnav")))
            leagueTeamElements = driver.find_elements_by_xpath("//ul[@id='schedsubnav']//li[contains(@class,'Navitem')]")

            league = League(league_id, league_name)
            print('adding league {} to db.'.format(league_name))
            db.session.add(league)

            for idx, teamElement in enumerate(leagueTeamElements):
                team_name = teamElement.text
                print("adding team {} to db.".format(team_name))
                team = Team(idx+1, team_name, league)
                db.session.add(team)

        # update team user
        user_team = Team.query.filter_by(league_id=league_id, idx=user_team_idx).first()
        if user_team:
            print('updating user to {} for team {}'.format(username, user_team))
            user_team.user = user

    db.session.commit()

    driver.quit()



# def scrape_user_teams(u, p):
#   driver = login(u, p)

def scrape_stats(u, p, lid, week):
    pass

if __name__ == '__main__':
    db.session.remove()
    db.drop_all()
    db.create_all()
    scrape_user_teams('YourYahooAccount', 'YourYahoopassword')
