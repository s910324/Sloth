import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class MLineListWidget(QWidget):
	def __init__(self, parent = None):
		super(MLineListWidget, self).__init__(parent)
		self.focus_color = QColor(200, 200, 200)

		self.setFocusPolicy(Qt.StrongFocus)
		self.setDcFocus(False)
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
		painter.setBrush(QColor(167, 167, 167))

		painter.drawRect(0, 0, w, h)

		painter.setPen(QColor(0,0,0,0))

		painter.setBrush(self.focus_color)
		painter.drawRect(3, 2, 3, h-4)



		#title:
		font = QFont("Helvetica", 11, QFont.Bold)
		painter.setFont(font)
		painter.setPen(QColor('#8D95AA'))
		painter.drawText(QRectF((25), (h / 2 - 8), 50, 50), Qt.AlignLeft, 'Text')

		#state
		# painter.setPen(QColor(0,0,0,0))
		# painter.setBrush(QColor('#161F2E'))
		# painter.setBrush(Qt.Dense3Pattern)
		# painter.drawRect(w-35, 2, 35, h)

		# font = QFont("Helvetica", 11, QFont.Normal)
		# painter.setFont(font)
		# painter.setPen(QColor('#7C013E'))
		# painter.drawText(QRectF((w-22), (h / 2 - 8), 50, 50), Qt.AlignLeft, 'x')
		# painter.drawLine(15, h-2, w - 30, h-2)

		painter.drawImage(QRectF(w-24,8,15,15), QImage("./MaterialDesignList/MIcon/menu.svg"))
		

	def setDcFocus(self, focused = True):
		if focused:
			self.focus_color = QColor(200, 200, 200)

		else:
			self.focus_color = QColor(50, 50, 50)

		self.update()


def run():
	app = QApplication(sys.argv)
	MainWindow = MViewBoxListWidget()
	MainWindow.show()
	app.exec_()


# run()

