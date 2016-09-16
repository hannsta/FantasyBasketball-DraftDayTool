## FantasyBasketball - DraftDayTool
 
Python tool designed to aid head-to-head players in drafting fantasy basketball teams. Python PyQT interface presents z-scores and rankings for 9 standard stat categories. Customizable timeframe and ranking algorithm. Still a work in progress, but pretty useful. Included the script I use to scrape data.
 
 
###Files:
* DraftDayTool.py - main PyQt inteface
* rankings.py - Database queries and math, generates table for interface display
* helpdialogs.py - help dialogs called by GUI
* /Images - contains images used by the tool's interface
* /Scrape-Scripts - contains a variety of scraping scripts to gather data from NBA.com and BasketBall-Reference.com
 
###Features:
 
* Remove players as they are drafted, add players to your team and see how your team's stats are distributed.
* Sliders adjust what categories are emphasized in the ranking aglorithms.
* Double click a players name to see advanced stats and trend analysis.


###Installation
Since this tool is not in executable form yet it must be run as a Python script.
* Copy all three python files into a single folder
* Copy all three images from the /Images folder into the same folder
* Ensure that nessesary Python modules are installed (see Requirements)
* Run DraftDayTool.py from the command line

###Requirements:
* pyqt5, numpy, scipy, matplotlib

