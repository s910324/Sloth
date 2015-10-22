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
		vlineListWidget.doubleClicked.connect(lambda widget = vlineListWidget : self.handleFocus(widget))
		return  vlineListWidget

	def handleFocus(self, widget):
		for index in range(self.count()):
			self.itemWidget(self.item(index)).header.setDcFocus(False)
		widget.setDcFocus(True)	

class viewLineListWidget(QWidget):
	doubleClicked = Signal(object)
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
		self.header = QHeader()
		self.header.setFixedHeight(30)
		vbox0 = QVBoxLayout()
		vbox0.setContentsMargins(0,0,0,0)
		vbox0.addWidget(self.header )
		self.setLayout(vbox0)



	def returnVal(self):
		return [ self.typLabel.text(), self.nameLineE.text(), self.time ]


	def mouseDoubleClickEvent(self, event):
		self.header.setFocus()
		self.doubleClicked.emit(self.header)
		event.accept()

