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
		self.plotTab = self.tabWidget.plotTab
		self.axesTab = self.tabWidget.axesTab

		self.setCentralWidget(self.tabWidget)
		self.resize(450, 650)

	def importPlotItem(self, line = None):
		ItemWidget = self.plotTab.addPlotItem(line)
		values     = ItemWidget.getLineValues()
		ItemWidget.doubleClicked.connect(lambda val = values :self.plotTab.setPanelVal(val))
		return ItemWidget



	def importPlotItems(self, lineDict = None):
		ItemWidgets = []
		try:
			self.plotTab.plotListWidget.clear()
			for index in lineDict:
				ItemWidget = self.importPlotItem(lineDict[index])
				ItemWidgets.append(ItemWidget)
			return ItemWidgets
		except:
			print  'importPlorItemError'
			return []



class graphTabWidget(QTabWidget):
	def __init__(self, parent = None):
		super(graphTabWidget, self).__init__(parent)
		self.plotTab = PlotPropertyTab()
		self.axesTab = AxesPropertyTab()
		self.addTab(self.plotTab, 'Plot Line')
		self.addTab(self.axesTab, 'Axes')

class PlotPropertyTab(QWidget):
	def __init__(self, parent=None):
		super(PlotPropertyTab, self).__init__(parent)
		self.plotListWidget = QListWidget()
		self.controlPanel   = QWidget()
		

		self.plotListWidget.setFixedWidth(100)
		
		self.HBox0  = QHBoxLayout()
		self.HBox0.addWidget(self.plotListWidget)
		self.HBox0.addWidget(self.controlPanel)

		self.controlPanelUI()
		self.setLayout(self.HBox0)


	def controlPanelUI(self):
		self.visQCombo = QComboBox()
		self.visQCombo.addItem("Hide", userData = 0)
		self.visQCombo.addItem("Show", userData = 1)

		self.applyUI   = QPushButton('Apply')
		self.cancleUI  = QPushButton('Cancle')
		self.nameUI    = panelUI('name:',       QLineEdit())
		self.visibleUI = panelUI('visible:', self.visQCombo)
		self.lineCUI   = panelUI('line color:', QLineEdit())
		self.lineWUI   = panelUI('line width:', QLineEdit())
		self.lineSUI   = panelUI('line style:', QComboBox())
		

		self.cVBox0  = QVBoxLayout()
		self.cHBox0  = QHBoxLayout()
		self.cVBox0.addWidget(self.nameUI)
		self.cVBox0.addWidget(self.visibleUI)
		self.cVBox0.addWidget(self.lineCUI)
		self.cVBox0.addWidget(self.lineWUI)
		self.cVBox0.addWidget(self.lineSUI)
		self.cVBox0.addStretch()
		self.cHBox0.addWidget(self.applyUI)
		self.cHBox0.addWidget(self.cancleUI)
		self.cVBox0.addLayout(self.cHBox0)
		self.controlPanel.setLayout(self.cVBox0)

	def setPanelVal(self, val):
		name, visibility = val
		self.nameUI.widget.setText(name)
		self.visibleUI.widget.setCurrentIndex(visibility)


	def addPlotItem(self, line = None):
		plotListItem = QListWidgetItem()
		ItemWidget   = plotListItemWidget(line)
		

		plotListItem.setSizeHint(ItemWidget.sizeHint())
		self.plotListWidget.addItem(plotListItem)
		self.plotListWidget.setItemWidget(plotListItem, ItemWidget)
		return ItemWidget

class panelUI(QWidget):
	def __init__(self, name = None, widget = None,  parent = None):
		super(panelUI, self).__init__(parent)
		self.name   = name
		self.layout = QHBoxLayout()
		
		if name:
			self.nameLabel = QLabel()
			self.nameLabel.setText(name)
			self.nameLabel.setFixedWidth(80)
			self.layout.addWidget(self.nameLabel)
		
		
		if widget:
			self.widget = widget
			self.layout.addWidget(self.widget)

		self.setLayout(self.layout)


class plotListItemWidget(QWidget):
	doubleClicked = Signal()
	def __init__(self, line = None, parent = None):
		super(plotListItemWidget, self).__init__(parent)
		self.lineAttri = []
		self.line      = line

		try:
			self.name = self.line.name()
		except:
			self.name = 'None'

		self.nameLabel = QLabel(self.name)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.nameLabel)
		self.setLayout(self.layout)


	def getLineValues(self):
		name       = self.line.line_name()
		visibility = self.line.isVisible()
		return name, visibility


	def mouseDoubleClickEvent(self, event):
		self.doubleClicked.emit()
		event.accept()



class AxesPropertyTab(QWidget):
	def __init__(self, parent=None):
		super(AxesPropertyTab, self).__init__(parent)
		self.plotList = QListWidget()

		self.HBox0 = QHBoxLayout()
		self.HBox0.addWidget(self.plotList)
		self.setLayout(self.HBox0)



def run():
	app = QApplication(sys.argv)
	# MainWindow = listItem()
	MainWindow = graphProperty()
	MainWindow.tabWidget.plotTab.addPlotItem('a')
	MainWindow.show()
	app.exec_()


# run()