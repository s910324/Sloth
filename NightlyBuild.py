import sys
import pickle
import numpy as np
import pandas as pd
import qdarkstyle
import plotSubWin as qtplt
import expTableWidget as tw
# import expTableWindow as tww #not currently in use
from time import localtime
from  wbSubWin  import WorkBookWindow
from SubWinList import SubWinList
#import OpenFileOptions as oFile #old, move to tempfles
import pandasOpenfile  as oFile
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtGui  import QFont as QFont
from bokehPlotter  import bokehp

class Sloth(QMainWindow):
	def __init__(self, parent=None):
		super(Sloth, self).__init__(parent)

		self.tabIDCounter  = -1
		self.tabColCounter = []
		self.subWinDict    = {}

		self.prjTreeView = QTreeWidget(self)
		self.subWinList  = SubWinList(self)
		self.mdiArea = QMdiArea(self)
		self.initMenuBar()
		self.initDocker()
		self.initToolBar()
		self.statusBar().showMessage('Ready')
		self.setCentralWidget(self.mdiArea)

	def initMenuBar(self):
		menubar        = self.menuBar()
		fileMenu       = menubar.addMenu('&File')
		editMenu       = menubar.addMenu('&Edit')
		viewMenu       = menubar.addMenu('&View')
		plotMenu       = menubar.addMenu('&Plot')
		colMenu        = menubar.addMenu('&Colume')
		wksheetMenu    = menubar.addMenu('&Worksheet')
		analysisMenu   = menubar.addMenu('&Analysis')
		statisticsMenu = menubar.addMenu('&Statistics')
		imageMenu      = menubar.addMenu('&Image')
		toolsMenu      = menubar.addMenu('&Tools')
		formatMenu     = menubar.addMenu('&Format')
		windowMenu     = menubar.addMenu('&Window')
		helpMenu       = menubar.addMenu('&Help')
		
	
	def initDocker(self):
		self.projDockWidget = QDockWidget("  ::  Projects ::", self)
		self.fileDockWidget = QDockWidget("  ::   Files   ::", self)
		self.projDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
		self.fileDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
		self.projDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea and Qt.RightDockWidgetArea)
		self.fileDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea and Qt.RightDockWidgetArea)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.projDockWidget)
		self.addDockWidget(Qt.LeftDockWidgetArea, self.fileDockWidget)
		self.projDockWidget.setWidget(self.prjTreeView)
		self.fileDockWidget.setWidget(self.subWinList )

		
		
	def initToolBar(self):
		
		self.MainToolbar = QToolBar('Main operations') 
		self.plotbar     = QToolBar('plot options') 
		self.addToolBar( Qt.TopToolBarArea , self.MainToolbar)
		self.addToolBar( Qt.BottomToolBarArea , self.plotbar)
		self.initPlotLineButton()

		nextAction = QAction('Exit', self)
		self.plotbar.addAction(nextAction)
		nextAction.triggered.connect(self.test2)
		
		exitAction      = QAction('Exit', self)
		openPjAction    = QAction('New Project', self)
		openAction      = QAction('Open', self)
		newwbAction     = QAction('New WorkBook', self)
		plotAction      = QAction('Plot', self)
		stackPlotAction = QAction('Stack Plot', self)
		testAction      = QAction('Test', self)
		addColAction    = QAction('Add Column', self)
		addRowAction    = QAction('Add Row', self)
		rmvColAction    = QAction('remove Column', self)
		rmvRowAction    = QAction('remove Row', self)        
		setXAction      = QAction('Set As X', self)
		setYAction      = QAction('Set As Y', self)
		setZAction      = QAction('Set As Z', self)
		
		exitAction.triggered.connect(self.CreateTableSub)
		openPjAction.triggered.connect(self.OpenNewProject)
		openAction.triggered.connect(self.OpenFile)
		newwbAction.triggered.connect(self.OpenNewWorkBook)
		plotAction.triggered.connect(     lambda stack = 0 : self.PlotData(stack))
		stackPlotAction.triggered.connect(lambda stack = 1 : self.PlotData(stack))
		testAction.triggered.connect(self.test)
		addColAction.triggered.connect(self.addCol)
		addRowAction.triggered.connect(self.addRow)
		rmvColAction.triggered.connect(self.rmvCol)
		rmvRowAction.triggered.connect(self.rmvRow)        
		setXAction.triggered.connect( lambda axis = 0 : self.setAxis(axis) )
		setYAction.triggered.connect( lambda axis = 1 : self.setAxis(axis) )
		setZAction.triggered.connect( lambda axis = 2 : self.setAxis(axis) )
		
		
		self.MainToolbar.addAction(exitAction)
		self.MainToolbar.addAction(openPjAction)
		self.MainToolbar.addAction(openAction)
		self.MainToolbar.addAction(newwbAction)
		self.MainToolbar.addAction(plotAction)
		self.MainToolbar.addAction(stackPlotAction)
		self.MainToolbar.addAction(testAction)
		self.MainToolbar.addAction(addColAction)
		self.MainToolbar.addAction(addRowAction)
		self.MainToolbar.addAction(rmvColAction)
		self.MainToolbar.addAction(rmvRowAction)
		self.MainToolbar.addAction(setXAction)
		self.MainToolbar.addAction(setYAction)
		self.MainToolbar.addAction(setZAction)
		
		
	def initPlotLineButton(self):
		lineMenu    = QMenu()        
		dotMenu     = QMenu()
		dotLineMenu = QMenu()
		
		linePlotButton    = QToolButton()
		dotPlotButton     = QToolButton()
		dotLinePlotButton = QToolButton()
		self.plotbar.addWidget(linePlotButton)
		self.plotbar.addSeparator()
		self.plotbar.addWidget(dotPlotButton)
		self.plotbar.addSeparator()
		self.plotbar.addWidget(dotLinePlotButton)
		self.plotbar.addSeparator()
		
		lineAction        = QAction('Line', self)
		hStepsAction      = QAction('Horizontal Step', self)
		vStepsAction      = QAction('Vertical Step', self)
		spineAction       = QAction('Spine Connect', self)
		
		dotAction        = QAction('Scatter', self)
		yErrorAction     = QAction('Y Error', self)
		xyErrorAction    = QAction('XY Error', self)
		vDropLineAction  = QAction('Verticle Drpo Line', self)
		bubbleAction     = QAction('Bubble', self)
		colorMapAction   = QAction('Color Map', self)        
		bPlusCMapAction  = QAction('Bubble + Color Map', self)        
		
		dotLineAction      = QAction('Line + Symbol', self)
		lineSeriesAction   = QAction('Line Series', self)
		twoSegmentAction   = QAction('2 Point Segment', self)
		threeSegmentAction = QAction('3 Point Segment', self)
		
		linePlotButton.setPopupMode(    QToolButton.MenuButtonPopup )
		dotPlotButton.setPopupMode(     QToolButton.MenuButtonPopup )
		dotLinePlotButton.setPopupMode( QToolButton.MenuButtonPopup )
		
		linePlotButton.setDefaultAction(    lineAction    )
		dotPlotButton.setDefaultAction(     dotAction    )
		dotLinePlotButton.setDefaultAction( dotLineAction )
		
		lineMenu.addAction(lineAction)
		lineMenu.addAction(hStepsAction)
		lineMenu.addAction(vStepsAction)
		lineMenu.addAction(spineAction)
		
		dotMenu.addAction(dotAction       )
		dotMenu.addAction(yErrorAction    )
		dotMenu.addAction(xyErrorAction   )
		dotMenu.addAction(vDropLineAction )
		dotMenu.addAction(bubbleAction    )
		dotMenu.addAction(colorMapAction  )
		dotMenu.addAction(bPlusCMapAction )
		
		dotLineMenu.addAction(dotLineAction      )
		dotLineMenu.addAction(lineSeriesAction   )
		dotLineMenu.addAction(twoSegmentAction   )
		dotLineMenu.addAction(threeSegmentAction )
		
		linePlotButton.setMenu(    lineMenu    )
		dotPlotButton.setMenu(     dotMenu     )        
		dotLinePlotButton.setMenu( dotLineMenu )
		
		lineAction.triggered.connect(self.test2)
				

	def addCol(self, num = 1):
		try:
			subWinHandle = self.mdiArea.currentSubWindow()
			workBookWin  = subWinHandle.widget()
			tableHandle  = workBookWin.centralWidget()
			labelList    = tableHandle.addCol(num)

			for label in labelList:
				print 'Tab #{0} append column #{1}'.format(workBookWin.getID(), label)

		except AttributeError:
			print 'No active/valid workbook for column appending.'
		
		
	def addRow(self):
		try:
			subWinHandle = self.mdiArea.currentSubWindow()
			workBookWin  = subWinHandle.widget()
			tableHandle  = workBookWin.centralWidget()
			
			if tableHandle.currentRow() > 2:
				tableHandle.insertRow(tableHandle.currentRow())
				print 'Tab #{0} append row #{1}'.format(workBookWin.getID(),  + tableHandle.currentRow())
				
		except AttributeError:
			print 'No active/valid workbook for  row appending.'
	
	
	def rmvCol(self):
		try: 
			subWinHandle = self.mdiArea.currentSubWindow()
			workBookWin  = subWinHandle.widget()
			tableHandle  = workBookWin.centralWidget()
			labelList    = tableHandle.rmvCol()

			for label in labelList:
				print 'Tab #{0} remove column #{1}'.format(workBookWin.getID(), label)
				
		except AttributeError:
			print 'No active/valid workbook for column removing.'

	def rmvRow(self):
		try:
			subWinHandle = self.mdiArea.currentSubWindow()
			workBookWin  = subWinHandle.widget()
			tableHandle  = workBookWin.centralWidget()
			labelList    = tableHandle.rmvRow()
			
			for label in labelList:
				print 'Tab #{0} remove row #{1}'.format(workBookWin.getID(), label)

		except AttributeError:
			print 'No active/valid workbook for row removing.'
	
	
	def setAxis(self, axis):
		try:
			subWinHandle = self.mdiArea.currentSubWindow()
			tableHandle  = subWinHandle.widget().centralWidget()
			tableHandle.setAxis(axis)
		except AttributeError:
			print 'No active/valid workbook for set axis operation.'

	def OpenNewProject(self):
		self.prjTreeView.setColumnCount(2)
		projFolder =  QTreeWidgetItem( self.prjTreeView  )
		projItem   =  QTreeWidgetItem( projFolder        )
		projFolder.setText( 0, "Project 1" )
		projItem.setText(   0, "Item 1"    )
		projItem.setText(   1, "Yes"       )
	

	
	def AddWinListItem(self, subWinTitle, wintype, tabID, path = ''):
		lt   = localtime()
		now  = u'{0}/{1}/{2}-{3}:{4}'.format(lt.tm_year, str(lt.tm_mon), str(lt.tm_mday), str(lt.tm_hour), str(lt.tm_min))
		
		subWinHandle = self.subWinList.addCrew( [ wintype, subWinTitle, now, path ] )
		subWinHandle.doubleClicked.connect(      lambda ID=tabID  :  self.RaiseSubWin(ID)     )
		subWinHandle.selfDestory.connect(        lambda ID=tabID  :  self.DestorySubWin(ID)   )


	def RaiseSubWin(self, tabID):
		window = self.subWinDict[tabID]
		if window.isHidden() or not window.isMaximized():
			self.mdiArea.setActiveSubWindow(window)
			window.showMaximized()
		else:
			window.hide()
		
		print 'Activating subwindow #' + str(tabID)


	def DestorySubWin(self, tabID):
		window = self.subWinDict[tabID]
		window.widget().unlock()
		if window.close():

			# self.mdiArea.removeSubWindow(window) #**content has been deleted, this will GC by system
			window.widget().close()
			print 'Destory Subwindow #' + str(tabID)

		else:
			window.widget().lock()
			print 'Unhook  Subwindow #' + str(tabID)


	def OpenNewWorkBook(self):
		tableHandle, subWinHandle, tabID = self.CreateTableSub()
		subWinTitle = "Untitled " + str(tabID)
		subWinHandle.setWindowTitle(subWinTitle)
		self.AddWinListItem(subWinTitle, 'sheet', tabID)
		tableHandle.setRowCount(200)
		self.addCol(3)


	def OpenFile(self):
		self.preViewWin = oFile.PreView()
		self.preViewWin.OpenFile()
		if self.preViewWin.exec_() == QDialog.Accepted :
			filePath, fileContainArray, headerSize = self.preViewWin.Submit()
			subWinTitle   = str(filePath.split('/')[-1])
			for fileContainer in fileContainArray:
				TableHandle, subWinHandle, tabID = self.CreateTableSub()
				(rowNum, colNum) = fileContainer.shape
				self.AddWinListItem(subWinTitle, 'sheet', tabID)
				TableHandle.setRowCount(rowNum)
				self.addCol(colNum)
		
				for col in range(colNum):
					for row in range(rowNum):
						try:
							contnent =  QTableWidgetItem(unicode(str(fileContainer[col][row])))
						except UnicodeEncodeError:
							contnent =  QTableWidgetItem(unicode(fileContainer[col][row]))
						if row < headerSize:
							contnent.setBackground(QColor('#0066cc'))
							contnent.setForeground(QColor('#ffffff'))
						TableHandle.setItem(row, col, contnent)


	def SaveFile(self):
		print 'a'
		
	def SaveAllFiles(self):
		print 'b'
		
	def CreateTableSub(self):
		wbWin       = WorkBookWindow()
		tableWidget = tw.TableWidgetCustom()
		tabID       = self.AddMdiSubWindow(wbWin)
		wbWin.setID(tabID)

		wbWin.setCentralWidget(tableWidget)
		wbWin.setAttribute(Qt.WA_DeleteOnClose)
		wbWin.setMinimumSize(QSize(250,250))
		wbWin.statusBar().showMessage('Tab #' + str(tabID) )
		wbWin.showMaximized()
		self.tabColCounter.append(0)

		return tableWidget, wbWin, tabID


	def AddMdiSubWindow(self, subWindow):
		self.tabIDCounter += 1
		self.mdiArea.addSubWindow(subWindow)
		tabID  = self.tabIDCounter
		wlist  = self.mdiArea.subWindowList() 
		subWin = wlist[-1]

		self.subWinDict[tabID] = subWin		

		return self.tabIDCounter


	def PlotData(self, stack):
		try:
			subWinHandle = self.mdiArea.currentSubWindow()
			subWinTitle  = '[plot]' + subWinHandle.windowTitle()
			tableHandle  = subWinHandle.widget().centralWidget()

			plotWindow   = bokehp.PlotWindowWidget()
			# plotWindow   = qtplt.MainWindow()
			tabID        = self.AddMdiSubWindow(plotWindow)


			selectArray, dataSet = tableHandle.getSelectedData()
			for column in selectArray:
					print 'selected Columns: {0}'.format(column)
					
			# self.saveData(dataSet) 


			plotWindow.plotData(stack, dataSet)

			plotWindow.setMinimumSize(QSize(250,250))
			plotWindow.showMaximized()
			self.tabColCounter.append(-1)
			self.AddWinListItem(subWinTitle, 'Plot', tabID)
		except AttributeError:
			print 'No active/valid workbook for data plotting.'

	def saveData(self, data):
		fileName   = './savedData.pkl'
		fileHolder = open(fileName, 'wb')
		try:
			pickle.dump(data, fileHolder)
		except (EnvironmentError, pickle.PicklingError) as err:
			raise SaveError(str(err))
		
		fileHolder.close()
