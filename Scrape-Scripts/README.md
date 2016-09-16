##Scripts to Scrape Basketball Data

###BBRef_95_15_TeamSeason.py
Scrapes game log data for each team, year-by-year, from basketball-reference.com, and places into a txt file that needs a bit of cleaning.

###BBRef_PlaybyPlay.py
Scrapes play-by-play box scores from every game in the 2016 year. For this project I created an interpreter to create box scores, broken up by the first 43 min and last 5 min. Results are placed into a database.

###nbaapiscrape.py
Scrapes the NBA.com API to grab each game's boxscore. Includes pickle files to track how many have been scraped so far so this can be run everyday to get up-to-date player data


