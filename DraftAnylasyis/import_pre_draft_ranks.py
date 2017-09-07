#!/usr/bin/python

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
def import_player_ranks(u, p, l, f, h):
    """Given a csv file that has player values, Set pre draft player values for a yahoo fantasy basketball league."""

    # read player values from csv file.
    print('reading player ranks from csv file...')
    df = pd.read_csv(f, encoding = "ISO-8859-1")
    names = df[df.columns[0]].tolist()
    player_list = [name.replace(".", "") for name in names]
    # print(player_list)

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
    print('login into yahoo as {}'.format(u))
    driver.get('https://login.yahoo.com/?.src=fantasy&specId=usernameRegWithName&.intl=us&.lang=en-US&authMechanism=primary&yid=&done=https%3A%2F%2Fbasketball.fantasysports.yahoo.com%2Fnba%2F%3Futmpdku%3D1&eid=100&add=1')
    delay = 8 # seconds
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'login-username'))).send_keys(u)
    driver.find_element_by_id('login-signin').click()
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'login-passwd'))).send_keys(p)
    driver.find_element_by_id('login-signin').click()

    # make sure the 'My Teams and Leagues' Table is loaded
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "gamehome-teams")))

    # find all leagues and teams
    print('find all leagues and teams')
    userTeamElements = driver.find_elements_by_xpath("//div[@class='Grid-table']//a[@class='Block Fz-sm Phone-fz-xs Pbot-xs']")
    
    # get the url of pre draft value rank for this league
    team_url = None
    for teamElement in userTeamElements:
        user_team_url = teamElement.get_attribute("href")
        match = re.search(r'/nba/(\d+)/(\d+)/?$', user_team_url)
        match_league_id = int(match.group(1))
        if match_league_id == l:
            team_url = user_team_url
            break;

    if team_url is None:
        print('cannot find league id={}'.format( l))
        return

    # there are usually about 600 players, we set count to 800 to make all players can display in one page
    pre_draft_value_url = team_url + '/editprerank?count=800'
    print('set pre draft values in {}'.format(pre_draft_value_url))
    driver.get(pre_draft_value_url)

    # first click 'Start Over'
    
    print('click "Start Over"')
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "reset-roster-btn")]'))).click()
    alert = driver.switch_to.alert
    alert.accept()
    # save result
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'submit-editprerank'))).click()
    time.sleep(2)

    # then click 'load all' to load all pages
    # click save would reset the status(count =800), so loading all players explicitly again.
    driver.get(pre_draft_value_url)
    print('Load all players')
    loadAllEle = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, 'Load More Players')))
    hov = ActionChains(driver).move_to_element(loadAllEle)
    hov.perform()
    time.sleep(2)
    ActionChains(driver).move_to_element(loadAllEle).click(loadAllEle).perform()
    time.sleep(5)

    playerElements  = driver.find_elements_by_xpath('//ul[@id="all_player_list"]//li//span//div[contains(@class, "playersimple-adddrop")]//span[@class="Bfc"]//span[2]')
    plusElements    = driver.find_elements_by_xpath('//ul[@id="all_player_list"]//li//span//div[contains(@class, "playersimple-adddrop")]//div[@class="Fl-end"]//span[2]')
    print('There are {} players in the table.'.format(len(playerElements)))

    name_to_ele_map = {}
    for plyaerEle, plusEle in zip(playerElements, plusElements):
        player_name = plyaerEle.text.replace(".", "")  # C.J. McCollum  -> CJ McCollum
        # print(player_name)
        name_to_ele_map[player_name] = plusEle

    print('Set player ranks...')
    for i, player_name in enumerate(player_list):
        if player_name not in name_to_ele_map:
            if i == 0:
                print('***** Cannot find player {} in the table, please check the name and add it to the top manually *****'.format(player_name))
            else:
                print('***** Cannot find player {} in the table, please check the name and add it to the #{} position, just after {} *****'.format(player_name, i+1, player_list[i-1]))

        else:
            webEle = name_to_ele_map[player_name]
            hov = ActionChains(driver).move_to_element(webEle)
            hov.perform()
            # time.sleep(2)
            ActionChains(driver).move_to_element(webEle).click(webEle).perform()

    # save result
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'submit-editprerank'))).click()
    time.sleep(2)

    # show result
    print('show result')
    driver.get(team_url + '/prerank')

    time.sleep(60)
    driver.quit()


if __name__ == '__main__':
    import_player_ranks()