# ----------------------------------------remove for rapid gui test-------------------------------------------------------		
	# def closeEvent(self, event):
		
		# reply = QMessageBox.question(self, 'Message',
		# 	"Are you sure to quit?", QMessageBox.Yes | 
		# 	QMessageBox.No, QMessageBox.No)
		# if reply ==  QMessageBox.Yes:
		# 	event.accept()
		# else:
		# 	event.ignore()  
# -----------------------------------------------------------------------------------------------


	def test(self):
		try:
			subWinHandle = self.mdiArea.currentSubWindow()
			tabID        = int(subWinHandle.widget().statusBar().currentMessage().split('#')[1])
			self.a =ScriptSetVal(tabID, subWinHandle)
		except AttributeError:
			print 'No active/valid workbook for script setting.'   
	def test2(self):
		print 'a'

	def ScriptSetVal(self):
		w = QMainWindow()
		t = QTextEdit()
		self.mdiArea.addSubWindow(w)
		w.setCentralWidget(t)
		w.setAttribute(Qt.WA_DeleteOnClose)
		w.setMinimumSize(QSize(250,250))
		w.setGeometry(QRect(200, 200, 500, 500))
		
		w.show()
		
		
class ScriptSetVal(QMainWindow):
	def __init__(self, tabID, subWinHandle, parent=None):
		super(ScriptSetVal,  self).__init__(parent)
		self.tabID = tabID    
		self.subWinHandle = subWinHandle
		self.tableHandle  = subWinHandle.widget().centralWidget()
		self.initUI()
		self.initToolBar()
		self.initDocker()
		
	def initUI(self): 
		self.t = QTextEdit()
		self.initFont()
		self.setCentralWidget(self.t)
		self.setGeometry(QRect(200, 200, 410, 610))
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.show()
	
	def initToolBar(self):
		self.scriptbar    = QToolBar('plot options') 
		self.addToolBar( Qt.BottomToolBarArea , self.scriptbar)
		scriptAction = QAction('set script', self)
		self.scriptbar.addAction(scriptAction)
		scriptAction.triggered.connect(self.RelectRng)

	def initFont(self):
		self.tabStop = 4
		self.font = QFont('Courier')
		self.metrics = QFontMetrics(self.font)
		self.t.setTabStopWidth(self.tabStop * self.metrics.width(' '));
		self.font.setStyleHint(QFont.Monospace);
		self.font.setFixedPitch(True);
		self.font.setPointSize(12)
		self.p = self.t.palette()
		self.p.setColor(QPalette.Base, QColor(0, 0, 0))
		self.p.setColor(QPalette.Text, QColor(255, 255, 255))
		self.t.setPalette(self.p)
		self.t.setFont(self.font)
		self.highlighter = Highlighter(self.t.document())

	def initDocker(self):
		self.elog = QTextEdit()
		self.elogDockWidget = QDockWidget("  ::  error log ::", self)
		self.elogDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
		self.elogDockWidget.setAllowedAreas(Qt.TopDockWidgetArea and Qt.BottomDockWidgetArea)
		self.addDockWidget(Qt.BottomDockWidgetArea, self.elogDockWidget)
		self.elogDockWidget.setWidget(self.elog)
		self.p = self.elog.palette()
		self.p.setColor(QPalette.Base, QColor(0, 0, 0))
		self.p.setColor(QPalette.Text, QColor(255, 0, 0))
		self.elog.setPalette(self.p)
		self.elog.setReadOnly(True)

		  

	def RelectRng(self):
		try:
			self.selectAry = []
			if len(self.tableHandle.selectedRanges()) != 0:
				for i in range( len(self.tableHandle.selectedRanges())):
					self.leftCol  = self.tableHandle.selectedRanges()[i].leftColumn()
					self.colCount = self.tableHandle.selectedRanges()[i].columnCount()
					for currentCol in range( self.leftCol, self.leftCol + self.colCount ):
						self.selectAry.append( currentCol )
				self.leftCol  = self.tableHandle.selectedRanges()[0].leftColumn()
				self.colCount = self.tableHandle.selectedRanges()[0].columnCount()
				self.topRow   = self.tableHandle.selectedRanges()[0].topRow()
				self.rowCount = self.tableHandle.selectedRanges()[0].rowCount()
				
				rows = []
				cols = []
				for i in range(self.topRow,  self.topRow  + self.rowCount, 1):
					rows.append(i)
				for i in range(self.leftCol, self.leftCol + self.colCount, 1):
					cols.append(i)

				try:
					exec(self.t.toPlainText())
				except Exception, e:
					self.elog.moveCursor(QTextCursor.End)
					self.elog.textCursor().insertHtml('<span style="color:#FF0000">Error: '+str(e)+'</span><br>')
					

					print str(e)
			else:
				print 'workbook hava not been selected.'

		except AttributeError:
			print 'No active/valid workbook for script setting.'
	
	def setItem(self, col, row, val):
		try:
			self.tableHandle.setItem(col, row, QTableWidgetItem(str(val)))
		except Exception, e:
			print str(e)       
			
	def view(self, text):
		self.elog.moveCursor(QTextCursor.End)
		self.elog.textCursor().insertHtml('<span style="color:#FFFFFF">'+text+'</span><br>')

