import sys
from PySide import QtGui
from   PySide.QtGui  import *
from   PySide.QtCore import *


class graphSelector(QWidget):
	checkedChange = Signal(int, int)
	def __init__(self, parent=None):
		super(graphSelector, self).__init__(parent)
		self.resize(450, 650)
		self.vbox0        = QVBoxLayout()
		box1              = self.setUpGroupBox()
		box2              = self.setUpLineOptionUI()
		box3              = self.setUpApplyUI()
		self.vbox0.addLayout(box1)
		self.vbox0.addLayout(box2)
		self.vbox0.addLayout(box3)
		self.checkBoxList = []
		self.setLayout(self.vbox0)

	def setUpGroupBox(self):
		self.groupBox     = QGroupBox("Exclusive Radio Buttons")
		self.checkLayout  = QVBoxLayout()
		vbox              = QVBoxLayout()
		self.groupBox.setLayout(self.checkLayout)
		vbox.addWidget(self.groupBox)
		return vbox
		

	def setUpApplyUI(self):
		hbox              = QHBoxLayout()
		self.applyPB      = QPushButton('Apply')
		self.canclePB     = QPushButton('Cancle')
		hbox.addWidget(self.applyPB)
		hbox.addWidget(self.canclePB)
		return hbox

	def setUpLineOptionUI(self):
		vbox0    = QVBoxLayout()
		hbox1    = QHBoxLayout()
		hbox2    = QHBoxLayout()
		self.p1x = QLineEdit()
		self.p1y = QLineEdit()
		self.p2x = QLineEdit()
		self.p2y = QLineEdit()
		valid    = QtGui.QDoubleValidator()
		self.p1x.setValidator(valid)
		self.p1y.setValidator(valid)
		self.p2x.setValidator(valid)
		self.p2y.setValidator(valid)
		hbox1.addWidget(QLabel('point 1 [x, y] =  [   '))
		hbox1.addWidget(self.p1x)
		hbox1.addWidget(QLabel(', '))
		hbox1.addWidget(self.p1y)
		hbox1.addWidget(QLabel(']'))

		hbox2.addWidget(QLabel('point 2 [x, y] =  [   '))
		hbox2.addWidget(self.p2x)
		hbox2.addWidget(QLabel(', '))
		hbox2.addWidget(self.p2y)
		hbox2.addWidget(QLabel(']'))
		
		vbox0.addLayout(hbox1)
		vbox0.addLayout(hbox2)
		vbox0.addStretch()
		return vbox0
	def addPlotHolder(self, viewBox, ticket):
		checkBox = QCheckBox('viewBox {0}'.format(ticket), self)
		checkBox.box_number = ticket

		checkBox.stateChanged.connect(lambda  stat = checkBox.checkState(), view = viewBox : self.setCheck(view, stat))
		self.checkLayout.addWidget(checkBox)
		self.checkLayout.addSpacing(5)
		self.checkBoxList.append(checkBox)

	def addPlotHolders(self, plotDic):
		for ticket in plotDic:
			plot, legend, viewBox = plotDic[ticket]
			self.addPlotHolder(viewBox, ticket)
		self.checkLayout.addStretch()


	def setCheck(self, viewBox, stat):
		viewBox.setSelect(stat)
		return stat




def run():
	app = QApplication(sys.argv)
	MainWindow = graphSelector()
	MainWindow.show()
	app.exec_()
# run()
