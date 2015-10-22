import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class viewBoxListWidget(QWidget):
	def __init__(self, lineMode = True, parent = None):
		super(viewBoxListWidget, self).__init__(parent)

		self.setFocusPolicy(Qt.StrongFocus)
		self.show()

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
		

		#header:
		painter.setPen(QColor(0,0,0,0))
		painter.setBrush(QColor('#354052'))
		painter.drawRect(0, 0, w, h)

		painter.setPen(QColor(0,0,0,0))

		painter.setBrush(QColor('#DDDDDD'))
		painter.drawRect(3, 2, 3, h-4)



		#title:
		font = QFont("Helvetica", 11, QFont.Bold)
		painter.setFont(font)
		painter.setPen(QColor('#5B6170'))
		painter.drawText(QRectF((25), (h / 2 - 6), 50, 50), Qt.AlignLeft, 'Text')

		#state
		painter.setPen(QColor(0,0,0,0))
		painter.setBrush(QColor('#161F2E'))
		painter.setBrush(Qt.Dense3Pattern)
		painter.drawRect(w-35, 2, 35, h)

		font = QFont("Helvetica", 11, QFont.Bold)
		painter.setFont(font)
		painter.setPen(QColor('#5B6170'))
		painter.drawText(QRectF((w-22), (h / 2 - 8), 50, 50), Qt.AlignLeft, '+')

	def setDcFocus(self, focused = True):
		if focused:
			self.header_Color = self.focused_Color

		else:
			self.header_Color = self.unFocused_Color

		self.update()


def run():
	app = QApplication(sys.argv)
	MainWindow = viewBoxListWidget()
	MainWindow.show()
	app.exec_()


run()

