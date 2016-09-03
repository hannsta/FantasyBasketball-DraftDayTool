import sqlite3
import numpy
from scipy import stats

def devs(x):
	newx= []
	for i in range(0,len(x)):
		newx.append((x[i]-numpy.mean(x))/numpy.std(x))
	return newx
def createTables():
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	try: cur.execute("DROP TABLE available;")
	except: print("table not found")
	cur.execute("CREATE TABLE available (`player_name`);")	
	query = '''
	INSERT INTO `available`
	(`player_name`)
	SELECT DISTINCT `player_name`
	FROM `gamelogs`
	WHERE `year` = '2015' '''
	cur.execute(query)
	try: cur.execute("DROP TABLE taken;")
	except: print("table not found")
	cur.execute("CREATE TABLE taken (`player_name`);")	
	try: cur.execute("DROP TABLE myTeam;")
	except: print("table not found")
	cur.execute("CREATE TABLE myTeam (`player_name`);")	
	conn.commit()
	print("Available Created")
def addPlayer(name):
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	cur.execute('INSERT INTO myTeam VALUES(?)', (name,))
	cur.execute("DELETE FROM `available` WHERE `player_name` = '%s'"%name)
	conn.commit()
def removePlayer(name):	
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	cur.execute('INSERT INTO taken VALUES(?)', (name,))
	cur.execute("DELETE FROM `available` WHERE `player_name` = '%s'"%name)
	conn.commit()
def myPlayerBack(name):
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	cur.execute('INSERT INTO available VALUES(?)', (name,))
	cur.execute("DELETE FROM myTeam WHERE `player_name` = '%s'"%name)
	conn.commit()
def oppPlayerBack(name):
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	cur.execute('INSERT INTO available VALUES(?)', (name,))
	cur.execute("DELETE FROM taken WHERE `player_name` = '%s'"%name)
	conn.commit()

def getMyTeam():
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	query = '''
	SELECT avg(t.pts), avg(t.tpm), avg(t.fg), avg(t.ft), avg(t.reb),avg(t.ast), avg(t.stl), avg(t.blk), avg(t.tov)
	FROM `myTeam` as m
	INNER JOIN `devs` as t
	ON m.player_name = t.player_name
	'''
	result=cur.execute(query)
	teamTotals=[]
	for row in result:
		for i in row:
			teamTotals.append(i)
	return teamTotals
def getOppTeam():
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	query = '''
	SELECT avg(t.pts), avg(t.tpm), avg(t.fg), avg(t.ft), avg(t.reb),avg(t.ast), avg(t.stl), avg(t.blk), avg(t.tov)
	FROM `taken` as m
	INNER JOIN `devs` as t
	ON m.player_name = t.player_name
	'''
	result=cur.execute(query)
	teamTotals=[]
	for row in result:
		for i in row:
			teamTotals.append(i)
	return teamTotals
def transpose(mx):
	rows=len(mx)
	cols=len(mx[0])
	matrix=[[0 for x in range(rows)] for x in range(cols)]
	for j in range(0,cols):
		for i in range(0,rows):
			matrix[j][i]=mx[i][j]
	return matrix
def switchToAverages(games):
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	query = '''SELECT `player_name`,  avg(`pts`) as pts, avg(`tpm`) as tpm, avg(`fga`) as fga, avg(`fgm`)/avg(`fga`) as fgp, avg(`fta`) as fta, avg(`ftm`)/avg(`fta`) as ftp, avg(`reb`) as reb, avg(`ast`) as ast, avg(`stl`) as stl, avg(`blk`) as blk, avg(`tov`) as tov
	FROM `gamelogs`
	WHERE `year` = '2015' and gamenum > '%f' 
	GROUP BY `player_name`'''%games
	table=[]
	result = cur.execute(query)
	count=0
	for row in result:	
		try:
			row[3]+row[4]+row[5]+row[6]
			table.append(row)
		except:
			count+=1
	print(count, " Rows Excluded - ", len(table), " Rows Remain")
	return table
