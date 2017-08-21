#!/usr/bin/python

import time
from selenium import webdriver
from selenium.webdriver import PhantomJS
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from sys import argv
import click

@click.command()
@click.option('--username', prompt='Your Yahoo username', help='Your Yahoo account username')
@click.option('--password', prompt='Your Yahoo password', help='Your Yahoo account password')
@click.option('--days', type=int, default=7, prompt='Number of days to set active lineup', help='Number of days to set active lineup')
@click.option('--headless', type=bool, default=True, prompt='Do you want to run in headless mode? [True|False]', help='If True you won\'t see what\'s going on while it\'s running. If false you will see the browser render the steps.')
def start_active_players(username, password, days, headless):
	"""Simple python program that sets your active players for the next number DAYS."""
	print("Logging in as: " + username)

	if(headless):
		DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
		driver = webdriver.PhantomJS()
	else:
		chrome_options = webdriver.ChromeOptions()
		driver = webdriver.Chrome()
		driver.set_window_size(1920, 1080)
		driver.maximize_window()

	driver.get('https://login.yahoo.com/?.src=fantasy&specId=usernameRegWithName&.intl=us&.lang=en-US&authMechanism=primary&yid=&done=https%3A%2F%2Fbasketball.fantasysports.yahoo.com%2Fnba%2F%3Futmpdku%3D1&eid=100&add=1')

	driver.find_element_by_id('login-username').send_keys(username)
	driver.find_element_by_id('login-signin').click()
	time.sleep(8)
	driver.find_element_by_id('login-passwd').send_keys(password)
	driver.find_element_by_id('login-signin').click()
	time.sleep(8)

	# hover to Fantasy Basketball to display the hidden dropdown menu 
	# teams = driver.find_element_by_xpath("//li[@class = 'Navitem Navitem-main Navitem-fantasy Va-top Fl-start Topstart']")
	# hov = ActionChains(driver).move_to_element(teams)
	# hov.perform()
	# time.sleep(1)

	# print("current url", driver.current_url)
	leagues = driver.find_elements_by_xpath("//div[@class='Grid-table']//dd[@class='Grid-u D-i']//a[@class='F-reset']")
	league_names = [league.text for league in leagues]
	teams = driver.find_elements_by_xpath("//div[@class='Grid-table']//a[@class='Block Fz-sm Phone-fz-xs Pbot-xs']")
	team_urls = [team.get_attribute("href") for team in teams]
	team_names = [team.text for team in teams]

	for leangue_name, team_name, team_url in zip(league_names, team_names, team_urls):
		print("Starting active players league='{}', team='{}'".format(leangue_name, team_name))
		driver.get(team_url)

		time.sleep(2)

		for x in range(0, days):
			date_text = driver.find_element_by_xpath("//span[@id='selectlist_nav']//a[@href='#']//span[@class='flyout-title']").text
			print("Starting active players for: " + date_text)

		# 	driver.find_element_by_xpath("//a[text() = 'Start Active Players']").click()
		# 	time.sleep(2)

			driver.find_element_by_xpath("//span[@id='selectlist_nav']//a[contains(@class, 'Js-next')]").click()
			time.sleep(2)

	driver.quit()

if __name__ == '__main__':
	start_active_players()
