#coding=utf-8
import sys
import pickle
from   PySide.QtGui  import *
from   PySide.QtCore import *
import pyqtgraph as pg
class graphProperty(QMainWindow):
	def __init__(self, parent=None):
		super(graphProperty, self).__init__(parent)
		self.tabWidget = graphTabWidget()
		self.setCentralWidget(self.tabWidget)
		self.resize(900, 650)


	def addPlotElements(self, line):
		plotList = self.tabWidget.plotTab.plotList
		plotlist.add



class graphTabWidget(QTabWidget):
	def __init__(self, parent = None):
		super(graphTabWidget, self).__init__(parent)
		self.plotTab = PlotProperty()
		self.axesTab = AxesProperty()
		self.addTab(self.plotTab, 'Plot Line')
		self.addTab(self.axesTab, 'Axes')

class PlotProperty(QWidget):
	def __init__(self, parent=None):
		super(PlotProperty, self).__init__(parent)
		self.plotList = QListWidget()
		self.plotList.setFixedWidth(100)
		self.controls = QWidget()
		self.HBox0    = QHBoxLayout()
		self.HBox0.addWidget(self.plotList)
		self.HBox0.addWidget(self.controls)
		self.setLayout(self.HBox0)

	# def addITem(self, line):
	# 	b = QPushButton('push')
	# 	self.HBox0.addWidget(b)
	# 	b.clicked.connect(lambda ID = line : self.setpen(ID))

	# def setpen(self, line):
	# 	line.pen = pg.mkPen(color = "#FF0000")
		
class AxesProperty(QWidget):
	def __init__(self, parent=None):
		super(AxesProperty, self).__init__(parent)
		self.plotList = QListWidget()

		self.HBox0 = QHBoxLayout()
		self.HBox0.addWidget(self.plotList)
		self.setLayout(self.HBox0)



def run():
	app = QApplication(sys.argv)
	# MainWindow = listItem()
	MainWindow = graphProperty()
	MainWindow.show()
	app.exec_()


run()