import sys
from   PySide             import QtGui
from   PySide.QtGui       import *
from   PySide.QtCore      import *
from   viewLineList       import *
from   QHeader            import *
from   QLefter            import *
from   QRighter           import *
from   QSpacer            import *


sys.path.append('./MaterialDesignList')

from MViewBoxListWidget import *

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

		# self.header = QHeader(lineMode = False)
		self.header = MViewBoxListWidget()
		self.header.setFixedHeight(30)

		vbox0 = QVBoxLayout()
		vbox0.setContentsMargins(0,0,0,0)
		vbox0.setSpacing(0)

		vbox0.addWidget(self.header)
		vbox0.addWidget(self.viewLineList)		
		self.setLayout(vbox0)



	def returnVal(self):
		return [ self.typLabel.text(), self.nameLineE.text(), self.time ]


	def mouseDoubleClickEvent(self, event):
		self.doubleClicked.emit(self)
		event.accept()

	def setDcFocus(self, focus = True):
		self.header.setDcFocus(focus)
