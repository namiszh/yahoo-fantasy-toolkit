# Yahoo Fantasy Basketball Toolkit

This directly contains the toolkit for playing with yahoo fantasy basketball.


## Pre Draft Price Evaluation

**What is it**

This tool scrapes projection data from [basketballmonster](https://basketballmonster.com/Projections.aspx), and then use the data to evaluate the price for each player. The result is exported to a csv file.

*NOTE:*
*you need to have a paid basetballmonster membership, otherwise you cannot get the projection data.*


**How to Run**

`python evaluate_player_price.py`

The price depends on your league settings, such as team numbers, player numbers per team, salary cap per team and number of $1 players in your league, thus that you will be prompted to input those information.

You can include these details as options to avoid having to fill them in each time. 

For example:

`python evaluate_player_price.py --username=yourusename --password=yourpassword --team_num=18 --player_num_per_team=12 --salary_cap_per_team=200 --one_dollar_player_num=30`


## Import Pre Draft Values

**What is it**

This tool reads player prices from a csv file, and then imports these values to your yahoo team.
The csv file should contain two columns: the first column is the player name; the second column is the price.

*NOTE:*
*this tool is used for auction draft type league.*


**How to Run**

`python import_pre_draft_values.py`

You will be prompted to input your yahoo user name, password, league id, and csv file which contains the prices.
You can include these details as options to avoid having to fill them in each time. 

For example:

`python import_pre_draft_values.py --u=yourusename --p=yourpassword --l=573 --f=price.csv`


## Import Pre Draft Ranks

**What is it**

This tool reads player ranks from a csv file, and then imports the player ranks to your yahoo team.
The csv file should contain one column: the player name already in rank.

*NOTE:*
*this tool is used for standard draft type league.*


**How to Run**

`python import_pre_draft_ranks.py`

You will be prompted to input your yahoo user name, password, league id, and csv file.
You can include these details as options to avoid having to fill them in each time. 

For example:

`python import_pre_draft_ranks.py --u=yourusename --p=yourpassword --l=573 --f=ranks.csv`


## Start Active Players

**What is it**

Python Selenium script that logs into your **Yahoo Fantasy Basketball** account, and starts active players for your teams for today and upcoming days. 

**How To Run**

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
* [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) download chromedriver and put it in PATH
* [PhantomJS](http://phantomjs.org/download.html)  download phantomjs.exe and put it in PATH
* Others using pip `pip install -r requirements.txt`

