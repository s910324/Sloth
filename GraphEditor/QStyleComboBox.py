import sys
from   PySide        import QtGui
from   PySide.QtGui  import *
from   PySide.QtCore import *

class QStyleComboBox(QComboBox):
	def __init__(self, option = None, parent=None):
		super(QStyleComboBox, self).__init__(parent)
		self.addItem()
		a = QListWidget()
		self.setModel(a.model())





class QtStyler(QWidget):
	def __init__(self, style = None, parent=None):
		super(QtStyler, self).__init__(parent)

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		self.drawWidget(painter)
		painter.end()


	def drawWidget(self, painter):
		size = self.size()
		w    = size.width()
		h    = size.height()
		
		pen = QPen()
		pen.setWidth(2)
		pen.setColor('#212121')
		pen.setStyle(Qt.SolidLine)
		painter.setPen(pen)
		painter.drawLine(QPointF(5, h/2), QPointF(w-5, h/2))


def run():
	app = QApplication(sys.argv)
	m = QtStyler()
	m.show()
	app.exec_()


run()		