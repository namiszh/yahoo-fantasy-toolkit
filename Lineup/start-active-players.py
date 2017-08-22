#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import click

@click.command()
@click.option('--u', prompt='Your Yahoo username', help='Your Yahoo account username')
@click.option('--p', hide_input=True, prompt='Your Yahoo password', help='Your Yahoo account password')
@click.option('--d', type=int, default=7, prompt='Number of days to set active lineup', help='Number of days to set active lineup')
@click.option('--h', type=bool, default=True, prompt='Do you want to run in headless mode? [True|False]', help='If True you won\'t see what\'s going on while it\'s running. If false you will see the browser render the steps.')
def start_active_players(u, p, d, h):
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
	leagues = driver.find_elements_by_xpath("//div[@class='Grid-table']//dd[@class='Grid-u D-i']//a[@class='F-reset']")
	teams = driver.find_elements_by_xpath("//div[@class='Grid-table']//a[@class='Block Fz-sm Phone-fz-xs Pbot-xs']")
	league_names = [league.text for league in leagues]
	team_urls = [team.get_attribute("href") for team in teams]
	team_names = [team.text for team in teams]

	for leangue_name, team_name, team_url in zip(league_names, team_names, team_urls):
		print("Starting active players for: league='{}', team='{}'".format(leangue_name, team_name))
		driver.get(team_url)

		# starting players for days.
		for x in range(0, d):
			date_text = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//span[@id='selectlist_nav']//a[@href='#']//span[@class='flyout-title']"))).text
			print("Starting active players for: " + date_text)

		# 	driver.find_element_by_xpath("//a[text() = 'Start Active Players']").click()
		# 	time.sleep(2)

			# click 'next day'
			WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//span[@id='selectlist_nav']//a[contains(@class, 'Js-next')]"))).click()

	driver.quit()

	print("Starting active players Finished.")

if __name__ == '__main__':
	start_active_players()
