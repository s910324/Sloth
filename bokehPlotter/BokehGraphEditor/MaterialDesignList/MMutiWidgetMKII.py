import sys

from PySide         import QtGui
from PySide.QtGui   import *
from PySide.QtCore  import *

class MLabelWidget(QWidget):
	def __init__(self,  labeltxt = None, labelW = 62, labelcolor = "#F0F0F0"):	
		super(MLabelWidget, self).__init__()
		self.genPoints()

	def paintEvent(self, event):
		self.painter = QPainter()
		self.painter.begin(self)
		self.paint(self.painter)
		self.painter.end()


	def paint(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)

		self.drawLabel(painter)



	def genPoints(self):
		s, p = self.size(), self.pos()
		h, w = s.height(),  s.width()
		x, y = p.x(),       p.y()

		self.upperSets = [ QPoint(x, y+5),     QPoint(x+4, y+1),     QPoint(x+w-4, y+1), QPoint(x+w, y+5) ]
		self.lowerSets = [ QPoint(x+w, y+h-5), QPoint(x+w-4, y+h-1), QPoint(x+4, y+h-1), QPoint(x, y+h-5) ]
		return upper, lower


class MMultiWidget(QWidget):
	def __init__(self,  labable    = True,       labeltxt  = None,     labelW   = 62, labelH  = 22, 
						labelcolor = "#F0F0F0",  bgcolor   = "#1c1c1c", 
						checkble   = False,      checkStat = False, 
						writable   = False ,      writetxt  = None,      wirteW  = 100,  wirteH  = 22):	
		super(MMultiWidget, self).__init__()

		self.labelW = labelW
		self.labelH = labelH
		self.wirteW = wirteW
		self.wirteH = wirteH
		checkbleFix = ([writable, labable] == [0, 0])
		self.w      = labelW*labable+ wirteW*writable+ 2 + checkbleFix *15
		self.h      = (max([labable, checkbleFix, checkble])*max([wirteH, labelH])) +2
		self.setFixedWidth(self.w)
		self.setFixedHeight(self.h)

		self.labeltext    = labeltxt
		fontDatabase      = QFontDatabase()
		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")
		self.labelcolor   = labelcolor
		self.bgcolor      = bgcolor
		self.bdcolor      = bgcolor
		self.Hoverbdcolor = bgcolor

		#checkRELEATD
		self.alignment    = Qt.AlignCenter
		self.checkStat    = checkStat
		if checkble:
			self.enableCheck()
		self.checkEnabled = checkble
		self.checkBGcolor = '#f0f0f0'

		#writeRELEATED
		self.wirteW       = wirteW
		self.wirteH       = wirteH
		self.writable     = writable
		self.writetxt     = writetxt 

		if self.writable:
			self.enableHoverEffect()
			self.LineEdit = QLineEdit()
			self.LineEdit.setStyleSheet('QLineEdit{border-style: hidden;}')
			self.LineEdit.setFixedHeight(self.h-6)
			self.LineEdit.setFixedWidth(self.wirteW - 8)
			self.LineEdit.setFont(QFont('disposabledroidBB', 10))
			self.LineEdit.textChanged.connect(lambda txt : self.__setattr__('writetxt', txt))
			Hbox = QHBoxLayout()
			Hbox.addStretch()
			Hbox.addWidget(self.LineEdit)
			Hbox.addSpacing(3)

			Hbox.setContentsMargins(2,0,0,0)
			self.setContentsMargins(0,0,0,0)
			self.setLayout(Hbox)


	def paintEvent(self, event):
		self.painter = QPainter()
		self.painter.begin(self)
		self.paint(self.painter)
		self.painter.end()


	def paint(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		self.drawBase(painter)
		self.drawLabel(painter)
		self.drawCheckWidget(painter)

	def drawBase(self, painter):
		size = self.size()
		h    = size.height()
		w    = size.width()
		pen            = QPen()
		brush          = QBrush(QColor(self.bgcolor))
		brush.setStyle(Qt.Dense5Pattern)
		pen.setWidth(1)
		pen.setColor(self.bdcolor)
		painter.setBrush(brush)
		painter.setPen(pen)
		if not self.writable:
			drawRect  = QRect(1, 1, size.width()-2, size.height()-2)
			painter.drawRect(drawRect)
		else:
			p       = 4
			points  =  [QPoint(1,1), 
					    QPoint(1 + self.labelW - p,1),    QPoint(1 + self.labelW, 1 + p), QPoint(1 + self.labelW + p,1),
						QPoint(w - 2, 1), 
						QPoint(w - 2, h-2),
						QPoint(1 + self.labelW + p, h-2), QPoint(1 + self.labelW, h-2 -p),   QPoint(1 + self.labelW - p, h-2),
						QPoint(1,h-2)]

			Polygon = QPolygon(points)
			painter.setPen(pen)
			painter.drawPolygon(Polygon, fillRule=Qt.WindingFill)

	def drawLabel(self, painter):
		offset    = 14 * self.checkEnabled
		textRect  = QRect(1 + offset, 1, self.labelW-2-offset, self.labelH-2)
		pen       = QPen()
		pen.setColor(self.labelcolor)
		painter.setPen(pen)
		painter.setFont(QFont('disposabledroidBB', 10))
		painter.drawText(textRect, Qt.AlignCenter, self.labeltext) 

	def drawCheckWidget(self, painter):
		if self.checkEnabled:
			pen   = QPen()
			brush = QBrush(QColor("#f0f0f0"))
			pen.setWidth(0)
			pen.setColor(self.bgcolor)
			
			brush.setStyle(Qt.SolidPattern)
			painter.setBrush(brush)
			painter.setPen(pen)
			painter.drawRect(QRect(3,5,10,10))

			if not self.checkStat:
				pen.setWidth(0)
				pen.setColor("#f0f0f0")
				brush      = QBrush(QColor(self.checkBGcolor))
				brush.setStyle(Qt.Dense2Pattern)
				painter.setBrush(brush)
				painter.setPen(pen)
				painter.drawRect(QRectF(4.5,6.5,7,7))
			else:
				pen.setColor(QColor('#FF0066'))
				pen.setJoinStyle(Qt.RoundJoin)
				pen.setWidth(2)
				points  = [QPoint(6,8), QPoint(8,13), QPoint(14,4)]
				Polygon = QPolygon(points)
				painter.setPen(pen)
				painter.drawPolyline(Polygon)



	def enableCheck(self):
		self.checkEnabled = True
		self.enableHoverEffect()

	def enableHoverEffect(self):
		self.Hoverbdcolor = '#FF0066'


	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton and self.checkEnabled :
			if QRect(1,1,self.labelW, self.labelH).contains(event.pos()):
				self.checkStat = not self.checkStat
				self.update()

	def enterEvent(self,event):
		self.bdcolor      = self.Hoverbdcolor
		self.checkBGcolor = '#ff0066'
		self.update()

	def leaveEvent(self,event):
		self.bdcolor      = self.bgcolor
		self.checkBGcolor = '#f0f0f0'
		self.update()

def run():
	app = QApplication(sys.argv)
	MainWindow = MMultiWidget(labelW = 92, labeltxt = "test func")
	MainWindow.show()
	app.exec_()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)

# run()	

