import sys
from   PySide             import QtGui
from   PySide.QtGui       import *
from   PySide.QtCore      import *
from   viewLineList       import *
from   QHeader            import *
from   QLefter            import *
from   QRighter           import *
from   QSpacer            import *

class viewBoxList(QListWidget):

	def __init__(self, parent=None):
		super(viewBoxList, self).__init__(parent)
		self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.setStyleSheet( """
                                QListWidget:item:selected:active {
                                     background-color: rgba(0,0,0,0);
                                }
                                QListWidget:item:selected:!active {
                                     background-color: rgba(0,0,0,0);
                                }
                                """)




	def addView(self):
		vListWidgetItem = QListWidgetItem()
		vListWidget     = viewBoxListWidget()
		vListWidgetItem.setSizeHint(vListWidget.sizeHint())

		self.addItem(vListWidgetItem)
		self.setItemWidget(vListWidgetItem, vListWidget)
		vListWidget.doubleClicked.connect(lambda widget = vListWidget : self.handleFocus(widget))

		return  vListWidget

	def handleFocus(self, widget = None):
		for index in range(self.count()):
			self.itemWidget(self.item(index)).setDcFocus(False)
		if widget:
			widget.setDcFocus(True)	

	def setLostFocus(self):
		self.handleFocus(None)



class viewBoxListWidget(QWidget):
	doubleClicked = Signal(object)
	def __init__(self, parent = None):
		super(viewBoxListWidget, self).__init__(parent)
		self.setDesign()

		# self.setFixedWidth(280)



	def setDesign(self):
		# style              = 'QPushButton{background-color: #808080; border-radius: 8px; color: #212121; }'
		# hbox0              = QHBoxLayout()
		# self.viewNameLable = QLabel('View box : n')
		# self.viewNameLable.setFixedWidth(50)

		# self.addLineButton = QPushButton('+')
		# self.addLineButton.setStyleSheet(style)
		# self.addLineButton.setFixedSize(16,16)
		
		# self.foldingButton = QPushButton('-')
		# self.foldingButton.setStyleSheet(style)
		# self.foldingButton.setFixedSize(16,16)


		# hbox0.addWidget(self.viewNameLable)
		# hbox0.addStretch()
		# hbox0.addWidget(self.addLineButton)
		# hbox0.addSpacing(5)
		# hbox0.addWidget(self.foldingButton)
		# hbox0.addSpacing(10)
		# vbox0 = QVBoxLayout()
		# vbox0.addLayout(hbox0)
		# vbox0.addLayout(self.HLine())


		self.viewLineList = viewLineList()
		# self.viewLineList.setMinimumHeight(5)
		# vbox0.addWidget(self.viewLineList)

		self.header = QHeader(lineMode = False)
		self.header.setFixedHeight(30)

		vbox0 = QVBoxLayout()
		vbox0.setContentsMargins(0,0,0,0)
		vbox0.setSpacing(0)


		vbox1 = QVBoxLayout()
		vbox1.setContentsMargins(0,0,0,0)
		vbox1.setContentsMargins(0,0,0,0)
		vbox1.setSpacing(0)		
		self.space1 = QSpacer()
		self.space2 = QSpacer()
		self.space1.setFixedHeight(8)
		self.space2.setFixedHeight(8)

		vbox1.addWidget(self.space1)
		vbox1.addWidget(self.viewLineList)
		vbox1.addWidget(self.space2)


		hbox0 = QHBoxLayout()
		hbox0.setContentsMargins(0,0,0,0)	
		hbox0.setSpacing(0)
		self.lefter  = QLefter()
		self.righter = QRighter()
		self.lefter.setFixedWidth(15)
		self.righter.setFixedWidth(15)

		hbox0.addWidget(self.lefter)
		hbox0.addLayout(vbox1)
		hbox0.addWidget(self.righter)

		vbox0.addWidget(self.header)
		vbox0.addLayout(hbox0)
		
		self.setLayout(vbox0)



	def returnVal(self):
		return [ self.typLabel.text(), self.nameLineE.text(), self.time ]


	def mouseDoubleClickEvent(self, event):
		self.doubleClicked.emit(self)
		event.accept()

	def setDcFocus(self, focus = True):
		self.header.setDcFocus(focus)
		self.lefter.setDcFocus(focus)
		self.righter.setDcFocus(focus)
		self.space1.setDcFocus(focus)
		self.space2.setDcFocus(focus)