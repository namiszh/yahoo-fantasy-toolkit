#Yahoo Fantasy Basketball Toolkits

This project contains a toolkits for playing with yahoo fantasy basketball. 

I have been a heavy gamer of yahoo fantasy basketball since 2007. There are also many tools about (Yahoo/Espn) fantasy basketball on GitHub. Now I'm going to develop my own tools taking the opportunity of learning python and web programing.



## Draft Analysis

### Pre Draft Price Evaluation

This tool scrapes projection data from [basketballmonster](https://basketballmonster.com/Projections.aspx), and then evaluates the price for each player. The result is exported to a csv file.

The price depends on your league settings, such as team numbers, players per team, salary cap per team and number of $1 players.

### Real Time Draft

TBD

reference: https://github.com/joehand/fantasy_bball_research


## Lineup

Python Selenium script that logs into your Yahoo fantasy basketball account and starts active players for today and upcoming days. Accepts arguments username, password, the number of days you would like the bot to process into the future and whether you want to see what the browser is running (useful for debugging) or run in headless mode.

`python start-active-players.py`

You can include these details as options to avoid having to fill them in each time. For example to start active players for the next week including today.

`python start-active-players.py --days=7 --username=YahooUsername --password=Y0urYah00Passw0rd --headless=False`

reference: https://github.com/devinmancuso/nba-start-active-players-bot


## Power Ranking

This is a web app that shows the power ranking for your leagues.

* Weekly Power Ranking
* Total Power Ranking


**Dependencies**

* Python
* [Click](http://click.pocoo.org/)
* Selenium WebDriver
* [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* PhantomJS
* Flask


**To-Do**

- [ ] Scrape projection data from web
- [ ] Start active player for all leagues
- [ ] Real Time Draft
- [ ] Power ranking
- [ ] Unit Test.
