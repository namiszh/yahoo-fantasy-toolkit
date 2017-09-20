# Draft Tools

This directly contains several draft tools.


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
