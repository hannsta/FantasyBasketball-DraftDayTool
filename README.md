# FantasyBasketball-DraftDayTool
Python tool designed to aid head-to-head players in drafting fantasy basketball teams.


Python PyQT interface designed to present z-scores and rankings for 9 standard stat categories. Customizable timeframe and ranking algorithm. Still a work in progress, but pretty useful. Included the script I use to scrape data.


Files:

DraftDayTool.py - main PyQt inteface

rankings.py - where most of the math is done, calls the database then generates specific tables to send back to interface

2016Analysis.db - SQLite v3 DB with gamelog data for the 2011-2015 seasons, also has some temporary tables to keep track of teams


Data Source:

Gamelogs for the 2011-2015 seasons, scraped from NBA.com's API.


Features:

Remove players as they are drafted, add players to your team and see how your team's stats are distributed.

Sliders adjust what categories are emphasized in the ranking aglorithms.

Double click a players name to see advanced stats and trend analysis.


Requirements:

pyqt5,numpy,scipy,matplotlib

