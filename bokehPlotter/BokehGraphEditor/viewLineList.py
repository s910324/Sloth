import sys
from   PySide             import QtGui
from   PySide.QtGui       import *
from   PySide.QtCore      import *
from   QHeader            import *
from   MaterialDesignList import MLineListWidget
# sys.path.append('./MaterialDesignList')

# from MLineListWidget import *

class viewLineList(QListWidget):
	itemDcFocused = Signal()
	def __init__(self, parent=None):
		super(viewLineList, self).__init__(parent)
		self.lineCount = -1
		self.setFixedHeight(0)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(  Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)


	def addLine(self, line = None):
		self.lineCount += 1
		self.setFixedHeight( 31 * (self.lineCount + 1))

		vlineListWidgetItem = QListWidgetItem()
		vlineListWidget     = viewLineListWidget(line)
		vlineListWidget.setShadow(self.lineCount == 0)

		vlineListWidgetItem.setSizeHint(vlineListWidget.sizeHint())

		self.addItem(vlineListWidgetItem)
		self.setItemWidget(vlineListWidgetItem, vlineListWidget)
		vlineListWidget.focusChanged.connect(lambda widget = vlineListWidget : self.handleFocus(widget))
		return  vlineListWidget

	def handleFocus(self, widget):
		for index in range(self.count()):
			lineListWidget = self.itemWidget(self.item(index))
			lineListWidget.header.setDcFocus(False)
		self.itemDcFocused.emit()
		widget.setDcFocus(True)	

class viewLineListWidget(QWidget):
	focusChanged  = Signal(object)
	doubleClicked = Signal()
	def __init__(self, line = None, parent = None):
		super(viewLineListWidget, self).__init__(parent)
		self.line   = line

		self.setDesign()

	def setDesign(self):
		vbox0       = QVBoxLayout()
		self.header = MLineListWidget.MLineListWidget()
		self.header.setFixedHeight(30)

		vbox0.setContentsMargins(0,0,0,0)
		vbox0.addWidget(self.header )
		self.setLayout(vbox0)

	def setValue(self, val):
		name, color, width, style, symbol, visible, viewNum = self.getLineVal()
		self.name    = name
		self.color   = color
		self.width   = width
		self.style   = style
		self.symbol  = symbol
		self.visible =  visible
		self.header.setTitle(name)
		self.header.setLineVisible(visible)
		return name, color, width, style, symbol, visible, viewNum


	def setShadow(self, shadow):
		self.shadow = 180 * shadow
		self.header.setShadow(self.shadow)


	def getLineValues(self):
		name, color, width, style, symbol, visible, viewNum = self.line.line_val()
		return name, color, width, style, symbol, visible, viewNum


	def returnVal(self):
		return [ self.typLabel.text(), self.nameLineE.text(), self.time ]


	def mouseDoubleClickEvent(self, event):
		event.accept()
		self.header.setFocus()
		self.doubleClicked.emit()
		self.focusChanged.emit(self.header)

def run():
	app = QApplication(sys.argv)
	MainWindow = viewLineList()
	MainWindow.addLine()
	MainWindow.show()
	app.exec_()


# run()