def loadTable(games):	
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	query = '''SELECT `player_name`,  avg(`pts`) as pts, avg(`tpm`) as tpm, avg(`fga`) as fga, avg(`fgm`)/avg(`fga`) as fgp, avg(`fta`) as fta, avg(`ftm`)/avg(`fta`) as ftp, avg(`reb`) as reb, avg(`ast`) as ast, avg(`stl`) as stl, avg(`blk`) as blk, avg(`tov`) as tov
	FROM `gamelogs`
	WHERE `year` = '2015' and gamenum > '%f' 
	GROUP BY `player_name`'''%games
	table=[]
	result = cur.execute(query)
	count=0
	for row in result:	
		try:
			row[3]+row[4]+row[5]+row[6]
			table.append(row)
		except:
			count+=1
	print(count, " Rows Excluded - ", len(table), " Rows Remain")
	table2=transpose(table)
	names=table2[0]
	table2.remove(table2[0])
	deviations=[]
	Tdevations=[]
	count=0
	for i in table2:
		i=numpy.asarray(i).astype(numpy.float)
		zscores=stats.zscore(i)
		deviations.append(zscores.tolist())
		#deviations.append(devs(i))
	print("Deviation Table Created..")
	predevfga=[]
	predevfta=[]
	minfga=sorted(deviations[2])[0]
	minfta=sorted(deviations[4])[0]
	for i in range(len(deviations[3])):
		predevfga.append((deviations[2][i]-minfga)*deviations[3][i])
		predevfta.append((deviations[4][i]-minfta)*deviations[5][i])
	preT=[]
	preT.append(names)
	preT.append(deviations[0])
	preT.append(deviations[1])
	devfga=numpy.asarray(predevfga).astype(numpy.float)
	devfta=numpy.asarray(predevfta).astype(numpy.float)
	zdevfga=stats.zscore(devfga)
	zdevfta=stats.zscore(devfta)
	preT.append(zdevfga.tolist())
	preT.append(zdevfta.tolist())
	#preT.append(devs(predevfga))
	#preT.append(devs(predevfta))
	preT.append(deviations[6])
	preT.append(deviations[7])
	preT.append(deviations[8])
	preT.append(deviations[9])
	preT.append(deviations[10])
	Tdeviations=transpose(preT)
	for i in Tdeviations:
		i.append(i[1]+i[2]+i[3]+i[4]+i[5]+i[6]+i[7]+i[8]-i[9])
	print("Ranking Table Complete")
	try: cur.execute("DROP TABLE devs;")
	except: print("table not found")
	cur.execute("CREATE TABLE devs (`player_name`, `pts`, `tpm`, `fg`, `ft`, `reb`, `ast`, `stl`, `blk`, `tov`);")	
	for r in range(0,len(Tdeviations)):
		t=Tdeviations[r][:-1]
		values = [(t)]
		cur.executemany('INSERT INTO `devs` VALUES (?,?,?,?,?,?,?,?,?,?)', values)
	conn.commit()
	return Tdeviations
def getAverages(playerName):
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	query = '''SELECT  `year`, `team_abv`, count(`min`), avg(`min`), avg(`pts`) as pts, avg(`tpm`) as tpm, avg(`fga`) as fga, avg(`fgm`)/avg(`fga`) as fgp, avg(`fta`) as fta, avg(`ftm`)/avg(`fta`) as ftp, avg(`reb`) as reb, avg(`ast`) as ast, avg(`stl`) as stl, avg(`blk`) as blk, avg(`tov`) as tov
	FROM `gamelogs`
	WHERE player_name = '%s' 
	GROUP BY `year`, `team_abv`'''%playerName
	table=[]
	result = cur.execute(query)
	for row in result:	
		table.append(row)
	query = '''SELECT  `year`, `team_abv`, count(`min`), avg(`min`), avg(`pts`) as pts, avg(`tpm`) as tpm, avg(`fga`) as fga, avg(`fgm`)/avg(`fga`) as fgp, avg(`fta`) as fta, avg(`ftm`)/avg(`fta`) as ftp, avg(`reb`) as reb, avg(`ast`) as ast, avg(`stl`) as stl, avg(`blk`) as blk, avg(`tov`) as tov
	FROM `gamelogs`
	WHERE player_name = '%s' and year='2015' and gamenum<'42' '''%playerName
	table2=[]
	result = cur.execute(query)
	for row in result:	
		table2.append(row)
	query = '''SELECT  `year`, `team_abv`, count(`min`), avg(`min`), avg(`pts`) as pts, avg(`tpm`) as tpm, avg(`fga`) as fga, avg(`fgm`)/avg(`fga`) as fgp, avg(`fta`) as fta, avg(`ftm`)/avg(`fta`) as ftp, avg(`reb`) as reb, avg(`ast`) as ast, avg(`stl`) as stl, avg(`blk`) as blk, avg(`tov`) as tov
	FROM `gamelogs`
	WHERE player_name = '%s' and year='2015' and gamenum>'41' '''%playerName
	table3=[]
	result = cur.execute(query)
	for row in result:	
		table3.append(row)
	return [table,table2,table3]
def leagueStDev():
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	query = '''SELECT `pts`, `tpm`, `fga`, `fgm`/`fga`, fta,`ftm`/`fta`, `reb`, `ast`,`stl`,`blk`,`tov`
	FROM `gamelogs`'''
	table=[]
	result = cur.execute(query)
	count=0
	for row in result:	
		rowz=[]
		for i in row:
			rowz.append(i)
		for i in range(2,6):
			try:
				rowz[i]+1
			except:
				rowz[i]=0
		if rowz[2]+rowz[3]+rowz[4]+rowz[5]!=0:
			table.append(rowz)
	table2=transpose(table)
	leagueDevs=[]
	leagueAvgs=[]
	for i in range(0,11):
		leagueDevs.append(numpy.std(table2[i]))
		leagueAvgs.append(numpy.mean(table2[i]))
	fga=devs(table[2])
	fta=devs(table[4])
	minfga=[x - sorted(fga)[0] for x in fga]
	minfta=[x - sorted(fta)[0] for x in fta]
	fg=numpy.multiply(minfga,devs(table[3]))
	ft=numpy.multiply(minfta,devs(table[5]))
	leagueDevs.append(numpy.std(fg))
	leagueDevs.append(numpy.std(ft))
	leagueAvgs.append(numpy.mean(fg))
	leagueAvgs.append(numpy.mean(ft))
	print("League Stats Generated")
	return [leagueAvgs,leagueDevs]
