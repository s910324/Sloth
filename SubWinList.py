#coding=utf-8
import sys
import pickle
from   PySide.QtGui  import *
from   PySide.QtCore import *

class SubWinList(QMainWindow):
	def __init__(self, parent=None):
		super(SubWinList, self).__init__(parent)
		self.fileName    = './settings/crewlist.pkg'
		self.listWidget  = QListWidget()
		self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		
		self.setWindowTitle('SubWindow Handler')
		self.setCentralWidget(self.listWidget)
		# self.setupToolbar()
		self.resize(400, 600)
		self.setMaximumWidth(400)

	def setupToolbar(self):
		self.MainToolbar  = QToolBar('Edit List') 
		addCrewAction	  = QAction('add  elem', self)
		saveListAction	  = QAction('save edit', self)
		loadListAction	  = QAction('load save', self)

		addCrewAction.triggered.connect(self.addCrew)
		saveListAction.triggered.connect(self.saveCrew)
		loadListAction.triggered.connect(self.loadCrew)

		self.MainToolbar.addAction(addCrewAction)
		self.MainToolbar.addAction(saveListAction)
		self.MainToolbar.addAction(loadListAction)

		self.addToolBar( Qt.LeftToolBarArea , self.MainToolbar)

	def addCrew(self, value = None):
		ClistWidgetItem = QListWidgetItem()

		if value == None:
			ClistWidget	= CListWidget(self.listWidget, self.listWidget.count() + 1, 'type', u'subname', 'time', 'path',)
		else:
			ClistWidget = CListWidget(self.listWidget, self.listWidget.count() + 1, value[1], value[2], value[3], value[4])

		ClistWidgetItem.setSizeHint(ClistWidget.sizeHint())

		self.listWidget.addItem(ClistWidgetItem)
		self.listWidget.setItemWidget(ClistWidgetItem, ClistWidget)
		return ClistWidget


	def saveCrew(self):
		fileName   = self.fileName
		fileHolder = open(fileName, 'wb')

		for index in xrange(self.listWidget.count()):
			listItem   = self.listWidget.item(index)
			listwidget = self.listWidget.itemWidget (listItem)
			values     = listwidget.returnVal()
			try:
				pickle.dump(values, fileHolder)
			except (EnvironmentError, pickle.PicklingError) as err:
				raise SaveError(str(err))
		
		fileHolder.close()

	def loadCrew(self):
		fileName = self.fileName
		stopFlag = 1
		values  = []
		package  = open( fileName, 'rb' )

		while(stopFlag):
			try:
				values.append( pickle.load( package ))

			except:
				stopFlag = 0
				package.close()

		self.listWidget.clear()
		for value in values:
			self.addCrew( value )
		package.close()


class CListWidget(QWidget):
	doubleClicked = Signal()
	selfDestory   = Signal()

	def __init__(self, host, count, subType, name, time, path, parent = None):
		super(CListWidget, self).__init__(parent)
		self.host    = host
		self.count   = count
		self.subType = subType
		self.name    = name
		self.time    = time
		self.path    = path
		self.subWin  = None
		self.mdiArea = None

		self.numLabel   = QLabel()
		self.typLabel   = QLabel()
		self.nameLineE  = QLineEdit()
		self.timeLabel  = QLabel()
		self.deleButton = QPushButton('x')
		
		self.setStyle()
		self.setValue(self.count, self.subType, self.name, self.time, self.path)
		self.setDesign()

	def setValue(self, num, subType, name, time, path):
		self.numLabel.setText(str(num).zfill(2))
		self.typLabel.setText(subType)
		self.nameLineE.setText(name)
		self.timeLabel.setText(time)
		self.deleButton.clicked.connect(self.distory)

	def setSubWin(self, subWin, host, tabID):
		self.subWin  = subWin
		self.mdiArea = host
		self.tabID   = tabID

	def returnSubWin(self):
		return self.subWin
		
	def raiseSubWin(self):
		if self.subWin:
			if self.subWin.isHidden() or not self.subWin.isMaximized():
				
				self.mdiArea.setActiveSubWindow(self.subWin)
				self.subWin.showMaximized()
			else:
				self.subWin.hide()
			print 'Activating subwindow #' + self.tabID


	def setDesign(self):
		self.hbox0 = QHBoxLayout()
		self.hbox1 = QHBoxLayout()
		self.vbox0 = QVBoxLayout()

		self.hbox0.addWidget(self.numLabel)
		self.hbox0.addWidget(self.typLabel)
		self.hbox0.addWidget(self.nameLineE)
		self.hbox0.addWidget(self.timeLabel)
		self.vbox0.addWidget(self.deleButton)
		self.vbox0.addStretch()

		self.hbox1.addLayout(self.vbox0)
		self.hbox1.addLayout(self.hbox0)

		self.setLayout(self.hbox1)

	def setStyle(self):
		self.numLabel.setStyleSheet(  "QLabel    { font-weight: bold; font-size: 14px; }" )
		self.typLabel.setStyleSheet(  "QLabel    { font-weight: bold; font-size: 14px; }" )
		self.timeLabel.setStyleSheet( "QLabel    { font-weight: bold; font-size: 14px; }" )
		self.nameLineE.setStyleSheet( "QLineEdit { font-weight: bold; font-size: 14px; }" )

		self.nameLineE.setFixedHeight(25)
		self.deleButton.setFixedSize(18,18)

	def distory(self):
		if self.closeChecker():
			for index in xrange(int(self.count), self.host.count(), 1):
				listItem   = self.host.item(index)
				listwidget = self.host.itemWidget (listItem)
				listwidget.moveUp()
			self.host.takeItem(self.count - 1)
			self.selfDestory.emit()


	def moveUp(self):
		self.count -= 1
		self.numLabel.setText(str(self.count).zfill(2))


	def returnVal(self):
		return [ self.count, self.typLabel.text(), self.nameLineE.text(), self.time ]


	def closeChecker(self):
		closeChk = QMessageBox()
		closeChk.setText("Close Confirm")
		closeChk.setInformativeText("This action will destory data/plotin this frame.")

		yes    = closeChk.addButton( self.tr("             Confiem Close           "), QMessageBox.ActionRole )
		no     = closeChk.addButton( self.tr("                Cancle               "), QMessageBox.ActionRole )

		closeChk.setDefaultButton(no)
		closeChk.exec_()

		if closeChk.clickedButton()   == yes:
			return True

		elif closeChk.clickedButton() == no:
			# self.showMinimized()
			# event.ignore()
			return False

		else:
			return False

	def mouseDoubleClickEvent(self, event):
		self.doubleClicked.emit()
		# self.raiseSubWin()
		event.accept()

def run():
	app = QApplication(sys.argv)
	# MainWindow = listItem()
	MainWindow = SubWinList()
	MainWindow.show()
	MainWindow.setupToolbar()
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


# run()
