import sys
from   PySide        import QtGui
from   PySide.QtGui  import *
from   PySide.QtCore import *
from   QHeader       import *

class viewLineList(QListWidget):
	def __init__(self, parent=None):
		super(viewLineList, self).__init__(parent)
		self.lineCount = 0

		self.setMaximumHeight(80)
		self.addLine()
		self.addLine()


	def addLine(self):
		self.lineCount += 1
		self.setMaximumHeight(80 * self.lineCount)
		
		vlineListWidgetItem = QListWidgetItem()
		vlineListWidget     = viewLineListWidget()
		vlineListWidgetItem.setSizeHint(vlineListWidget.sizeHint())

		self.addItem(vlineListWidgetItem)
		self.setItemWidget(vlineListWidgetItem, vlineListWidget)
		return  vlineListWidget



class viewLineListWidget(QWidget):
	def __init__(self, parent = None):
		super(viewLineListWidget, self).__init__(parent)
		self.setDesign()

	def setDesign(self):
		# style              = 'QPushButton{background-color: #808080; border-radius: 8px; color: #212121; }'
		# hbox0              = QHBoxLayout()
		# self.viewNameLable = QLabel('View box : n')
		# self.viewNameLable.setFixedWidth(50)


		
		# self.deleteButton = QPushButton('x')
		# self.deleteButton.setStyleSheet(style)
		# self.deleteButton.setFixedSize(16,16)
		

		# hbox0.addWidget(self.viewNameLable)
		# hbox0.addStretch()
		# hbox0.addWidget(self.deleteButton)

		# vbox0              = QVBoxLayout()
		# vbox0.setContentsMargins(10,10,10,2)
		# vbox0.addLayout(hbox0)
		# vbox0.addLayout(self.HLine(3))
		a = QHeader()
		a.setFixedHeight(30)
		vbox0 = QVBoxLayout()
		vbox0.addWidget(a)
		self.setLayout(vbox0)



	def returnVal(self):
		return [ self.typLabel.text(), self.nameLineE.text(), self.time ]


	def mouseDoubleClickEvent(self, event):
		self.doubleClicked.emit()
		event.accept()


	def HLine(self, width = 1):
		vbox  = QVBoxLayout()
		hline = QFrame()
		hline.setFrameStyle( QFrame.HLine  |  QFrame.Plain )
		hline.setFrameShadow( QFrame.Sunken )
		hline.setLineWidth(width)
		vbox.addSpacing(5)
		vbox.addWidget(hline)
		vbox.setContentsMargins(0,0,0,0)
		vbox.addSpacing(5)
		# toto.setStyleSheet('border: 1px solid #303030; background-color: #303030;')
		return vbox

	def VLine(self):
		toto = QFrame()
		toto.setFrameStyle(QFrame.VLine  |  QFrame.Plain)
		toto.setLineWidth(1)
		toto.setFrameShadow(QFrame.Sunken)
		# toto.setStyleSheet('border: 1px solid #303030; background-color: #303030;')
		return toto		

# def run():
# 	app = QApplication(sys.argv)
# 	# MainWindow = listItem()
# 	MainWindow = viewBoxList()
# 	MainWindow.addView()
# 	MainWindow.addView()
# 	MainWindow.show()


# 	app.exec_()

# run()