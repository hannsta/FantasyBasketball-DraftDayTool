from PyQt5.QtCore import pyqtProperty, Qt, QVariant, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
global old
import rankings	
import helpDialogs as help
import numpy as np
import sqlite3
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
class HelpDialog(QWidget):
	def __init__(self, fnt):
		QWidget.__init__(self)
		self.setWindowTitle("Help")
		scroll = QScrollArea()
		expText,title=fnt()
		self.nameLabel=QLabel(title, self)
		self.nameLabel.move(15,10)
		self.nameLabel.setFont(QFont("Times", 12, QFont.Bold))
		self.textD=QTextEdit(self)
		self.textD.move(0,50)
		self.textD.setFixedHeight(350)
		self.textD.setFixedWidth(350)
		self.textD.textCursor().insertHtml(expText)
		self.textD.setReadOnly(True)
class MyPopup(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle("Player Stats")
		self.nameLabel=QLabel("", self)
		self.nameLabel.move(15,10)
		self.nameLabel.setFont(QFont("Times", 12, QFont.Bold))
	def setPlayer(self, playerName, leagueSt):
		self.nameLabel.setText(playerName)
		tables=rankings.getAverages(playerName)
		careerAverages=tables[0]
		fronthalf=tables[1][0]
		backhalf=tables[2][0]
		self.label1=QLabel("Career Averages", self)
		self.label1.move(15,35)
		self.label1.setFont(QFont("Times", 8, QFont.Bold))
		self.playerStatsTable = QTableWidget(len(careerAverages), 15, self)
		self.playerStatsTable.setHorizontalHeaderLabels(["Year","Team", "GP", "Min","Pts","3Pt","FGA","FG%","FTA","FT%","Reb","Ast","Stl","Blk","Tov"])
		self.playerStatsTable.verticalHeader().setVisible(True)
		self.playerStatsTable.move(15,50)
		playerTableHeight=len(careerAverages)*20+25
		self.playerStatsTable.setFixedHeight(playerTableHeight)
		self.playerStatsTable.setFixedWidth(620)
		for i in range(0,16):
			self.playerStatsTable.setColumnWidth(i,40)
		for i in range(len(careerAverages)):
			for j in range(len(careerAverages[i])):
				statCat = QTableWidgetItem()
				dataLine=careerAverages[i][j]
				if j==7 or j==9:
					dataLine=dataLine*100
				try:
					if dataLine>10:
						statCat.setData(Qt.DisplayRole, round(dataLine,1))
					else:
						statCat.setData(Qt.DisplayRole, round(dataLine,2))
				except:
					statCat.setData(Qt.DisplayRole, dataLine)
				self.playerStatsTable.setItem(i, j, statCat)
			self.playerStatsTable.setRowHeight(i, 20)
		self.figure = plt.figure()
		self.figure.set(facecolor='none')
		self.canvas = FigureCanvas(self.figure)
		self.canvas.setParent(self)
		self.canvas.move(-60,playerTableHeight+60)
		self.canvas.setFixedHeight(300)
		self.canvas.setFixedWidth(760)
		self.plot(playerName,leagueSt)
		self.label2=QLabel("Individual Game Scores", self)
		self.label2.move(15,playerTableHeight+70)
		self.label2.setFont(QFont("Times", 8, QFont.Bold))
		self.slideHelp = QPushButton(self)
		self.slideHelp.clicked.connect(lambda func: self.ExplainPopUp())
		self.slideHelp.setIcon(QIcon('help.png'))
		self.slideHelp.setIconSize(QSize(17,17))
		self.slideHelp.setFixedWidth(15)
		self.slideHelp.setFixedHeight(15)
		self.slideHelp.move(160,playerTableHeight+70)
		self.label3=QLabel("2015 - Half Season Averages", self)
		self.label3.move(15,playerTableHeight+360)
		self.label3.setFont(QFont("Times", 8, QFont.Bold))
		self.thisyearTable = QTableWidget(2, 15, self)
		self.thisyearTable.setHorizontalHeaderLabels(["Year","Team", "GP", "Min","Pts","3Pt","FGA","FG%","FTA","FT%","Reb","Ast","Stl","Blk","Tov"])
		self.thisyearTable.verticalHeader().setVisible(True)
		self.thisyearTable.move(15,playerTableHeight+380)
		self.thisyearTable.setFixedHeight(65)
		self.thisyearTable.setFixedWidth(620)
		for i in range(0,16):
			self.thisyearTable.setColumnWidth(i,40)
		for j in range(len(fronthalf)):
			statCat = QTableWidgetItem()
			statCat2 = QTableWidgetItem()
			dataLine=fronthalf[j]
			dataLine2=backhalf[j]
			if j==7 or j==9:
				dataLine=dataLine*100
				dataLine2=dataLine2*100
			try:
				if dataLine>10:
					statCat.setData(Qt.DisplayRole, round(dataLine,1))
					statCat2.setData(Qt.DisplayRole, round(dataLine2,1))
				else:
					statCat.setData(Qt.DisplayRole, round(dataLine,2))
					statCat2.setData(Qt.DisplayRole, round(dataLine2,2))
			except:
				statCat.setData(Qt.DisplayRole, dataLine)
				statCat2.setData(Qt.DisplayRole, dataLine2)
			self.thisyearTable.setItem(0, j, statCat)
			self.thisyearTable.setItem(1, j, statCat2)
		self.thisyearTable.setRowHeight(0, 20)
		self.thisyearTable.setRowHeight(1, 20)
	def plot(self,playerName,leagueSt):
		self.figure.clear() 
		plotData=rankings.getCareerPlot(playerName, leagueSt)
		x=plotData[0]
		y=plotData[1]
		x=np.subtract(x,201000)
		min=int(x[0]/100)
		max=int(x[-1]/100)
		years=[]
		stats=[]
		yearNames=[]
		for j in range(min,max+1):
			year=[]
			stat=[]
			yearName=2010+j
			years.append(year)
			stats.append(stat)
			yearNames.append(yearName)
		for i in range(len(x)):
			for j in range(min,max+1):
				if x[i] > j*100 and i<(j+1)*100:
					years[j-min].append(x[i])
					stats[j-min].append(y[i])
		ax = self.figure.add_subplot(111)
		colors=["Cadetblue","sage","darkgreen","navy","mediumorchid"]
		for i in range(0,len(years)):
			ax.scatter(years[i],stats[i],color=colors[i], s=4)
		ax.plot(np.unique(years[-1]), np.poly1d(np.polyfit(years[-1],stats[-1], 2))(np.unique(years[-1])))
		ax.xaxis.set_ticks(np.arange(x[0], x[-1], 100))
		ax.set_xlim([x[0],x[-1]])	
		ax.set_ylim([-10,25])
		ax.xaxis.set_ticklabels(yearNames)
		ax.yaxis.set_ticks([-5.04,-.067,2.47,5.45,7.6,11.5])
		ax.yaxis.grid()
		ax.yaxis.set_ticklabels(["0", "50%","25%","10%","5%","1%"])
		# refresh canvas
		for tick in ax.xaxis.get_major_ticks():
				tick.label.set_fontsize(10) 
		for tick in ax.yaxis.get_major_ticks():
				tick.label.set_fontsize(10) 
		self.canvas.draw()
	def ExplainPopUp(self):
		self.p= HelpDialog(help.IndGamesExp)
		self.p.setGeometry(500, 100, 350, 400)
		self.p.show()
class Window(QWidget):
	def __init__(self, parent=None):
		global old
		super(Window, self).__init__(parent)
		old=True
		rankings.createTables()
		self.createGUI()
		self.myPlayerCount=0
		self.oppPlayerCount=0
		self.teamTotals=[0,0,0,0,0,0,0,0,0]
		self.oppTotals=[0,0,0,0,0,0,0,0,0]
		self.leagueSt = rankings.leagueStDev()
	def createGUI(self):
		self.figure = plt.figure()
		self.figure.set(facecolor='none')
		self.slideHelp = QPushButton(self)
		self.slideHelp.clicked.connect(lambda:self.HelpPopUp("1"))
		self.slideHelp.setIcon(QIcon('help.png'))
		self.slideHelp.setIconSize(QSize(17,17))
		self.slideHelp.setFixedWidth(15)
		self.slideHelp.setFixedHeight(15)
		self.slideHelp.move(850,35)

		#self.slideHelp.setStyleSheet("background-color: none")
		self.canvas = FigureCanvas(self.figure)
		self.canvas.setParent(self)
		self.canvas.move(695,220)
		self.canvas.setFixedHeight(200)
		self.canvas.setFixedWidth(405)
		self.statTable=rankings.loadTable(0)
		for i in self.statTable:
			i.append(i[-1])
		self.table = QTableWidget(461, 14, self)
		self.myTeamTable = QTableWidget(15, 2, self)
		for i in range(15):
			self.myTeamTable.setRowHeight(i, 17)
			self.myTeamTable.setRowHeight(i, 17)
		self.myTeamTable.setHorizontalHeaderLabels(["My Team",""])
		self.myTeamTable.verticalHeader().setVisible(True)
		self.myTeamTable.move(740,430)
		self.myTeamTable.setFixedHeight(150)
		self.myTeamTable.setFixedWidth(160)
		self.oppTeamTable = QTableWidget(150, 2, self)
		self.oppTeamTable.setHorizontalHeaderLabels(["Opp Players", ""])
		self.oppTeamTable.verticalHeader().setVisible(True)
		self.oppTeamTable.move(905,430)
		self.oppTeamTable.setFixedHeight(150)
		self.oppTeamTable.setFixedWidth(160)
		for i in range(150):
			self.oppTeamTable.setRowHeight(i, 17)
		self.oppTeamTable.setColumnWidth(0,92)
		self.myTeamTable.setColumnWidth(0,97)
		self.oppTeamTable.setColumnWidth(1,20)
		self.myTeamTable.setColumnWidth(1,20)
		self.setData()
		categories=["Pts", "3Pts", "FG%", "FT%", "Reb", "Ast", "Stl", "Blk","Tov"]
		self.table.setHorizontalHeaderLabels(["Name", "Pts", "3Pts", "FG%", "FT%", "Reb", "Ast", "Stl", "Blk","Tov","Total", "Adj Tot","",""])
		self.table.verticalHeader().setVisible(True)
		#self.myTeamTable.horizontalHeader().setStretchLastSection(True)
      
		for i in range(0,13):
			self.table.resizeColumnToContents(i)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.setSortingEnabled(True)
		self.table.move(10,30)
		self.table.setFixedHeight(550)
		self.table.setFixedWidth(705)
		self.table.setColumnWidth(13, 30) 
		self.table.setColumnWidth(14, 30) 
		#self.table.itemClicked.connect(self.coloring)
		self.table.doubleClicked.connect(self.playerStats)
		#Slider
		self.sliders=[]
		self.oppLabels=[]
		self.teamLabels=[]
		self.labela=QLabel("Category Weighting", self)
		self.labela.move(730,35)
		self.labela.setFont(QFont("Times", 8, QFont.Bold))
		for i in range(0,9):
			slider = QSlider(Qt.Vertical, self)
			slider.setMinimum(0)
			slider.setMaximum(10)
			slider.setValue(10)
			slider.setFixedHeight(60)
			slider.setFixedWidth(20)
			slider.setTickPosition(QSlider.TicksLeft)
			slider.setTickInterval(1)
			self.sliders.append(slider)
			slider.move(730+30*i,60)
			label=QLabel(categories[i], self)
			label.move(735+30*i,120)
			#teamLabel=QLabel("0.00", self)
			#teamLabel.move(735+30*i,400)
			#self.teamLabels.append(teamLabel)
			#oppLabel=QLabel("0.00", self)
			#oppLabel.move(735+30*i,370)
			#self.oppLabels.append(oppLabel)
		self.labelb=QLabel("Time Interval", self)
		self.labelb.move(730,142)
		self.labelb.setFont(QFont("Times", 8, QFont.Bold))
		self.timelabel1=QLabel("Full Season", self)
		self.timelabel1.move(730,185)
		self.timelabel2=QLabel("Last Game", self)
		self.timelabel2.move(960,185)
		self.gameSlider = QSlider(Qt.Horizontal, self)
		self.gameSlider.setMinimum(0)
		self.gameSlider.setMaximum(82)
		self.gameSlider.setValue(0)
		self.gameSlider.setTickPosition(QSlider.TicksBelow)
		self.gameSlider.setTickInterval(5)
		self.gameSlider.move(740, 165)
		self.gameSlider.setFixedWidth(250)
		self.gameSlider.setFixedHeight(20)
		upTable = QPushButton('Update Table', self)
		upTable.clicked.connect(self.updateTable)
		upTable.move(1000,30)
		self.setGeometry(100, 100, 1100, 600)
		self.setWindowTitle("Draft Day Tool")
		self.graphLabel=QLabel("Team Averages", self)
		self.graphLabel.move(730,210)
		self.graphLabel.setFont(QFont("Times", 8, QFont.Bold))
		self.graphHelp = QPushButton(self)
		self.graphHelp.clicked.connect(lambda:self.HelpPopUp("2"))
		self.graphHelp.setIcon(QIcon('help.png'))
		self.slideHelp.setIconSize(QSize(17,17))
		self.graphHelp.setFixedWidth(15)
		self.graphHelp.setFixedHeight(15)
		self.graphHelp.move(830,210)
		self.show()
	def plot(self):
		self.figure.clear() 
		x=rankings.getMyTeam()
		y=rankings.getOppTeam()
		if not y[0]:
			y=[0,0,0,0,0,0,0,0,0]
		if not x[0]:
			x=[0,0,0,0,0,0,0,0,0]
		z=np.arange(9)
		# create an axis
		ax = self.figure.add_subplot(111)
		# discards the old graph
		#ax.hold(False)
		# plot data
		# plot data
		oppTeam=ax.bar(z+.5,y,.15,color='lightsteelblue')
		myTeam=ax.bar(z,x,.5,color='dimgrey')
		if sorted(x)[-1]<4 and sorted(y)[-1]<4:
			ax.set_ylim([-1,4])
		else:	
			ax.set_ylim([-1,6])
		ax.set_xticks(z+.35)
		ax.set_xticklabels(('Pts','3Pt','FG%','FT%','Reb','Ast','Stl','Blk','Tov'))
		# refresh canvas
		for tick in ax.xaxis.get_major_ticks():
				tick.label.set_fontsize(10) 
		for tick in ax.yaxis.get_major_ticks():
				tick.label.set_fontsize(10) 
		self.canvas.draw()
	def setData(self):
		self.cellcount=0
		for i in self.statTable:
			nameItem = QTableWidgetItem(i[0])
			for j in range(1,12):
				colorItem1 = QTableWidgetItem()
				if j<10:
					colorItem1.setData(Qt.DisplayRole, round(i[j],3))
				else:
					colorItem1.setData(Qt.DisplayRole, round(i[j],2))
				self.table.setItem(self.cellcount, j, colorItem1)
			removeP = QPushButton(self.table)
			removeP.clicked.connect(self.removePlayer)
			removeP.setIcon(QIcon('removePlayer.png'))
			removeP.setIconSize(QSize(24,24))
			addP = QPushButton(self.table)
			addP.setIcon(QIcon('takePlayer.png'))
			addP.setIconSize(QSize(24,24))
			removeP.setFixedWidth(24)
			addP.setFixedWidth(24)
			addP.clicked.connect(self.addPlayer)
			self.table.setItem(self.cellcount, 0, nameItem)
			self.table.setCellWidget(self.cellcount, 12, removeP)
			self.table.setCellWidget(self.cellcount, 13, addP)
			self.cellcount+=1
		self.coloring()
	def updateTable(self):
		global old
		if old:
			self.statTable=rankings.loadTable(self.gameSlider.value())
		conn = sqlite3.connect('2016Analysis.db')
		cur = conn.cursor() 
		available=[]
		query='''SELECT *
		FROM available'''
		result = cur.execute(query)
		for row in result:	
			available.append(row[0])
		self.table.clear()
		self.table.setSortingEnabled(False)
		values=[]
		for i in range(0,9):
			values.append(self.sliders[i].value())
		removes=[]
		for i in self.statTable:
			if i[0] in available:
				if old:
					i.append(i[1]*values[0]/10+i[2]*values[1]/10+i[3]*values[2]/10+i[4]*values[3]/10+i[5]*values[4]/10+i[6]*values[5]/10+i[7]*values[6]/10+i[8]*values[7]/10-i[9]*values[8]/10)
			else:
				removes.append(i)
		old = True
		for i in removes:
			self.statTable.remove(i)
		self.setData()
		self.table.setSortingEnabled(True)
		self.table.setHorizontalHeaderLabels(["Name", "Pts", "3Pts", "FG%", "FT%", "Reb", "Ast", "Stl", "Blk","Tov","Total", "Adj Tot","",""])
		self.plot()
	def removePlayer(self):
		self.oppPlayerCount+=1
		button = self.focusWidget()
		index = self.table.indexAt(button.pos())
		namez = self.table.item(index.row(),0)
		playerName=namez.text()
		rankings.removePlayer(namez.text())
		self.oppTotals=rankings.getOppTeam()
		#for i in range(0,9):
			#self.oppLabels[i].setNum(self.oppTotals[i]*self.myPlayerCount/self.oppPlayerCount)
		removeP = QPushButton(self.oppTeamTable)
		removeP.clicked.connect(self.putOppPlayerBack)
		removeP.setIcon(QIcon('removePlayer.png'))
		removeP.setIconSize(QSize(13,13))
		removeP.setFixedWidth(13)
		self.oppTeamTable.setCellWidget(self.oppPlayerCount-1, 1, removeP)
		self.table.removeRow(index.row())
		nameIt = QTableWidgetItem(playerName)
		self.oppTeamTable.setItem(self.oppPlayerCount-1, 0, nameIt)
		self.plot()
	def addPlayer(self):
		button = self.focusWidget()
		index = self.table.indexAt(button.pos())
		namez = self.table.item(index.row(),0)
		playerName=namez.text()
		rankings.addPlayer(playerName)
		self.teamTotals=rankings.getMyTeam()
		#for i in range(0,9):
		#	self.teamLabels[i].setText(str(self.teamTotals[i]))
		self.table.removeRow(index.row())
		nameIt = QTableWidgetItem(playerName)
		self.myTeamTable.setItem(self.myPlayerCount, 0, nameIt)
		removeP = QPushButton(self.myTeamTable)
		removeP.clicked.connect(self.putMyPlayerBack)
		removeP.setIcon(QIcon('removePlayer.png'))
		removeP.setIconSize(QSize(13,13))
		removeP.setFixedWidth(13)
		self.myTeamTable.setCellWidget(self.myPlayerCount, 1, removeP)
		self.myPlayerCount+=1
		self.plot()
	def putMyPlayerBack(self):
		global old
		old=False
		button = self.focusWidget()
		index = self.myTeamTable.indexAt(button.pos())
		namez = self.myTeamTable.item(index.row(),0)
		playerName=namez.text()
		rankings.myPlayerBack(playerName)
		self.myTeamTable.removeRow(index.row())
		self.updateTable()
		self.myPlayerCount-=1
	def putOppPlayerBack(self):
		global old
		old=False
		button = self.focusWidget()
		index = self.oppTeamTable.indexAt(button.pos())
		namez = self.oppTeamTable.item(index.row(),0)
		playerName=namez.text()
		rankings.myPlayerBack(playerName)
		self.oppTeamTable.removeRow(index.row())
		self.updateTable()
		self.oppPlayerCount-=1
	def playerStats(self):
		index = self.table.selectedIndexes()[0]
		namez = self.table.item(index.row(),0)
		playerName=namez.text()
		self.p=MyPopup()
		self.p.setGeometry(300, 100, 650, 600)
		self.p.setPlayer(playerName,self.leagueSt)
		self.p.show()
	def HelpPopUp(self,fnt):
		if fnt=="1":
			self.p= HelpDialog(help.gameSliders)
		if fnt=="2":
			self.p= HelpDialog(help.teamGraph)
		self.p.setGeometry(500, 100, 350, 400)
		self.p.show()
	def coloring(self):
		for j in range(0,self.cellcount):
			for i in range(1,10):	
				try:
					itz = self.table.item(j,i)
					score=float(itz.text())
					if i==9:
						score*=-1
					r=60
					g=151
					if score>4:
						score=4
					if score<-4:
						score=-4
					multiplier=95*score/4
					if multiplier>0:
						b=95-multiplier
					else:
						b=155-multiplier
					a=(abs(125-b)/125)*200+30
					self.table.item(j, i).setBackground(QColor(r,g,b,a))
				except:
					pass
if __name__ == '__main__':

	import sys

	app = QApplication(sys.argv)

	window = Window()
	window.show()

	sys.exit(app.exec_())