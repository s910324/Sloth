import sys
from   PySide             import QtGui
from   PySide.QtGui       import *
from   PySide.QtCore      import *
from   viewLineList       import *
from   QHeader            import *
from   QLefter            import *
from   QRighter           import *
from   QSpacer            import *
from   MaterialDesignList import MViewBoxListWidget 

# sys.path.append('./MaterialDesignList')

# from MViewBoxListWidget import *


class viewBoxList(QListWidget):

	def __init__(self, parent=None):
		super(viewBoxList, self).__init__(parent)
		self.viewBoxCount = -1
		self.viewBoxDict  = {}		
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(  Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.setStyleSheet( """
                                QListWidget:item:selected:active {
                                     background-color: rgba(0,0,0,0);
                                }
                                QListWidget:item:selected:!active {
                                     background-color: rgba(0,0,0,0);
                                }
                                """)




	def addView(self, viewBox = None):
		self.viewBoxCount += 1

		vListWidgetItem = QListWidgetItem()
		vListWidget     = viewBoxListWidget(viewBox, vListWidgetItem)
		vListWidgetItem.setSizeHint(vListWidget.sizeHint())

		self.addItem(vListWidgetItem)
		self.setItemWidget(vListWidgetItem, vListWidget)
		vListWidget.doubleClicked.connect(lambda widget = vListWidget : self.handleFocus(widget))
		vListWidget.viewLineList.itemDcFocused.connect(lambda widget = vListWidget.viewLineList : self.handleItemFocus(widget))
		self.viewBoxDict[self.viewBoxCount] = viewBox, vListWidget
		return  vListWidget

	def addLine(self, viewBoxNum = None, line = None):
		viewBox, vListWidget = self.viewBoxDict[viewBoxNum]
		vlineListWidget      = vListWidget.addLine(line)
		return vlineListWidget

	def handleFocus(self, widget = None):
		for index in range(self.count()):
			viewBoxWidget = self.itemWidget(self.item(index))
			viewBoxWidget.setDcFocus(False)
		if widget:
			widget.setDcFocus(True)	

	def handleItemFocus(self, item = None):
		#Remove all focuses on item, let item trigger it's focus
		for index in range(self.count()):
			viewBoxWidget = self.itemWidget(self.item(index))
			linelist = viewBoxWidget.viewLineList
			for lineIndex in range(linelist.count()):
				linelistWidget = linelist.itemWidget(linelist.item(lineIndex))
				linelistWidget.header.setDcFocus(False)


	def setLostFocus(self):
		self.handleFocus(None)




class viewBoxListWidget(QWidget):
	doubleClicked = Signal(object)
	def __init__(self, viewBox = None, item = None,  parent = None):
		super(viewBoxListWidget, self).__init__(parent)
		self.item     = item
		self.viewBox  = viewBox
		self.setDesign()

	def setDesign(self):
		self.viewLineList = viewLineList()
		self.header = MViewBoxListWidget.MViewBoxListWidget()
		self.header.setFixedHeight(30)

		vbox0 = QVBoxLayout()
		vbox0.setContentsMargins(0,0,0,0)
		vbox0.setSpacing(0)

		vbox0.addWidget(self.header)
		vbox0.addWidget(self.viewLineList)		
		self.setLayout(vbox0)

	def addLine(self, line = None):
		vlineListWidget = self.viewLineList.addLine(line)
		self.item.setSizeHint(self.sizeHint())
		return  vlineListWidget

	def returnVal(self):
		return [ self.typLabel.text(), self.nameLineE.text(), self.time ]


	def mouseDoubleClickEvent(self, event):
		self.doubleClicked.emit(self)
		event.accept()

	def setDcFocus(self, focus = True):
		self.header.setDcFocus(focus)

	def getViewVal(self):

		combine = self.viewBox.plot_spec().copy()
		combine.update( self.viewBox.plot_title())
		return combine

	def setViewVal(self, val):
		# name, color, width, style, symbol, visible, viewNum 
		return self.viewBox.plot_spec(**val)

def run():
	app = QApplication(sys.argv)
	MainWindow = viewBoxList()
	a = MainWindow.addView()
	MainWindow.addView()
	a.addLine()
	a.addLine()
	MainWindow.show()
	app.exec_()


# run()
