import sys
from PySide import QtGui
from   PySide.QtGui  import *
from   PySide.QtCore import *
import  graphSelectorListEditor as gListEditor

class graphSelector(QWidget):
	checkedChange  = Signal(int, int)
	requestPreview = Signal(int, list)
	def __init__(self, parent=None):
		super(graphSelector, self).__init__(parent)
		self.resize(350, 650)
		self.vbox0        = QVBoxLayout()
		box1              = self.setUpGroupBox()
		box2              = self.setUpLineOptionUI()
		box3              = self.setUpLineEditor()
		box4              = self.setUpApplyUI()

		self.vbox0.addLayout(box1)
		self.vbox0.addLayout(box2)
		self.vbox0.addLayout(box3)
		self.vbox0.addLayout(box4)
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
		self.applyPB      = QPushButton('Apply Changes')
		self.canclePB     = QPushButton('Cancle')
		# self.applyPB.setStyleSheet( 'border: 2px solid #008800; height: 20px;')
		# self.canclePB.setStyleSheet('border: 2px solid #880000; height: 20px;')		
		self.applyPB.clicked.connect(self.preview)
		self.canclePB.clicked.connect(self.cancleOperation)
		hbox.addWidget(self.applyPB)
		hbox.addWidget(self.canclePB)
		
		return hbox

	def setUpLineOptionUI(self):
		layout    = QVBoxLayout()
		vbox0     = QVBoxLayout()
		hbox1     = QHBoxLayout()
		hbox2     = QHBoxLayout()
		groupBox  = QGroupBox("Point Coordinate:")
		groupBox1 = QGroupBox("Point1:")
		groupBox2 = QGroupBox("Point2:")

		self.p1x = QLineNumEdit()
		self.p1y = QLineNumEdit()
		self.p2x = QLineNumEdit()
		self.p2y = QLineNumEdit()
		self.previewPB = QPushButton('Add to Praph')


		hbox1.addWidget(QLabel('['))
		hbox1.addWidget(self.p1x)
		hbox1.addWidget(QLabel(', '))
		hbox1.addWidget(self.p1y)
		hbox1.addWidget(QLabel(']'))
		groupBox1.setLayout(hbox1)

		hbox2.addWidget(QLabel('['))
		hbox2.addWidget(self.p2x)
		hbox2.addWidget(QLabel(', '))
		hbox2.addWidget(self.p2y)
		hbox2.addWidget(QLabel(']'))
		groupBox2.setLayout(hbox2)

		vbox0.addWidget(groupBox1)
		vbox0.addSpacing(10)
		vbox0.addWidget(groupBox2)
		vbox0.addWidget(self.previewPB)
		self.previewPB.clicked.connect(self.preview)
		# vbox0.addStretch()
		groupBox.setLayout(vbox0)
		layout.addWidget(groupBox)
		return layout

	def setUpLineEditor(self):
		vbox0 = QVBoxLayout()
		vbox1 = QVBoxLayout()
		groupBox        = QGroupBox("Lines:")
		self.lineEditor = gListEditor.graphListEditor()
		vbox0.addWidget(groupBox)
		vbox1.addWidget(self.lineEditor)
		groupBox.setLayout(vbox1)
		return vbox0


	def cancleOperation(self):
		for widget in self.checkBoxList:
			widget.setChecked(False)
		self.close()

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

	def valueCheck(self):
		data = [self.p1x.checkValue(), self.p1y.checkValue(), self.p2x.checkValue(), self.p2y.checkValue()]
		if None not in data:
			print 'data = ' + str(data)
			return data
		return False

	def preview(self):
		data = self.valueCheck()
		activeBox = []
		print data
		if data:
			for checkBox in self.checkBoxList:
				if checkBox.isChecked():
					viewBox_number = checkBox.box_number
					print data
					self.requestPreview.emit(viewBox_number, data)
					activeBox.append(viewBox_number)
			return activeBox, data
		else:
			return False


class QLineNumEdit(QLineEdit):
	def __init__(self, parent=None):
		super(QLineNumEdit, self).__init__(parent)
		valid    = QtGui.QDoubleValidator()
		self.setValidator(valid)
		self.textChanged.connect(self.checkValue)

	def checkValue(self):
		try:
			value = float(self.text())
			self.setStyleSheet("border: 1px solid None;")
			return value
		except ValueError:
			self.setStyleSheet("border: 1px solid red;")
			return None

	
def run():
	app = QApplication(sys.argv)
	MainWindow = graphSelector()
	MainWindow.show()
	app.exec_()
run()
