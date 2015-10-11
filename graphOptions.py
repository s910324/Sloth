#coding=utf-8
import sys
import pickle
from   PySide.QtGui  import *
from   PySide.QtCore import *

class graphProperty(QMainWindow):
	def __init__(self, parent=None):
		super(graphProperty, self).__init__(parent)
		self.fileName    = './settings/crewlist.pkg'
		self.listWidget  = QListWidget()
		self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		
		self.setWindowTitle(u'編 輯 名 單')
		self.setCentralWidget(self.listWidget)
		self.setupToolbar()
		self.resize(400, 600)
		self.setMaximumWidth(400)

	def setupToolbar(self):
		self.MainToolbar  = QToolBar(u'編輯名單') 
		addCrewAction	  = QAction(u'新增\n人員', self)
		saveListAction	  = QAction(u'儲存\n編輯', self)
		loadListAction	  = QAction(u'載入\n存檔', self)

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
			ClistWidget	= CListWidget(self.listWidget, self.listWidget.count() + 1, 4, u'無名氏')
		else:
			ClistWidget = CListWidget(self.listWidget, value[0], value[1], value[2])

		ClistWidgetItem.setSizeHint(ClistWidget.sizeHint())

		self.listWidget.addItem(ClistWidgetItem)
		self.listWidget.setItemWidget(ClistWidgetItem, ClistWidget)

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
	def __init__(self, host, count, pos, name, parent = None):
		super(CListWidget, self).__init__(parent)
		self.host  = host
		self.count = count
		self.pos   = pos
		self.name  = name

		self.numLabel   = QLabel()
		self.posCombo   = QComboBox()
		self.nameLineE  = QLineEdit()
		self.deleButton = QPushButton('x')
		
		self.setStyle()
		self.setValue(self.count, self.pos, self.name)
		self.setDesign()

	def setValue(self, num, pos, name):

		self.numLabel.setText(str(num).zfill(2))
		self.posCombo.setCurrentIndex(pos)
		self.nameLineE.setText(name)
		self.deleButton.clicked.connect(self.distory)

	def setDesign(self):
		self.hbox0 = QHBoxLayout()
		self.hbox1 = QHBoxLayout()
		self.vbox0 = QVBoxLayout()

		self.hbox0.addWidget(self.numLabel)
		self.hbox0.addWidget(self.posCombo)
		self.hbox0.addWidget(self.nameLineE)
		self.vbox0.addWidget(self.deleButton)
		self.vbox0.addStretch()

		self.hbox1.addLayout(self.hbox0)
		self.hbox1.addLayout(self.vbox0)
		self.setLayout(self.hbox1)

	def setStyle(self):
		self.numLabel.setStyleSheet(  "QLabel    { font-weight: bold; font-size: 18px; }" )
		self.posCombo.setStyleSheet(  "QComboBox { font-weight: bold; font-size: 14px; }" )
		self.nameLineE.setStyleSheet( "QLineEdit { font-weight: bold; font-size: 14px; }" )

		self.posCombo.insertItems(0, [u'  請選擇', u'  分隊長', u'  小隊長', u'  隊   員', u'  役   男'])
		self.posCombo.setFixedHeight(35)
		self.nameLineE.setFixedHeight(35)
		self.deleButton.setFixedSize(18,18)

	def distory(self):
		for index in xrange(self.count, self.host.count(), 1):
			listItem   = self.host.item(index)
			listwidget = self.host.itemWidget (listItem)
			listwidget.moveUp()
		self.host.takeItem(self.count - 1)


	def moveUp(self):
		self.count -= 1
		self.numLabel.setText(str(self.count).zfill(2))


	def returnVal(self):
		return [ self.count, self.posCombo.currentIndex(), self.nameLineE.text() ]




def run():
	app = QApplication(sys.argv)
	# MainWindow = listItem()
	MainWindow = graphProperty()
	MainWindow.show()
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


run()