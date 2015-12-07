import sys
from   PySide.QtGui  import *
from   PySide.QtCore import *
from   QLineNumber   import *

class lineControlWidget (QWidget):
	def __init__(self, parent=None):
		super(lineControlWidget , self).__init__(parent)
		box0 = self.setupLineUI()
		box1 = self.setupSymbolUI()
		boxZ = QVBoxLayout()
		boxZ.addLayout(box0)
		boxZ.addLayout(box1)
		self.setLayout(boxZ)


	def setupLineUI(self):

		nameLable      = QLabel('Line Name:')
		nameLable.setFixedWidth(100)
		self.nameLine  = QLineEdit()
		self.lineVisi  = QCheckBox('show')
		hbox0          = QHBoxLayout()
		hbox0.addWidget(nameLable)
		hbox0.addWidget(self.nameLine)
		hbox0.addWidget(self.lineVisi)

		pos1Label0 = QLabel('Position1 (X, Y):     [')
		pos1Label0.setFixedWidth(100)
		pos1Label1 = QLabel(', ')
		pos1Label2 = QLabel(']')

		pos2Label0 = QLabel('Position2 (X, Y):     [')
		pos2Label0.setFixedWidth(100)
		pos2Label1 = QLabel(', ')
		pos2Label2 = QLabel(']')

		self.pos1x = QLineNumber()
		self.pos1y = QLineNumber()
		self.pos2x = QLineNumber()
		self.pos2y = QLineNumber()

		hbox1      = QHBoxLayout()
		hbox1.addWidget(pos1Label0)
		hbox1.addWidget(self.pos1x)
		hbox1.addWidget(pos1Label1)
		hbox1.addWidget(self.pos1y)
		hbox1.addWidget(pos1Label2)

		hbox2      = QHBoxLayout()
		hbox2.addWidget(pos2Label0)
		hbox2.addWidget(self.pos2x)
		hbox2.addWidget(pos2Label1)
		hbox2.addWidget(self.pos2y)
		hbox2.addWidget(pos2Label2)		

		hbox3           = QHBoxLayout()
		vboxA           = QVBoxLayout()
		lCLable         = QLabel('Line Color')
		lCLable.setAlignment(Qt.AlignHCenter)
		self.lColorLine = QLineEdit()
		self.lColorLine.setFixedWidth(120)
		vboxA.addWidget(lCLable)
		vboxA.addWidget(self.lColorLine)

		vboxB           = QVBoxLayout()
		lWLable         = QLabel('Line Width')
		lWLable.setAlignment(Qt.AlignHCenter)
		self.lWidthLine = QLineEdit()
		self.lWidthLine.setFixedWidth(120)
		vboxB.addWidget(lWLable)
		vboxB.addWidget(self.lWidthLine)	

		vboxC = QVBoxLayout()
		lSLable         = QLabel('Line Style')
		lSLable.setAlignment(Qt.AlignHCenter)
		self.lStyleLine = QComboBox()
		self.lStyleLine.setFixedWidth(120)
		vboxC.addWidget(lSLable)
		vboxC.addWidget(self.lStyleLine)

		hbox3.addLayout(vboxA)
		hbox3.addLayout(vboxB)
		hbox3.addLayout(vboxC)

		vbox           = QVBoxLayout()
		vbox.addLayout(hbox0)
		vbox.addLayout(self.HLine())

		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addLayout(self.HLine())

		vbox.addLayout(hbox3)
		vbox.addLayout(self.HLine())
		vbox.addSpacing(25)
		groupBox = QGroupBox('Line Options:')
		groupBox.setLayout(vbox)
		box = QVBoxLayout()
		box.addWidget(groupBox)
		return box


	def setupSymbolUI(self):
		hbox0           = QHBoxLayout()
		self.symbolVisi = QCheckBox('show Symbol')

		vboxA           = QVBoxLayout()
		sCLable         = QLabel('Symbol Color')
		sCLable.setAlignment(Qt.AlignHCenter)
		self.sColorLine = QLineEdit()
		self.sColorLine.setFixedWidth(120)
		vboxA.addWidget(sCLable)
		vboxA.addWidget(self.sColorLine)

		vboxB           = QVBoxLayout()
		sZLable         = QLabel('Symbol Size')
		sZLable.setAlignment(Qt.AlignHCenter)
		self.sSizeLine  = QLineEdit()
		self.sSizeLine.setFixedWidth(120)
		vboxB.addWidget(sZLable)
		vboxB.addWidget(self.sSizeLine)	

		vboxC           = QVBoxLayout()
		sSLable         = QLabel('Symbol Style')
		sSLable.setAlignment(Qt.AlignHCenter)
		self.sStyleLine = QComboBox()
		self.sStyleLine.setFixedWidth(120)
		vboxC.addWidget(sSLable)
		vboxC.addWidget(self.sStyleLine)
		
		hbox0.addLayout(vboxA)
		hbox0.addLayout(vboxB)
		hbox0.addLayout(vboxC)	




		hbox1             = QHBoxLayout()
		self.outlineVisi  = QCheckBox('show Symbol Outline')

		vboxM           = QVBoxLayout()
		oCLable         = QLabel('Outline Color')
		oCLable.setAlignment(Qt.AlignHCenter)
		self.oColorLine = QLineEdit()
		self.oColorLine.setFixedWidth(120)
		vboxM.addWidget(oCLable)
		vboxM.addWidget(self.oColorLine)

		vboxN           = QVBoxLayout()
		oWLable         = QLabel('Outline Width')
		oWLable.setAlignment(Qt.AlignHCenter)
		self.oWidthLine  = QLineEdit()
		self.oWidthLine.setFixedWidth(120)
		vboxN.addWidget(oWLable)
		vboxN.addWidget(self.oWidthLine)	

		vboxO           = QVBoxLayout()
		oSLable         = QLabel('Outline Style')
		oSLable.setAlignment(Qt.AlignHCenter)
		self.oStyleLine = QComboBox()
		self.oStyleLine.setFixedWidth(120)
		vboxO.addWidget(oSLable)
		vboxO.addWidget(self.oStyleLine)


		hbox1.addLayout(vboxM)
		hbox1.addLayout(vboxN)
		hbox1.addLayout(vboxO)	

		groupBox = QGroupBox('Symbol Options:')
		vboxZ    = QVBoxLayout()
		vboxZ.addSpacing(10)
		vboxZ.addWidget(self.symbolVisi)
		vboxZ.addSpacing(10)
		vboxZ.addLayout(hbox0)
		vboxZ.addLayout(self.HLine())
		vboxZ.addWidget(self.outlineVisi)
		vboxZ.addSpacing(10)
		vboxZ.addLayout(hbox1)
		vboxZ.addLayout(self.HLine())
		vboxZ.addStretch()
		groupBox.setLayout(vboxZ)
		box      = QVBoxLayout()
		box.addWidget(groupBox)
		return box

	def setPanelVal(self, val):
		print val
		name, color, width, style, symbol, visible, viewNum = val
		self.nameLine.setText(name)
		if visible:
			self.lineVisi.setChecked(True)
		else:
			self.lineVisi.setChecked(False)
		self.lColorLine.setText(str(color))
		self.lWidthLine.setText(str(width))





	def HLine(self):
		vbox  = QVBoxLayout()
		hline = QFrame()
		hline.setFrameStyle( QFrame.HLine  |  QFrame.Plain )
		hline.setFrameShadow( QFrame.Sunken )
		hline.setLineWidth(1)
		vbox.addSpacing(15)
		vbox.addWidget(hline)
		vbox.addSpacing(15)
		# toto.setStyleSheet('border: 1px solid #303030; background-color: #303030;')
		return vbox

	def VLine(self):
		toto = QFrame()
		toto.setFrameStyle(QFrame.VLine  |  QFrame.Plain)
		toto.setLineWidth(1)
		toto.setFrameShadow(QFrame.Sunken)
		# toto.setStyleSheet('border: 1px solid #303030; background-color: #303030;')
		return toto		



def run():
	app        = QApplication(sys.argv)
	MainWindow = lineControlWidget()


	app.exec_()
# run()		