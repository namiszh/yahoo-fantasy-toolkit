# Yahoo Fantasy Basketball

This project contains a WebApp and toolkit to help playing with yahoo fantasy basketball.

## WebApp
Analysis and Visualation of your yahoo fantasy basketball teams and leagues for the current season. 
This would need to authorize to sign in to yahoo, and then import stats via yahoo api.


## Toolkit
Several standalone python scripts.

* Draft Tools

  * Pre Draft Price Evaluation
  
       Scrapes project data from [basketballmonster](https://basketballmonster.com/Projections.aspx), and then evaluates the price for each player. The result is exported to a csv file.
  * Import Pre Draft Values
  
       Reads player prices from a csv file, and then imports these values to your yahoo team.       
       Used for **auction** draft type league.
  * Import Pre Draft Ranks
  
       Reads player ranks from a csv file, and then imports the player ranks to your yahoo team.     
       Used for **snake** draft type league.

* Lineup Tools
  * Start Active Players
  
       Starts active players for your teams for today and upcoming days. 
