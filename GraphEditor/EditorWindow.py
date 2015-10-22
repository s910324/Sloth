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
		hbox1.addLayout(box1)
		hbox1.addLayout(vbox1)
		vbox1.addLayout(box2)
		vbox1.addLayout(box3)
		self.setLayout(hbox1)

	def setupList(self):
		self.viewBoxList = viewBoxList()
		self.viewBoxList.addView()
		self.viewBoxList.addView()
		self.viewBoxList.setFixedWidth(300)
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



def run():
	app        = QApplication(sys.argv)
	MainWindow = EditorWindow()
	MainWindow.show()
	app.exec_()
run()
