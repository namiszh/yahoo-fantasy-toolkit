#!/usr/bin/python

"""
    Script to evaluate player prices before drafting.

    This script will get projection data from 'basketballmonster.com',
    and then use league settings to evaluate player prices.

    First, you need to have a paid basetballmonster membership, otherwise
    you cannot view the projection.

    :copyright: (c) 2017 by HuangShaozuo.
"""

from bs4 import BeautifulSoup
from scipy import stats
from selenium import webdriver
from selenium.webdriver import PhantomJS
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import click
import csv
import pandas as pd
import time

# the web site 'basketballmonster' need to be paid member to view the projection 
BB_USER_NAME='yourbasketballmonserusername'
BB_PASSWORD='yourbasketballmonserpassword'

# use hupu(https://bbs.hupu.com/fba) official settings.
# actually not used in program for now, need to enhance the program to use this setting
CATEGORIES = ['PTS', '3PM', 'REB', 'AST', 'STL', 'BLOCK', 'FG', 'FT', 'TO', 'ORB', 'AT']

class PriceEvaluator() :

    def __init__(self, team_num = 18, player_num_per_team = 12, salary_cap_per_team = 200,
            one_dollar_player_num = 30, categories=CATEGORIES):

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
        season_data_page, per_game_data_page = self._load_data_pages(True)

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
            driver = webdriver.PhantomJS()
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--dns-prefetch-disable")
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.set_window_size(1920, 1080)
            driver.maximize_window()
            driver.implicitly_wait(10)#seconds 

        print("visiting https://basketballmonster.com")
        driver.get('https://basketballmonster.com/')

        # login
        print("login with user name", BB_USER_NAME)
        loginElement = driver.find_element_by_link_text('Login').click()
        # time.sleep(5)
        usernameElement = driver.find_element_by_id('ContentPlaceHolder1_UsernameTextBox')
        usernameElement.send_keys(Keys.CONTROL + "a") # ctr + a to select existing, thus we can override (not append) it
        usernameElement.send_keys(BB_USER_NAME)
        passwordElement = driver.find_element_by_id('ContentPlaceHolder1_PasswordTextBox')
        passwordElement.send_keys(Keys.CONTROL + "a") # ctr + a to select existing, thus we can override (not append) it
        passwordElement.send_keys(BB_PASSWORD)
        driver.find_element_by_id('ContentPlaceHolder1_LoginButton').click()
        # time.sleep(5)

        # after login, the page will redirect to main, now go to league settings
        print("league setting on https://basketballmonster.com/LeagueSettings.aspx")
        driver.get('https://basketballmonster.com/LeagueSettings.aspx')
        teamNumElement = driver.find_element_by_id('ContentPlaceHolder1_LeagueSizeUserControl1_NumberOfTeamsTextBox')
        teamNumElement.send_keys(Keys.CONTROL + "a")
        teamNumElement.send_keys(self.team_num)
        teamPlayerElement = driver.find_element_by_id('ContentPlaceHolder1_LeagueSizeUserControl1_NumberOfPlayersTextBox')
        teamPlayerElement.send_keys(Keys.CONTROL + "a")
        teamPlayerElement.send_keys(self.player_num_per_team)
        salaryCapElement = driver.find_element_by_id('ContentPlaceHolder1_LeagueSizeUserControl1_DollarsForPlayersTextBox')
        salaryCapElement.send_keys(Keys.CONTROL + "a")
        salaryCapElement.send_keys(self.salary_cap_per_team)
        oneDollarPlayerElement = driver.find_element_by_id('ContentPlaceHolder1_LeagueSizeUserControl1_OneDollarTextBox')
        
        oneDollarPlayerElement.send_keys(Keys.CONTROL + "a")

        # basketball monster the number of $1 dollar player is per team.
        # the number of $1 dollar player in this class it total
        oneDollarPlayerElement.send_keys(self.one_dollar_player_num // self.player_num_per_team)
        oneDollarPlayerElement.send_keys(Keys.RETURN)

        # make 'offense rebound' and 'assist to turnovers' active
        driver.find_element_by_xpath('//input[@name="CATGROUP:10"][@id="ON"]').click()
        driver.find_element_by_xpath('//input[@name="CATGROUP:29"][@id="ON"]').click()
        driver.find_element_by_id('ContentPlaceHolder1_SaveSettingsButton').click()
        # time.sleep(5)

         # use 2016 player ranking to test for now, will change to projection when it is available
        print("redirect to https://basketballmonster.com/PlayerRankings.aspx")
        driver.get('https://basketballmonster.com/PlayerRankings.aspx')

         # player filter set to "all players"
        driver.find_element_by_id('ContentPlaceHolder1_PlayerFilterUserControl1_PlayerFilterRadioButtonList_1').click()
        # make sure value column will be displayed
        valueElement = driver.find_element_by_id('ContentPlaceHolder1_ShowOptionsUserControl1_ValuesCheckBoxList_0')
        checked = valueElement.is_selected();
        if not checked:
            valueElement.click()

        # set value type to 'total value'
        print("get total value ranking")
        driver.find_element_by_id('ContentPlaceHolder1_ValueTypeUserControl1_ValueTypeRadioButtonList_0').click()
        driver.find_element_by_id('ContentPlaceHolder1_GetRankingsButton').click()
        # time.sleep(5)
        totalContent = driver.page_source

        print("get per game value ranking")
        driver.find_element_by_id('ContentPlaceHolder1_ValueTypeUserControl1_ValueTypeRadioButtonList_1').click()
        driver.find_element_by_id('ContentPlaceHolder1_GetRankingsButton').click()
        # time.sleep(5)
        perGameContent = driver.page_source
        
        driver.quit()

        return totalContent, perGameContent


    def _scrape_data(self, page_source):
        """
        Get the projection data (name, value) for each player.
        """
        soup = BeautifulSoup(page_source, "html.parser")
        rows = soup.find('table', class_='gridT gridThighlight data-font').findAll('tr')
        print("there are ", len(rows), "rows in the data table")
        player_data = [row for row in rows if row.find('td')]  # skip header rows
        print("there are ", len(player_data), "players in the data table")

        # get only value and name, the 4th column: value; 5th column : name 
        player_data = [[col.text.strip() for col in row.findAll('td')[3:5]] for row in player_data] # get only value and name

        names = []
        values = []

        for x in player_data:
            name = x[1]
            value = float(x[0])
            names.append(name)
            values.append(value)

        return names, values


    def _evaluate_player_prices(self, rawValues):

        # user standard score, not raw score to evaluate price
        zScores = stats.zscore(rawValues)

        total_player_num = self.team_num * self.player_num_per_team
        total_salary_cap = self.team_num * self.salary_cap_per_team
        print('the number of total player:', total_player_num)
        print('the number of $1 player:', self.one_dollar_player_num)
        print('total salary in your league:', total_salary_cap)

        top_player_budget = total_salary_cap - self.one_dollar_player_num * 1
        top_player_num = total_player_num - self.one_dollar_player_num
        top_player_ave_price = top_player_budget / top_player_num
        print('available funds for top player:', top_player_budget)
        print('the number of top player:', top_player_num)
        print('total average price of top player:', top_player_ave_price)

        # there can be two ways to map the average price to a player:
        #    o. median player. 
        #       example: 
        #         it's the 3rd player if there are 5 players in total.
        #    o. the player of which his value is closest to the average value.
        #       example:
        #         given value list [7, 3, 2, 2, 1], then the second player
        #         is selected to map the average price.
        #         
        # I use the first way for now because we also use z score, not raw score.
        median_player_idx = top_player_num // 2

        # the index of the first one dollar player.
        first_one_dollar_player_idx = top_player_num

        # convert the z value to price
        # the formula is Price = a + b* zScore
        # and two  equation:
        #  top_player_ave_price = a + b* zScores[median_player_idx]
        #  1                    = a + b* zScores[first_one_dollar_player_idx]
        #  thus we can calculate a and b.
        b = (top_player_ave_price - 1) / (zScores[median_player_idx] - zScores[first_one_dollar_player_idx])
        a = top_player_ave_price - b * zScores[median_player_idx]

        prices = []

        for i, score in enumerate(zScores):

            # make $1 player to 1, and negative price to zero
            if i < top_player_num:
                price = round(a + b * score)
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

        print('write to result to csv file "price.csv"')
        with open('price.csv', 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Price_Total', 'Price_PerGame']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for name, sean_price in zip(season_names, season_prices):
                per_game_price = name_to_price_map[name]
                writer.writerow({'Name': name, 'Price_Total': sean_price, 'Price_PerGame' : per_game_price})


@click.command()
@click.option('--team_num', type=int, default=18, prompt='team numbers in your league', help='Your team numbers of the league.')
@click.option('--player_num_per_team', type=int, default=12, prompt='player numbers of each team', help='player numbers for each team.')
@click.option('--salary_cap_per_team', type=int, default=200, prompt='salary cap of each team', help='salary cap for each team.')
@click.option('--one_dollar_player_num', type=int, default=30, prompt='# of total $1 player in league', help='the more the $1 player, the more funds available for top players.')
def main(team_num, player_num_per_team, salary_cap_per_team, one_dollar_player_num):

    evaluator = PriceEvaluator(team_num, player_num_per_team, salary_cap_per_team, one_dollar_player_num)
    evaluator.run()


if __name__ == '__main__':
    main()
