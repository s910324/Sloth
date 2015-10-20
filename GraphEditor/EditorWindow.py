import sys
from   PySide import QtGui
from   PySide.QtGui         import *
from   PySide.QtCore        import *
from   viewBoxListWidget    import *
from   lineControlWidget import *

class EditorWindow(QGroupBox):
	def __init__(self, parent=None):
		super(EditorWindow, self).__init__(parent)
		self.resize(650, 700)
		self.setupLayout()

	def setupLayout(self):
		box1 = self.setupList()
		box2 = self.setupControl()
		box3 = self.setupSubmitUI()
		hbox1 = QHBoxLayout()
		vbox1 = QVBoxLayout()
		hbox1.addLayout(box1)
		hbox1.addLayout(vbox1)
		vbox1.addLayout(box2)
		vbox1.addLayout(box3)
		self.setLayout(hbox1)

	def setupList(self):
		self.viewBoxList = viewBoxListWidget()
		self.viewBoxList.setFixedWidth(200)
		vbox             = QVBoxLayout()
		vbox.addWidget(self.viewBoxList)
		return vbox

	def setupControl(self):
		self.control = lineControlWidget()
		vbox         = QVBoxLayout()
		vbox.addWidget(self.control)
		
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
