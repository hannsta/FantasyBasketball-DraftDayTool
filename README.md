## FantasyBasketball - DraftDayTool
 
Python tool designed to aid head-to-head players in drafting fantasy basketball teams. Python PyQT interface presents z-scores and rankings for 9 standard stat categories. Customizable timeframe and ranking algorithm. Still a work in progress, but pretty useful. Included the script I use to scrape data.
 
 
###Files:
* DraftDayTool.py - main PyQt inteface
* rankings.py - where most of the math is done, calls the database then generates specific tables to send back to interface
* nbaapiscrape.py - script used to collect gamelog data
* helpdialogs.py - help dialogs called by GUI
 
###Features:
 
* Remove players as they are drafted, add players to your team and see how your team's stats are distributed.
* Sliders adjust what categories are emphasized in the ranking aglorithms.
* Double click a players name to see advanced stats and trend analysis.


###Requirements:
pyqt5,numpy,scipy,matplotlib

