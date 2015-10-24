import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class MViewBoxListWidget(QWidget):
	def __init__(self, title = 'viewBox', parent = None):
		super(MViewBoxListWidget, self).__init__(parent)
		self.title =  title
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
		a = QBrush(QColor('#354052'), bs = Qt.FDiagPattern)
		painter.setPen(QColor(0,0,0,0))
		painter.setBrush(a)
		painter.drawRect(0, 0, w, h)


		#title:
		font = QFont("Helvetica", 11, QFont.Bold)
		painter.setFont(font)
		painter.setPen(QColor('#8D95AA'))
		painter.drawText(QRectF((35), (h / 2 - 8), 50, 50), Qt.AlignLeft, self.title)


		#add line:
		font = QFont("Helvetica", 11, QFont.Bold)
		painter.setFont(font)
		painter.setPen(QColor('#900321'))
		painter.drawText(QRectF((w-22), (h / 2 - 10), 50, 50), Qt.AlignLeft, '+')

		#Icon:
		painter.drawImage(QRectF(5,8,16,16), QImage("./MaterialDesignList/MIcon/window.svg"))


	def setTitle(self, title):
		self.title = title
		self.update
	def setDcFocus(self, focused = True):
		pass
def run():
	app = QApplication(sys.argv)
	MainWindow = MViewBoxListWidget()
	MainWindow.show()
	app.exec_()


# run()

