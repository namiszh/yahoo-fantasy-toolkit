#!/usr/bin/python

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import _find_element
from selenium.webdriver.support.ui import WebDriverWait
import click
import re


class element_text_changed(object):
    """
    class to determine whether the text of a web element has changed.
    """
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        actual_text = _find_element(driver, self.locator).text
        return actual_text != self.text

# class element_id_changed(object):
#     """
#     class to determine whether the id of a web element has changed.
#     """
#     def __init__(self, locator, old_id):
#         self.locator = locator
#         self.old_id = old_id

#     def __call__(self, driver):
#         new_id = _find_element(driver, self.locator).get_attribute("id")
#         print(self.old_id, new_id)
#         return new_id != self.old_id

class url_changes(object):
    """An expectation for checking the current url.
    url is the expected url, which must not be an exact match
    returns True if the url is different, false otherwise."""
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        return self.url != driver.current_url

def output_alternates(page):
    """
    Output information if there are players on bench who are available to play.
    """
    soup = BeautifulSoup(page, "html.parser")
    try:
        bench = soup.find_all('tr', class_='bench')
        bench_bios = [p.find('div', class_='ysf-player-name') for p in bench]
        opponents = [p.find_all('td', recursive=False)[4].text for p in bench]

        for player, opponent in zip(bench_bios, opponents):
            n = player.find('a', class_='name')
            d = player.find('span')
            if n and d and opponent:
                name = n.text
                pos = d.text
                print('    - Alternate: %s (%s) [%s]' % (name, pos, opponent))
    except:
        pass

@click.command()
@click.option('--u', prompt='Your Yahoo username', help='Your Yahoo account username')
@click.option('--p', hide_input=True, prompt='Your Yahoo password', help='Your Yahoo account password')
@click.option('--l', default='all', prompt='Your teams (all or league ids separated by space)', help='Your Yahoo Teams')
@click.option('--d', type=int, default=7, prompt='Number of days to set active lineup', help='Number of days to set active lineup')
@click.option('--h', type=bool, default=True, prompt='Do you want to run in headless mode? [True|False]', help='If True you won\'t see what\'s going on while it\'s running. If false you will see the browser render the steps.')
def start_active_players(u, p, l, d, h):
    """Simple python program that sets your active players for the next number DAYS."""
    print("Logging in as: " + u)

    if(h):
        DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
        driver = webdriver.PhantomJS()
    else:
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome()
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
    leagues = driver.find_elements_by_xpath("//div[@id='gamehome-teams']//h3//a")
    league_names = [league.text for league in leagues]
    print("You have", len(leagues), "leagues:", league_names)
    league_urls = [league.get_attribute("href") for league in leagues]
    league_ids = [re.search(r'/nba/(\d+)$', url).group(1) for url in league_urls]

    process_team_list = dict()
    if l=='all':
        for league_name, league_url in zip(league_names, league_urls):
            process_team_list[league_name] = league_url
    else:
        leagues = l.split()
        for league_name, lid, league_url in zip(league_names, league_ids, league_urls):
            if lid in leagues:
                process_team_list[league_name] = league_url

        if not process_team_list :
            print("Cannot not find leagues with id", leagues)
            return

    for league_name, league_url in process_team_list.items():
        print("Starting active players for league '{}'".format(league_name))
        driver.get(league_url)
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "sitenav")))

        driver.find_element_by_link_text("My Team").click()
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "full_stat_nav")))

        # starting players for days.
        for x in range(0, d):
            date_text = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//span[@id='selectlist_nav']//a[@href='#']//span[@class='flyout-title']"))).text
            print("Starting active players for: " + date_text)

            current_url = driver.current_url
            driver.find_element_by_link_text("Start Active Players").click()
            WebDriverWait(driver, delay).until(url_changes(current_url))
            
            # if there are bench player that has match, output info
            output_alternates(driver.page_source)

            # click 'next day'
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//span[@id='selectlist_nav']//a[contains(@class, 'Js-next')]"))).click()

            # wait until page refreshes, that is the date has changed.
            WebDriverWait(driver, delay).until(
                element_text_changed(
                    (By.XPATH, "//span[@id='selectlist_nav']//a[@href='#']//span[@class='flyout-title']"), date_text ) )


    driver.quit()

    print("Starting active players Finished.")



if __name__ == '__main__':
    start_active_players()
