# Draft Analysis Tools

## Pre Draft Price Evaluation

**What is it**

This tool scrapes projection data from [basketballmonster](https://basketballmonster.com/Projections.aspx), and then use the data to evaluate the price for each player. The result is exported to a csv file.

*NOTE:*
*you need to have a paid basetballmonster membership, otherwise you cannot get the projection data.*


**How to Run**

`python EvaluatePrice.py`

The price depends on your league settings, such as team numbers, player numbers per team, salary cap per team and number of $1 players in your league, thus that you will be prompted to input those information.