class Highlighter( QSyntaxHighlighter):
	def __init__(self, parent=None):
		super(Highlighter, self).__init__(parent)
 
		keywordFormat =  QTextCharFormat()
		keywordFormat.setForeground( Qt.darkBlue)
		keywordFormat.setFontWeight( QFont.Bold)
 
		keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
				"\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
				"\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
				"\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
				"\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
				"\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
				"\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
				"\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
				"\\bvolatile\\b"]
 
		self.highlightingRules = [( QRegExp(pattern), keywordFormat)
				for pattern in keywordPatterns]
 
		classFormat =  QTextCharFormat()
		classFormat.setFontWeight( QFont.Bold)
		classFormat.setForeground( Qt.darkMagenta)
		self.highlightingRules.append(( QRegExp("\\bQ[A-Za-z]+\\b"),
				classFormat))
 
		singleLineCommentFormat =  QTextCharFormat()
		singleLineCommentFormat.setForeground( Qt.red)
		self.highlightingRules.append(( QRegExp("//[^\n]*"),
				singleLineCommentFormat))
 
		self.multiLineCommentFormat =  QTextCharFormat()
		self.multiLineCommentFormat.setForeground( Qt.red)
 
		quotationFormat =  QTextCharFormat()
		quotationFormat.setForeground( Qt.darkGreen)
		self.highlightingRules.append(( QRegExp("\".*\""),
				quotationFormat))
 
		functionFormat =  QTextCharFormat()
		functionFormat.setFontItalic(True)
		functionFormat.setForeground( Qt.blue)
		self.highlightingRules.append(( QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
				functionFormat))
 
		self.commentStartExpression =  QRegExp("/\\*")
		self.commentEndExpression =  QRegExp("\\*/")
 
	def highlightBlock(self, text):
		for pattern, format in self.highlightingRules:
			expression =  QRegExp(pattern)
			index = expression.indexIn(text)
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)
 
		self.setCurrentBlockState(0)
 
		startIndex = 0
		if self.previousBlockState() != 1:
			startIndex = self.commentStartExpression.indexIn(text)
 
		while startIndex >= 0:
			endIndex = self.commentEndExpression.indexIn(text, startIndex)
 
			if endIndex == -1:
				self.setCurrentBlockState(1)
				commentLength = text.length() - startIndex
			else:
				commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()
 
			self.setFormat(startIndex, commentLength,
					self.multiLineCommentFormat)
			startIndex = self.commentStartExpression.indexIn(text,
					startIndex + commentLength);
 
if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = Sloth()
	frame.showMaximized()    
	def load_stylesheet(pyside=True):
		f = QFile("./settings/style.qss")
		if not f.exists():
			return ""
		else:
			f.open(QFile.ReadOnly | QFile.Text)
			ts = QTextStream(f)
			stylesheet = ts.readAll()
			return stylesheet	
	app.setStyleSheet(load_stylesheet())
	app.exec_()
	sys.exit
