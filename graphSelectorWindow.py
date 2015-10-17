import sys
from   PySide.QtGui  import *
from   PySide.QtCore import *


class graphSelector(QWidget):
	checkedChange = Signal(int, int)
	def __init__(self, parent=None):
		super(graphSelector, self).__init__(parent)
		self.resize(450, 650)
		self.checkLayout  = QVBoxLayout()
		self.checkBoxList = []
		self.setLayout(self.checkLayout)


	def addPlotHolder(self, viewBox, ticket):
		checkBox = QCheckBox('viewBox {0}'.format(ticket), self)
		checkBox.box_number = ticket

		checkBox.stateChanged.connect(lambda  stat = checkBox.checkState(), view = viewBox : self.setCheck(view, stat))
		self.checkLayout.addWidget(checkBox)
		self.checkBoxList.append(checkBox)

	def addPlotHolders(self, plotDic):
		for ticket in plotDic:
			plot, legend, viewBox = plotDic[ticket]
			self.addPlotHolder(viewBox, ticket)

	def setCheck(self, viewBox, stat):
		viewBox.setSelect(stat)
		return stat

def run():
	app = QApplication(sys.argv)
	MainWindow = graphSelector()
	MainWindow.show()
	app.exec_()
# run()