#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Script to evaluate player prices before drafting.

    This script will get projection data from 'basketballmonster.com',
    and then use league settings to evaluate player prices.

    First, you need to have a paid basetballmonster membership, otherwise
    there is no projection data on the projection page.

    :copyright: (c) 2017 by HuangShaozuo.
"""

from bs4 import BeautifulSoup
from scipy import stats
from selenium import webdriver
from selenium.webdriver import PhantomJS
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import click
import csv
import time


# use hupu(https://bbs.hupu.com/fba) official settings.
# actually not used in program for now, need to enhance the program to use this setting
CATEGORIES = ['PTS', '3PM', 'REB', 'AST', 'STL', 'BLOCK', 'FG', 'FT', 'TO', 'ORB', 'AT']

class PriceEvaluator() :

    def __init__(self, username, password, team_num = 18, player_num_per_team = 12, salary_cap_per_team = 200,
            one_dollar_player_num = 30, categories=CATEGORIES):

        self.username = username
        self.password = password
        self.categories = categories
        self.team_num = team_num
        self.player_num_per_team = player_num_per_team
        self.salary_cap_per_team = salary_cap_per_team

        # This number should match your expectation for the # of $1 players in your league.
        # It can also be used to scale up the projected prices for the top players: 
        # the more $1 players, the more funds available for the top players.
        self.one_dollar_player_num = one_dollar_player_num

    def run(self):
        
        # basketball monster has two value type projections: total season and per game
        season_data_page, per_game_data_page = self._load_data_pages(False)

        season_names, season_values = self._scrape_data(season_data_page)
        season_prices = self._evaluate_player_prices(season_values)

        per_game_names, per_game_values = self._scrape_data(per_game_data_page)
        per_game_prices = self._evaluate_player_prices(per_game_values)

        self._output_to_csv(season_names, season_prices, per_game_names, per_game_prices)

    def _load_data_pages(self, headless = True):
        """
        Load the page that has projection data. 
        This page is not a static page, we first need to login, and then fill some settings.
        Returns the page source.
        """

        if headless:
            DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
            driver = webdriver.PhantomJS()
        else:
            chrome_options = Options()
            chrome_options.add_argument("--dns-prefetch-disable")
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.set_window_size(1920, 1080)
            driver.maximize_window()

        print("visiting https://basketballmonster.com")
        driver.get('https://basketballmonster.com/')

        delay = 8
        # login
        print("login with user name", self.username)
        loginElement = driver.find_element_by_link_text('Login').click()
        usernameElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_UsernameTextBox")))
        usernameElement.send_keys(Keys.CONTROL + "a") # ctr + a to select existing, thus we can override (not append) it
        usernameElement.send_keys(self.username)
        passwordElement = driver.find_element_by_id('ContentPlaceHolder1_PasswordTextBox')
        passwordElement.send_keys(Keys.CONTROL + "a") # ctr + a to select existing, thus we can override (not append) it
        passwordElement.send_keys(self.password)
        driver.find_element_by_id('ContentPlaceHolder1_LoginButton').click()
        time.sleep(2)

        # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "RankingsMenu")))
        # driver.get('https://basketballmonster.com/LeagueSettings.aspx')
        
        # teamNumElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_LeagueSizeUserControl1_NumberOfTeamsTextBox")))
        # teamNumElement.send_keys(Keys.CONTROL + "a")
        # teamNumElement.send_keys(self.team_num)
        # teamPlayerElement = driver.find_element_by_id('ContentPlaceHolder1_LeagueSizeUserControl1_NumberOfPlayersTextBox')
        # teamPlayerElement.send_keys(Keys.CONTROL + "a")
        # teamPlayerElement.send_keys(self.player_num_per_team)
        # salaryCapElement = driver.find_element_by_id('ContentPlaceHolder1_LeagueSizeUserControl1_DollarsForPlayersTextBox')
        # salaryCapElement.send_keys(Keys.CONTROL + "a")
        # salaryCapElement.send_keys(self.salary_cap_per_team)
        # oneDollarPlayerElement = driver.find_element_by_id('ContentPlaceHolder1_LeagueSizeUserControl1_OneDollarTextBox')
        # oneDollarPlayerElement.send_keys(Keys.CONTROL + "a")

        # # basketball monster the number of $1 dollar player is per team.
        # # the number of $1 dollar player in this class it total
        # oneDollarPlayerElement.send_keys(self.one_dollar_player_num // self.player_num_per_team)
        # oneDollarPlayerElement.send_keys(Keys.RETURN)

        # # make 'offense rebound' and 'assist to turnovers' active
        # driver.find_element_by_xpath('//input[@name="CATGROUP:10"][@id="ON"]').click()
        # driver.find_element_by_xpath('//input[@name="CATGROUP:29"][@id="ON"]').click()
        # driver.find_element_by_xpath('//*[@id="form1"]/div[6]/div[1]/input[1]').click()

        driver.get('https://basketballmonster.com/Projections.aspx')

        # player filter set to "all players"
        playerFilter = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "PlayerFilterControl")))
        playerFilterSelect = Select(playerFilter)
        playerFilterSelect.select_by_visible_text("All Players")

        # set value type to 'total value'
        print("get total value ranking")
        valueType = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "ValueDisplayType")))
        valueTypeSelect = Select(valueType)
        valueTypeSelect.select_by_visible_text("Total Value")
        # non_comparison_toggle = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_UpdatePanel"]/div[5]/div/label[4]')))
        # ActionChains(driver).move_to_element(non_comparison_toggle).click(non_comparison_toggle).perform()
        refresh_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/div[7]/div[4]/input[1]')))
        ActionChains(driver).move_to_element(refresh_button).click(refresh_button).perform()
        time.sleep(8)
        totalContent = driver.page_source

        print("get per game value ranking")
        valueType = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "ValueDisplayType")))
        valueTypeSelect = Select(valueType)
        valueTypeSelect.select_by_visible_text("Per Game Value")
        # non_comparison_toggle = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_UpdatePanel"]/div[5]/div/label[4]')))
        # ActionChains(driver).move_to_element(non_comparison_toggle).click(non_comparison_toggle).perform()
        refresh_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/div[7]/div[4]/input[1]')))
        ActionChains(driver).move_to_element(refresh_button).click(refresh_button).perform()
        time.sleep(8)
        perGameContent = driver.page_source
        
        # driver.quit()

        return totalContent, perGameContent


    def _scrape_data(self, page_source):
        """
        Get the projection data (name, value) for each player.
        """
        soup = BeautifulSoup(page_source, "html.parser")
        rows = soup.find('table', class_='datatable').findAll('tr')
        print("There are ", len(rows), "rows in the data table")

        # find name and value column index
        name_index = -1
        value_index = -1
        for row in rows:
            if row.find('th'):
                for idx, col in enumerate(row.findAll('th')):
                    if col.text.strip() == 'Name':
                        name_index = idx
                    elif col.text.strip() == 'Value':
                        value_index = idx
                break
        print('name column index', name_index)
        print('value column index', value_index)

        player_data = [row for row in rows if row.find('td')]  # skip header rows
        print("There are ", len(player_data), "players in the data table")

        names  = [row.findAll('td')[name_index].text.strip()  for row in player_data]
        values = [float(row.findAll('td')[value_index].text.strip()) for row in player_data]

        return names, values


    def _evaluate_player_prices(self, rawValues):

        # user standard score, not raw score to evaluate price
        # scores = stats.zscore(rawValues)
        # user raw values
        scores = rawValues

        total_player_num = self.team_num * self.player_num_per_team
        total_salary_cap = self.team_num * self.salary_cap_per_team
        print('The number of total player:', total_player_num)
        print('The number of $1 player:', self.one_dollar_player_num)
        print('Total salary in your league:', total_salary_cap)

        top_player_budget = total_salary_cap - self.one_dollar_player_num * 1
        top_player_num = total_player_num - self.one_dollar_player_num
        top_player_ave_price = top_player_budget / top_player_num
        print('Available funds for top player:', top_player_budget)
        print('The number of top player:', top_player_num)
        print('Total average price of top player:', top_player_ave_price)

        # calculation solution:
        #  1. the last top palyer's price is 2.(one dollar player is excluded here)
        #  2. calcualte the total value of all top player - suppose the last top player's value is 0

        top_player_total_value = 0
        for i, score in enumerate(scores):

            # make $1 player to 1, and negative price to zero
            if i < top_player_num:
                top_player_total_value += (score - scores[top_player_num])
            else:
                break

        a = 2
        b = top_player_budget / top_player_total_value;

        prices = []

        for i, score in enumerate(scores):

            # make $1 player to 1, and negative price to zero
            if i < top_player_num:
                price = round(a + b * (score - scores[top_player_num]))
            elif i < total_player_num:
                price = 1
            else:
                price = 0

            prices.append(int(price))

        return prices


    def _output_to_csv(self, season_names, season_prices, per_game_names, per_game_prices) :

        # season_names and per_game_names are not in same order,
        # so I first need to map the per_game_value to season names
        name_to_price_map = {}
        for name, price in zip (per_game_names, per_game_prices):
            name_to_price_map[name] = price

        csv_file_name = '{}_{}_{}_{}_price.csv'.format(self.team_num, self.player_num_per_team, self.salary_cap_per_team, self.one_dollar_player_num)
        print('Write to result to csv file "{}"'.format(csv_file_name))
        with open(csv_file_name, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Price_Total', 'Price_PerGame']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for name, sean_price in zip(season_names, season_prices):
                if name in name_to_price_map:
                    per_game_price = name_to_price_map[name]
                else:
                    per_game_price = 0
                writer.writerow({'Name': name, 'Price_Total': sean_price, 'Price_PerGame' : per_game_price})


@click.command()
@click.option('--username', prompt='Your BasketballMonster username', help='Need paid user to get basketball monster projection')
@click.option('--password', hide_input=True, prompt='Your BasketballMonster password', help='Need paid user to get basketball monster projection')
@click.option('--team_num', type=int, default=18, prompt='team numbers in your league', help='Your team numbers of the league.')
@click.option('--player_num_per_team', type=int, default=12, prompt='player numbers of each team', help='player numbers for each team.')
@click.option('--salary_cap_per_team', type=int, default=200, prompt='salary cap of each team', help='salary cap for each team.')
@click.option('--one_dollar_player_num', type=int, default=30, prompt='number of total $1 player in league', help='the more the $1 player, the more funds available for top players.')
def main(username, password, team_num, player_num_per_team, salary_cap_per_team, one_dollar_player_num):

    evaluator = PriceEvaluator(username, password, team_num, player_num_per_team, salary_cap_per_team, one_dollar_player_num)
    evaluator.run()


if __name__ == '__main__':
    main()
