# Start Active Players

Python Selenium script that logs into your **Yahoo Fantasy Basketball** account, and starts active players for your teams for today and upcoming days. 

## How To Run

`python start-active-players.py`

You will be prompted to input information such as your yahoo user name, password, league ids, the number of days you would like to process. You can include these details as options to avoid having to fill them in each time. For example: to start active players for the next week including today for all your leagues.

`python start-active-players.py --u=YahooUsername --p=Y0urYah00Passw0rd --l=all --d=7 --h=False`

If you only want to start active players for some of your leagues, you can explicitly specify the leagues ids with the --l option.
If multiple leagues, separate them with space.

`python start-active-players.py --u=YahooUsername --p=Y0urYah00Passw0rd --l=12345 45678 --d=7 --h=False`

The option '--h' specifies whether your want to see what the browser is running (useful for debugging) or run in headless mode.

Please Note:
If the players on bench have matches on that day, this program will output information such as below:
```
Starting active players for: Wed, Nov 1
Starting active players for: Thu, Nov 2
Starting active players for: Fri, Nov 3
    - Alternate: Stanley Johnson (Det - SG,SF) [Mil]
    - Alternate: Andre Drummond (Det - PF,C) [Mil]
```

## Dependencies

* [Python](https://www.python.org/)
* [Click](http://click.pocoo.org/)  `pip install click`
* [Selenium WebDriver](http://www.seleniumhq.org/projects/webdriver/) `pip install selenium`
* [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) download chromedriver and put it in PATH
* [PhantomJS](http://phantomjs.org/)  download phantomjs.exe and put it in PATH
* [BeautifulSoup](https://pypi.python.org/pypi/beautifulsoup4/) `pip install beautifulsoup4`


