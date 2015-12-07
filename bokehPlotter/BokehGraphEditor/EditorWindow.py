import sys
from   PySide               import QtGui
from   PySide.QtGui         import *
from   PySide.QtCore        import *
from   viewBoxList          import *
from   lineControlWidget    import *
from   viewBoxControlWidget import *

class EditorWindow(QGroupBox):
	def __init__(self, parent=None):
		super(EditorWindow, self).__init__(parent)
		self.resize(650, 700)
	
		self.setupLayout()

	def setupLayout(self):
		box1  = self.setupList()
		box2  = self.setupControl()
		box3  = self.setupSubmitUI()
		hbox1 = QHBoxLayout()
		vbox1 = QVBoxLayout()

		hbox1.setContentsMargins(0,0,0,0)
		hbox1.addLayout(box1)
		hbox1.addLayout(vbox1)
		vbox1.addLayout(box2)
		vbox1.addLayout(box3)
		self.setLayout(hbox1)
		self.setContentsMargins(0,0,0,0)

	def setupList(self):
		self.viewBoxList = viewBoxList()
		self.viewBoxList.setFixedWidth(280)
		vbox             = QVBoxLayout()
		vbox.setContentsMargins(0,0,0,0)
		vbox.addWidget(self.viewBoxList)
		return vbox

	def setupControl(self):
		self.lcontrol = lineControlWidget()
		self.vcontrol = viewBoxControlWidget()
		vbox          = QVBoxLayout()
		vbox.addWidget(self.vcontrol)
		vbox.addWidget(self.lcontrol)
		self.vcontrol.hide()
		return vbox		

	def setupSubmitUI(self):
		self.applyPB  = QPushButton('Apply Changes')
		self.applyPB.setFixedWidth(125)
		self.canclePB = QPushButton('Cancle')
		self.canclePB.setFixedWidth(125)
		hbox          = QHBoxLayout()
		hbox.addStretch()
		hbox.addWidget(self.applyPB)
		hbox.addWidget(self.canclePB)
		return hbox

	def addView(self, viewBox = None):
		viewBoxListWidget = self.viewBoxList.addView(viewBox)
		return viewBoxListWidget

	def addPlot(self, viewBoxNum = 0, line = None):
		viewBox, vListWidget = self.viewBoxList.viewBoxDict[viewBoxNum]
		vlineListWidget      = self.viewBoxList.addLine(viewBoxNum, line)
		values               = vlineListWidget.getLineValues()
		print values
		vlineListWidget.doubleClicked.connect(lambda val = values : self.lcontrol.setPanelVal(val))
		return vlineListWidget

	# def importPlotItem(self, line = None):
	# 	vlineListWidget = self.plotTab.addPlotItem(line)
	# 	values     = ItemWidget.getLineValues()
	# 	ItemWidget.doubleClicked.connect(lambda val = values :self.plotTab.setPanelVal(val))
	# 	return ItemWidget

	def importPlotItems(self,viewBoxDict = None, lineDict = None):
		ItemWidgets = []
		# try:
		# self.plotTab.plotListWidget.clear()
		for index in viewBoxDict:
			# plot, legend, viewBox = viewBoxDict[index]
			# ItemWidget = self.addView(lineDict[index])
			ItemWidget = self.addView()
		for index in lineDict:
			line       = lineDict[index]
			viewboxNum = line.line_viewNum()
			ItemWidget = self.addPlot(viewboxNum, line)
			ItemWidgets.append(ItemWidget)
		return ItemWidgets


	# def importPlotItems(self, lineDict = None):
	# 	ItemWidgets = []
	# 	# try:
	# 	self.plotTab.plotListWidget.clear()
	# 	for index in lineDict:
	# 		ItemWidget = self.importPlotItem(lineDict[index])
	# 		ItemWidgets.append(ItemWidget)
	# 	return ItemWidgets


def Debugger():
	app  = QApplication(sys.argv)
	form = EditorWindow()
	form.show()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)
	app.exec_()
Debugger()