from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3
import sys
import codecs
import re


def interpret(com, team, team2):
	if "makes 2-pt" in com:
		team[0]+=2
		team[1]+=1
		team[2]+=1
	if "misses 2-pt" in com:	
		team[1]+=1
	if "makes 3-pt" in com:
		team[0]+=3
		team[1]+=1
		team[2]+=1
		team[5]+=1
		team[6]+=1
	if "misses 3-pt" in com:
		team[1]+=1
		team[5]+=1
	if "makes free throw" in com:
		team[0]+=1
		team[3]+=1
		team[4]+=1
	if "misses free throw" in com:
		team[3]+=1
	if "Offensive rebound" in com:
		team[7]+=1
		team[8]+=1
	if "Defensive rebound" in com:
		team[8]+=1
	if "foul" in com:
		team[12]+=1
	if "Turnover" in com:
		team[11]+=1
	if "block" in com:
		team2[10]+=1
	if "steal" in com:
		team2[9]+=1	
	return team, team2

def getPage(url, num):
	g = open('last5min.txt', 'w') 
	page = urlopen(url)
	soup = BeautifulSoup(page.read(), "html.parser")
	teamA=teamB=""	
	for k in soup.find_all('tr'):
		a=0
		for z in k.find_all('th'):
			if a==1:
				teamA=z.findAll(text=True)
			if a==5:
				teamB=z.findAll(text=True)
			a+=1
		for j in k.find_all('td'):
			text=j.findAll(text=True)
			for l in text:
				g.write(l)
			g.write(",")
		g.write("\n")
	g.close()
	f=open('last5min.txt', 'r')
	teamOne=[0,0,0,0,0,0,0,0,0,0,0,0,0]
	teamTwo=[0,0,0,0,0,0,0,0,0,0,0,0,0]
	frt=reset=0
	for line in f:
		rows=line.split(",")
		if len(rows)>1:

			if rows[1]=="Start of 4th quarter":
				frt=1
			time=rows[0]
			tpart=time.split(":")
			sec=tpart[1].split(".")
			time=int(tpart[0])+int(sec[0])/100
			if frt==1 and time<5 and reset==0:
				reset=1
				firstPartOne=teamOne
				firstPartTwo=teamTwo
				teamOne=[0,0,0,0,0,0,0,0,0,0,0,0,0]
				teamTwo=[0,0,0,0,0,0,0,0,0,0,0,0,0]
			if len(rows[1])>2:
				teamOne, teamTwo=interpret(rows[1],teamOne, teamTwo)
			else:
				teamTwo, teamOne=interpret(rows[5],teamTwo, teamOne)
	#0 points, 1fga, 2fgm, 3fta, 4ftm, 5tpa, 6tpm
	#7 oreb, 8reb, 9stl, 10,blk, 11tov, 12pf
	one=[num,teamA[0],teamB[0]]	
	two=[num,teamA[0],teamB[0]]
	for i in range(len(firstPartOne)):
		one.append(firstPartOne[i])
		two.append(teamOne[i])
	for i in range(len(teamOne)):
		one.append(firstPartTwo[i])
		two.append(teamTwo[i])
	return one, two

months=["october","november","december","january","february","march","april"]
urlList=[]
for month in months:
	url="http://www.basketball-reference.com/leagues/NBA_2016_games-"+month+".html"
	try:
		page = urlopen(url)
	except:
		print("bad!", url)
	soup = BeautifulSoup(page.read(), "html.parser")
	stop=False
	for l in soup.find_all('table', {'class': 'suppress_glossary sortable stats_table'}):
		for k in l.find_all('tr'):
			if stop==False:
				for z in k.find_all('th'):
					if "Playoffs" in z.findAll(text=True):
						stop=True
				for j in k.find_all('td'):
					for m in j.find_all('a'):
						n=m.get('href',None)
						if "boxscores" in n:
							parts=n.split("/")
							urlList.append(parts[2])

	
conn = sqlite3.connect('2016LastFive.db')
cur = conn.cursor() 
try: cur.execute("DROP TABLE FirstFourty;")
except: print("table not found")
try: cur.execute("DROP TABLE LastFive;")
except: print("table not found")
	#0 points, 1fga, 2fgm, 3fta, 4ftm, 5tpa, 6tpm
	#7 oreb, 8reb, 9stl, 10,blk, 11tov, 12pf
cur.execute("CREATE TABLE FirstFourty (`g_num`,`team_a`,`team_b`,`a_pts`,`a_fga`,`a_fgm`,`a_fta`,`a_ftm`,`a_tpa`,`a_tpm`,`a_oreb`,`a_reb`,`a_stl`,`a_blk`,`a_tov`,`a_pf`,`b_pts`,`b_fga`,`b_fgm`,`b_fta`,`b_ftm`,`b_tpa`,`b_tpm`,`b_oreb`,`b_reb`,`b_stl`,`b_blk`,`b_tov`,`b_pf`);")	
cur.execute("CREATE TABLE LastFive (`g_num`,`team_a`,`team_b`,`a_pts`,`a_fga`,`a_fgm`,`a_fta`,`a_ftm`,`a_tpa`,`a_tpm`,`a_oreb`,`a_reb`,`a_stl`,`a_blk`,`a_tov`,`a_pf`,`b_pts`,`b_fga`,`b_fgm`,`b_fta`,`b_ftm`,`b_tpa`,`b_tpm`,`b_oreb`,`b_reb`,`b_stl`,`b_blk`,`b_tov`,`b_pf`);")	
count=1
conn.commit()
for i in urlList:
	url="http://www.basketball-reference.com/boxscores/pbp/"+i
	try:	
		A,B=getPage(url,count)
		cur.execute('INSERT INTO FirstFourty VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',  A)
		cur.execute('INSERT INTO LastFive VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',  B)
		conn.commit()
	except:
		print("bad:",url)
	if count%100==0:
		print(count/100*8.3,"%")
	count+=1
	