def getCareerPlot(playerName, leagueSt):
	leagueAvgs=leagueSt[0]
	leagueDevs=leagueSt[1]
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	query = '''SELECT `pts`, `tpm`, `fga`, `fgm`*1.0/`fga`, fta,`ftm`*1.0/`fta`, `reb`, `ast`,`stl`,`blk`,`tov`, `year`, `gamenum`
	FROM `gamelogs`
	WHERE `player_name`='%s'
	ORDER BY `year`, `gamenum`'''%playerName
	xtable=[]
	ytable=[]
	result = cur.execute(query)
	for row in result:
		rowz=[]
		for i in range(0,11):
			try:
				rowz.append((row[i]-leagueAvgs[i])/leagueDevs[i])
			except:
				rowz.append((0-leagueAvgs[i])/leagueDevs[i])
		fg=((rowz[2]*rowz[3])-leagueAvgs[11])/leagueDevs[11]
		ft=((rowz[4]*rowz[5])-leagueAvgs[12])/leagueDevs[12]
		sum=rowz[0]+rowz[1]+rowz[6]+rowz[7]+rowz[8]+rowz[9]-rowz[10]+fg+ft
		xtable.append(row[11]*100+row[12])
		ytable.append(sum)
	table=[xtable,ytable]
	return table
def gameScores():	
	conn = sqlite3.connect('2016Analysis.db')
	cur = conn.cursor() 
	query = '''SELECT `player_name`, `pts`, `tpm`, `fga`, `fgm`*1.0/`fga`, fta,`ftm`*1.0/`fta`, `reb`, `ast`,`stl`,`blk`,`tov`
	FROM `gamelogs`'''
	table=[]
	result = cur.execute(query)
	count=0
	for row in result:	
		rowz=[]
		for i in row:
			rowz.append(i)
		for i in range(1,11):
			try:
				rowz[i]+1
			except:
				rowz[i]=0
		if rowz[1]+rowz[2]+rowz[3]+rowz[4]+rowz[5]+rowz[6]+rowz[7]+rowz[8]+rowz[9]+rowz[10]!=0:
			table.append(rowz)
		else:
			count+=1
	table.append(["NULL TEST",0,0,0,0,0,0,0,0,0,0,0])
	print(count, " Rows Excluded - ", len(table), " Rows Remain")
	table2=numpy.transpose(table)
	table2=table2.tolist()
	names=table2[0]
	table2.remove(table2[0])
	deviations=[]
	Tdevations=[]
	count=0
	for i in table2:
		count+=1
		i=numpy.asarray(i).astype(numpy.float)
		zscores=stats.zscore(i)
		deviations.append(zscores.tolist())
	print("Game Score Table Created..")
	predevfga=[]
	predevfta=[]
	minfga=sorted(deviations[2])[0]
	minfta=sorted(deviations[4])[0]
	for i in range(len(deviations[3])):
		predevfga.append((deviations[2][i]-minfga)*deviations[3][i])
		predevfta.append((deviations[4][i]-minfta)*deviations[5][i])
	preT=[]
	preT.append(names)
	preT.append(deviations[0])
	preT.append(deviations[1])
	devfga=numpy.asarray(predevfga).astype(numpy.float)
	devfta=numpy.asarray(predevfta).astype(numpy.float)
	zdevfga=stats.zscore(devfga)
	zdevfta=stats.zscore(devfta)
	preT.append(zdevfga)
	preT.append(zdevfta)
	preT.append(deviations[6])
	preT.append(deviations[7])
	preT.append(deviations[8])
	preT.append(deviations[9])
	preT.append(deviations[10])
	Tdeviations=transpose(preT)
	for i in Tdeviations:
		i.append(i[1]+i[2]+i[3]+i[4]+i[5]+i[6]+i[7]+i[8]-i[9])
	print("Ranking Table Complete")
	try: cur.execute("DROP TABLE indvGames;")
	except: print("table not found")
	cur.execute("CREATE TABLE indvGames (`player_name`, `pts`, `tpm`, `fg`, `ft`, `reb`, `ast`, `stl`, `blk`, `tov`, `tot`);")	
	for r in range(0,len(Tdeviations)):
		t=Tdeviations[r]
		values = [(t)]
		cur.executemany('INSERT INTO `indvGames` VALUES (?,?,?,?,?,?,?,?,?,?,?)', values)
	conn.commit()
	return Tdeviations