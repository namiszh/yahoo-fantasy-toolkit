# Rob to start active players

Python Selenium script that logs into your **Yahoo Fantasy Basketball** account, and starts active players for **All YOUR TEAMS** for today and upcoming days. Accepts arguments username, password, the number of days you would like the bot to process into the future and whether you want to see what the browser is running (useful for debugging) or run in headless mode.

## How To Run

`python start-active-players.py`

You can include these details as options to avoid having to fill them in each time. For example to start active players for the next week including today.

`python start-active-players.py --u=YahooUsername --p=Y0urYah00Passw0rd --d=7 --h=True`


## Dependencies

* [Python](https://www.python.org/)
* [Click](http://click.pocoo.org/)
* [Selenium WebDriver](http://www.seleniumhq.org/projects/webdriver/)
* [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* [PhantomJS](http://phantomjs.org/)

