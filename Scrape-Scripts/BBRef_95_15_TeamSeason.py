from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import codecs
import re
g = open('95_15CompleteGameLogsDump.txt', 'w')


teams=["DET","ATL","CLE","CHI","NOP","GSW","WAS","ORL","PHI","BOS","BKN","UTA","CHA","MIA","IND","TOR","DEN","SEA","NOK","VAN","HOU","MEM","NYK","MIL","SAS","OKC","DAL","PHX","POR","LAC","SAC","MIN","LAL","NOH","NJN"]

years=[]	
for i in range(1995,2017):
	years.append(i)
	
for t in teams:
	for y in years:
		print("http://www.basketball-reference.com/teams/"+t+"/"+str(y)+"/gamelog")
		try:
			page = urlopen("http://www.basketball-reference.com/teams/"+t+"/"+str(y)+"/gamelog")
			soup = BeautifulSoup(page.read(), "html.parser")
			for l in soup.find_all('table', {'class': 'row_summable sortable stats_table'}):
				for k in l.find_all('tr'):
					g.write(t+","+str(y)+",")
					for j in k.find_all('td'):
						text=j.findAll(text=True)
						for l in text:
							g.write(l)
						g.write(",")
					g.write("\n")
				
		except:
			print(t,y,"---does not work")