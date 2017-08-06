# Rob to start active players

Python Selenium script that logs into your Yahoo fantasy basketball account and starts active players for today and upcoming days. Accepts arguments username, password, the number of days you would like the bot to process into the future and whether you want to see what the browser is running (useful for debugging) or run in headless mode.

`python start-active-players.py`

You can include these details as options to avoid having to fill them in each time. For example to start active players for the next week including today.

`python start-active-players.py --days=7 --username=YahooUsername --password=Y0urYah00Passw0rd --headless=False`

