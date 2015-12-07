import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class QHeader(QWidget):
	def __init__(self, lineMode = True, parent = None):
		super(QHeader, self).__init__(parent)
		self.lineMode        = lineMode  #otherwise will be ViewBox Header
		self.unFocused_Color = '#6C6D6D'
		self.focused_Color   = '#E7E8EB'
		self.header_Color    = '#6C6D6D'

		self.lineRbColor = '#FF4848'
		self.viewRbColor = '#545454'
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
		painter.setPen(  QColor( self.header_Color ))
		painter.setBrush(QColor( self.header_Color ))
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
		



	def setDcFocus(self, focused = True):
		if focused:
			self.header_Color = self.focused_Color

		else:
			self.header_Color = self.unFocused_Color

		self.update()
