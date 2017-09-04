#!/usr/bin/python

# from bs4 import BeautifulSoup
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import click
import pandas as pd
import re
import time

@click.command()
@click.option('--u', prompt='Your Yahoo username', help='Your Yahoo account username')
@click.option('--p', hide_input=True, prompt='Your Yahoo password', help='Your Yahoo account password')
@click.option('--l', type=int, prompt='Your yahoo league id', help='Your yahoo league id')
@click.option('--f', prompt='your player value csv file', help='your player value csv file')
@click.option('--h', type=bool, default=True, prompt='Do you want to run in headless mode? [True|False]', help='If True you won\'t see what\'s going on while it\'s running. If false you will see the browser render the steps.')
def import_player_values(u, p, l, f, h):
    """Given a csv file that has player values, Set pre draft player values for a yahoo fantasy basketball league."""

    # read player values from csv file.
    df = pd.read_csv(f, encoding = "ISO-8859-1")
    names = df[df.columns[0]].tolist()
    prices = df[df.columns[1]].tolist()
    player_values = {}
    for name, price in zip(names, prices):
        # in case name is different: for example, some website is 'C.J. McCollum', others it 'CJ McCollum'
        # so we unify the name 
        player_values[name.replace(".", "")] = int(price)

    # get selenium web driver
    if h:
        DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
        driver = webdriver.PhantomJS()
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--dns-prefetch-disable")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.maximize_window()
        

    # login into yahoo
    driver.get('https://login.yahoo.com/?.src=fantasy&specId=usernameRegWithName&.intl=us&.lang=en-US&authMechanism=primary&yid=&done=https%3A%2F%2Fbasketball.fantasysports.yahoo.com%2Fnba%2F%3Futmpdku%3D1&eid=100&add=1')
    delay = 8 # seconds
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'login-username'))).send_keys(u)
    driver.find_element_by_id('login-signin').click()
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'login-passwd'))).send_keys(p)
    driver.find_element_by_id('login-signin').click()

    # make sure the 'My Teams and Leagues' Table is loaded
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "gamehome-teams")))

    # find all leagues and teams
    userTeamElements = driver.find_elements_by_xpath("//div[@class='Grid-table']//a[@class='Block Fz-sm Phone-fz-xs Pbot-xs']")
    
    # get the url of pre draft value rank for this league
    pre_draft_value_url = None
    for teamElement in userTeamElements:
        user_team_url = teamElement.get_attribute("href")
        match = re.search(r'/nba/(\d+)/(\d+)/?$', user_team_url)
        match_league_id = int(match.group(1))
        if match_league_id == l:
            pre_draft_value_url = user_team_url + '/prerank_auction_costs'
            print('find pre draft value setting url {} for league id={}'.format(pre_draft_value_url, l))
            break

    if pre_draft_value_url is None:
        print('cannot find league id={}'.format( l))
        return

    driver.get(pre_draft_value_url)
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "ysf-preauctioncosts-dt")))

    # sort player by name
    # the players are sorted by value by default, thus if we change value,
    # the player sequence would be changed.
    # While the players are displayed in many pages, changing the player sequence could miss some player while goto next page.
    driver.find_element_by_xpath('//table[@id="ysf-preauctioncosts-dt"]//thead//tr//th[contains(@class, "player")]//div//a').click()
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "ysf-preauctioncosts-dt")))

    playerElements  = driver.find_elements_by_xpath('//table[@id="ysf-preauctioncosts-dt"]//tbody//tr//td[contains(@class, "player")]//div//div//a')
    valueElements   = driver.find_elements_by_xpath('//table[@id="ysf-preauctioncosts-dt"]//tbody//tr//td[contains(@class, "tac")]//div//input[@type="text"]')
    excludeElements = driver.find_elements_by_xpath('//table[@id="ysf-preauctioncosts-dt"]//tbody//tr//td[contains(@class, "tpx")]//input[@type="checkbox"]')
    for playerElement, valueElement, excludeElement in zip(playerElements, valueElements, excludeElements):
        player_name = playerElement.text.replace(".", "")  # C.J. McCollum  -> CJ McCollum
        player_value = int(valueElement.get_attribute("value"))
        if player_name not in player_values:
            print('***** Cannot find player {} in csv data file *****'.format(player_name))
        else:
            new_value = player_values[player_name]
            if player_value != new_value:

                selected = excludeElement.is_selected();

                # if new value is zero, original value is not zero.
                # Since set value to zero is not allowed in yahoo,
                # we can exclude this player.
                if new_value == 0:
                    if not selected:
                        ActionChains(driver).move_to_element(excludeElement).click().perform()
                        # excludeElement.click();
                        print("----- Exclude player {} -----".format(player_name))
                else:
                    # make sure not selected thus we can input new value
                    if selected:
                        ActionChains(driver).move_to_element(excludeElement).click().perform()
                        WebDriverWait(driver, delay).until(EC.visibility_of(valueElement))
                    valueElement.send_keys(Keys.CONTROL + "a") # ctr + a to select existing, thus we can override (not append) it
                    valueElement.send_keys(new_value)
                    print("##### Value changed from {:3d} to {:3d} for player {} #####".format(player_value, new_value, player_name))
            else:
                print("===== Value kept unchanged as {:3d} for player {} =====".format(player_value, player_name))
    # save
    saveElement = driver.find_element_by_id('ysf-preauctioncosts-save')
    ActionChains(driver).move_to_element(saveElement).click().perform()

    time.sleep(600)
    driver.quit()


if __name__ == '__main__':
    import_player_values()
