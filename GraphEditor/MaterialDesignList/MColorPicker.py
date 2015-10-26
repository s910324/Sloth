import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class MColorPicker(QWidget):
	def __init__(self, color = None, parent = None):
		super(MColorPicker, self).__init__(parent)

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		self.drawWidget(painter)
		painter.end()


	def drawWidget(self, painter):
		painter.drawRect()


class MColorView(QWidget):
	def __init__(self, color = None, parent = None):
		super(MColorView, self).__init__(parent)
		self.resize(32, 50)
	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		self.drawWidget(painter)
		painter.end()


	def drawWidget(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		size = self.size()
		w    = size.width()
		h    = size.height()
		r    = (h if w >= h else w)/2 - 5

		pen = QPen()
		pen.setWidth(6)
		pen.setColor('#19212C')		
		painter.setPen(pen)
		painter.drawEllipse(QPointF(w/2, h/2), r, r)

		pen.setWidth(2)
		pen.setColor('#1B7BFF')
		painter.setPen(pen)
		painter.setBrush(QColor('#323232'))
		painter.drawEllipse(QPointF(w/2, h/2), r, r)


def run():
	app = QApplication(sys.argv)
	MainWindow = MColorView()
	MainWindow.show()
	app.exec_()


run()

