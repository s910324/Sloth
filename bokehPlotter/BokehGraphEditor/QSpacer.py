import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class QSpacer(QWidget):
	def __init__(self,  parent = None):
		super(QSpacer, self).__init__(parent)
		self.show()
		self.unFocused_Color = '#363636'
		self.focused_Color   = '#858585'
		self.body_Color      = '#363636'

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

		painter.setPen(  QColor( self.body_Color ))
		painter.setBrush(QColor( self.body_Color ))
		painter.drawRoundedRect(0, 0, w, h, 0, 0, mode = Qt.AbsoluteSize)


	def setDcFocus(self, focused = True):
		if focused:
			self.body_Color = self.focused_Color

		else:
			self.body_Color = self.unFocused_Color
		self.update()
