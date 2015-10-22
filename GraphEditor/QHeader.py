import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class QHeader(QWidget):
	def __init__(self):
		super(QHeader, self).__init__()
		self.show()
		self.lineMode = True #otherwise will be ViewBox Header
		self.lineRbColor = '#FF4848'
		self.viewRbColor = '#545454'

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
		self.lineMode = False

		#header:
		painter.setPen(  QColor('#E7E8EB'))
		painter.setBrush(QColor('#E7E8EB'))
		painter.drawRoundedRect(0, 5, w, h, 8, 8, mode = Qt.AbsoluteSize)
		
		if self.lineMode:
			RbColor = self.lineRbColor
		else: 
			RbColor = self.viewRbColor

			#L button:
			painter.setBrush(QColor ('#74D43C'))
			painter.setPen(  QColor ('#74D43C'))
			painter.drawRoundedRect((w - 55), (h / 2 - 3), 14, 14, 8, 8, mode = Qt.AbsoluteSize)			
		
		#R button:			
		painter.setBrush(QColor (RbColor))
		painter.setPen(  QColor (RbColor))
		painter.drawRoundedRect((w - 23), (h / 2 - 3), 14, 14, 8, 8, mode = Qt.AbsoluteSize)



		#title:
		font = QFont("Helvetica", 11, QFont.Bold)
		painter.setFont(font)
		painter.setPen(  QColor('#5B6170'))
		painter.drawText(QRectF((w / 2 - 20), (h / 2 - 7), 50, 50), Qt.AlignLeft, 'Text')
		


		


def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = QHeader()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()