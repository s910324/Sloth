# import sys

# from PySide         import QtGui
# from PySide.QtGui   import *
# from PySide.QtCore  import *

# class MMultiWidget(QWidget):
# 	def __init__(self,  labable    = True,       labeltxt  = None,     labelW   = 62, labelH  = 22, 
# 						labelcolor = "#F0F0F0",  bgcolor   = "#1c1c1c", 
# 						checkble   = False,      checkStat = False, 
# 						writable   = False ,      writetxt  = None,      wirteW  = 100,  wirteH  = 22):	
# 		super(MMultiWidget, self).__init__()
# 		m =  self.palette().color(QPalette.Background)
# 		# bgcolor = QColor(m.red()*0.6, m.green()*0.6, m.blue()*0.6)
# 		# labelcolor = "#050505"
# 		self.labelW = labelW
# 		self.labelH = labelH
# 		self.wirteW = wirteW
# 		self.wirteH = wirteH
# 		checkbleFix = ([writable, labable] == [0, 0])
# 		self.w      = labelW*labable+ wirteW*writable+ 2 + checkbleFix *15
# 		self.h      = (max([labable, checkbleFix, checkble])*max([wirteH, labelH])) +2
# 		self.setFixedWidth(self.w)
# 		self.setFixedHeight(self.h)

# 		self.labeltext    = labeltxt
# 		fontDatabase      = QFontDatabase()
# 		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")
# 		self.labelcolor   = labelcolor
# 		self.bgcolor      = bgcolor
# 		self.bdcolor      = bgcolor
# 		self.Hoverbdcolor = bgcolor

# 		#checkRELEATD
# 		self.alignment    = Qt.AlignCenter
# 		self.checkStat    = checkStat
# 		if checkble:
# 			self.enableCheck()
# 		self.checkEnabled = checkble
# 		self.checkBGcolor = '#f0f0f0'

# 		#writeRELEATED
# 		self.wirteW       = wirteW
# 		self.wirteH       = wirteH
# 		self.writable     = writable
# 		self.writetxt     = writetxt 

# 		if self.writable:
# 			self.enableHoverEffect()
# 			self.LineEdit = QLineEdit()
# 			self.LineEdit.setStyleSheet('QLineEdit{border-style: hidden;}')
# 			self.LineEdit.setFixedHeight(self.h-6)
# 			self.LineEdit.setFixedWidth(self.wirteW - 8)
# 			self.LineEdit.setFont(QFont('disposabledroidBB', 10))
# 			self.LineEdit.textChanged.connect(lambda txt : self.__setattr__('writetxt', txt))
# 			Hbox = QHBoxLayout()
# 			Hbox.addStretch()
# 			Hbox.addWidget(self.LineEdit)
# 			Hbox.addSpacing(3)

# 			Hbox.setContentsMargins(2,0,0,0)
# 			self.setContentsMargins(0,0,0,0)
# 			self.setLayout(Hbox)


# 	def paintEvent(self, event):
# 		self.painter = QPainter()
# 		self.painter.begin(self)
# 		self.paint(self.painter)
# 		self.painter.end()


# 	def paint(self, painter):
# 		painter.setRenderHint(QPainter.Antialiasing)
# 		self.drawBase(painter)
# 		self.drawLabel(painter)
# 		self.drawCheckWidget(painter)

# 	def drawBase(self, painter):
# 		size = self.size()
# 		h    = size.height()
# 		w    = size.width()
# 		pen            = QPen()
# 		brush          = QBrush(QColor(self.bgcolor))
# 		brush.setStyle(Qt.Dense5Pattern)
# 		pen.setWidth(1)
# 		pen.setColor(self.bdcolor)
# 		painter.setBrush(brush)
# 		painter.setPen(pen)
# 		if not self.writable:
# 			drawRect  = QRect(1, 1, size.width()-2, size.height()-2)
# 			painter.drawRect(drawRect)
# 		else:
# 			p       = 4
# 			points  =  [QPoint(1,1), 
# 					    QPoint(1 + self.labelW - p,1),    QPoint(1 + self.labelW, 1 + p), QPoint(1 + self.labelW + p,1),
# 						QPoint(w - 2, 1), 
# 						QPoint(w - 2, h-2),
# 						QPoint(1 + self.labelW + p, h-2), QPoint(1 + self.labelW, h-2 -p),   QPoint(1 + self.labelW - p, h-2),
# 						QPoint(1,h-2)]

# 			Polygon = QPolygon(points)
# 			painter.setPen(pen)
# 			painter.drawPolygon(Polygon, fillRule=Qt.WindingFill)

# 	def drawLabel(self, painter):
# 		offset    = 14 * self.checkEnabled
# 		textRect  = QRect(1 + offset, 1, self.labelW-2-offset, self.labelH-2)
# 		pen       = QPen()
# 		pen.setColor(self.labelcolor)
# 		painter.setPen(pen)
# 		painter.setFont(QFont('disposabledroidBB', 10))
# 		painter.drawText(textRect, Qt.AlignCenter, self.labeltext) 

# 	def drawCheckWidget(self, painter):
# 		if self.checkEnabled:
# 			pen   = QPen()
# 			brush = QBrush(QColor("#f0f0f0"))
# 			pen.setWidth(0)
# 			pen.setColor(self.bgcolor)
			
# 			brush.setStyle(Qt.SolidPattern)
# 			painter.setBrush(brush)
# 			painter.setPen(pen)
# 			painter.drawRect(QRect(3,5,10,10))

# 			if not self.checkStat:
# 				pen.setWidth(0)
# 				pen.setColor("#f0f0f0")
# 				brush      = QBrush(QColor(self.checkBGcolor))
# 				brush.setStyle(Qt.Dense2Pattern)
# 				painter.setBrush(brush)
# 				painter.setPen(pen)
# 				painter.drawRect(QRectF(4.5,6.5,7,7))
# 			else:
# 				pen.setColor(QColor('#FF0066'))
# 				pen.setJoinStyle(Qt.RoundJoin)
# 				pen.setWidth(2)
# 				points  = [QPoint(6,8), QPoint(8,13), QPoint(14,4)]
# 				Polygon = QPolygon(points)
# 				painter.setPen(pen)
# 				painter.drawPolyline(Polygon)



# 	def enableCheck(self):
# 		self.checkEnabled = True
# 		self.enableHoverEffect()

# 	def enableHoverEffect(self):
# 		self.Hoverbdcolor = '#FF0066'


# 	def mousePressEvent(self, event):
# 		if event.button() == Qt.LeftButton and self.checkEnabled :
# 			if QRect(1,1,self.labelW, self.labelH).contains(event.pos()):
# 				self.checkStat = not self.checkStat
# 				self.update()

# 	def enterEvent(self,event):
# 		self.bdcolor      = self.Hoverbdcolor
# 		self.checkBGcolor = '#ff0066'
# 		self.update()

# 	def leaveEvent(self,event):
# 		self.bdcolor      = self.bgcolor
# 		self.checkBGcolor = '#f0f0f0'
# 		self.update()

# def run():
# 	app = QApplication(sys.argv)
# 	MainWindow = MMultiWidget(labelW = 92, labeltxt = "test func")
# 	MainWindow.show()
# 	app.exec_()
# 	import os
# 	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
# 	print "File Path: " + os.path.realpath(__file__)

# run()	

import sys
from PySide.QtGui   import *
from PySide.QtCore  import *

class MMultiWidget(QWidget):
	def __init__(self, bdcolor = QColor(26,122,194,250)):	
		super(MMultiWidget , self).__init__()
		self.setFixedHeight(28)
		self.setMinimumWidth(28)
		self.mainH = HBoxLayout()
		self.setLayout(self.mainH)
		self.setContentsMargins(0,0,0,0)
	
		self.bgcolor = "#1c1c1c"
		self.bdcolor = bdcolor



	def paintEvent(self, event):
		self.painter = QPainter()
		self.painter.begin(self)
		self.paint(self.painter)
		self.painter.end()


	def paint(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		self.drawBase(painter)

	def drawBase(self, painter):
		pen            = QPen()
		brush          = QBrush(QColor(0,0,0, 120))
		brush.setStyle(Qt.SolidPattern)
		pen.setWidth(1.5)
		pen.setColor(QColor(self.bdcolor))
		painter.setBrush(brush)
		painter.setPen(pen)

		painter.drawPolygon(self.mainH.getwidgetPoints(), fillRule=Qt.WindingFill)
		for i in self.mainH.widgetList:
			i.paint(painter)

	def addHead(self):                self.mainH.addHead()
	def addSep(self):                 self.mainH.addSep()
	def addBase(self,   *args, **kw): self.mainH.addBase(*args, **kw)
	def addLabel(self,  *args, **kw): self.mainH.addLabel(*args, **kw)
	def addCheck(self,  *args, **kw): self.mainH.addCheck(*args, **kw)
	def addButton(self, *args, **kw): self.mainH.addButton(*args, **kw)
	def addLine(self,   *args, **kw): self.mainH.addLine(*args, **kw)
	def addTail(self):                self.mainH.addTail()


class HBoxLayout(QHBoxLayout):
	def __init__(self):	
		super(HBoxLayout, self).__init__()
		self.setSpacing(0)
		self.setContentsMargins(0,0,0,0)
		self.widgetList = []

	def addHead(self):
		head = headWidget()
		self.addWidget(head)
		self.widgetList.append(head)
		return head

	def addSep(self):
		sep = sepWidget()
		self.addWidget(sep)
		self.widgetList.append(sep)
		return sep

	def addBase(self,  *args, **kw):
		base = baseWidget(*args, **kw)
		self.addWidget(base)
		self.widgetList.append(base)	
		return base

	def addLabel(self, *args, **kw):
		label = labelWidget(*args, **kw)
		self.addWidget(label)
		self.widgetList.append(label)			
		return label

	def addCheck(self, *args, **kw):
		check = checkWidget(*args, **kw)
		self.addWidget(check)
		self.widgetList.append(check)
		return check

	def addButton(self, *args, **kw):
		button = buttonWidget(*args, **kw)
		self.addWidget(button)
		self.widgetList.append(button)
		return button
	

	def addLine(self, *args, **kw):
		line = lineWidget(*args, **kw)
		self.addWidget(line)
		self.widgetList.append(line)
		return line


	def addTail(self):
		tail = tailWidget()
		self.addWidget(tail)
		self.widgetList.append(tail)
		return tail

	def getwidgetPoints(self):
		up, down   = [], []
		widgetList = self.widgetList
		for upWidget, downWidget in zip(widgetList, widgetList[::-1]):
			upWidget.poly()
			downWidget.poly()	
			up   += upWidget.up
			down += downWidget.down
		return QPolygon(up+down)


	


class baseWidget(QWidget):
	def __init__(self, w = None):	
		super(baseWidget, self).__init__()
		self.poly()
		self.setMinimumHeight(15)
		self.setMinimumWidth(1)
		if w:
			self.setFixedWidth(w)

	def poly(self):
		s, p = self.size(), self.pos()
		x, y = p.x()+2, p.y()+2
		h, w = s.height()-4,  s.width()-4
		self.up   = [ QPoint(x, y),     QPoint(x+w, y) ]
		self.down = [ QPoint(x+w, y+h),  QPoint(x, y+h) ]
		self.rect = QRect(x,y,w,h)

	def paint(self, painter):
		pass

class labelWidget(baseWidget):
	def __init__(self, text = "label", color = '#FFFFFF', w = None, fontSize = 12, alignment = Qt.AlignCenter):
		super(labelWidget, self ).__init__()
		self.labelColor = color
		self.labeltext  = text
		self.fontSize   = fontSize
		self.alignment  = alignment
		if w:
			self.setFixedWidth(w)
		fontDatabase    = QFontDatabase()
		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")


	def paint(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		pen = QPen()
		pen.setColor(self.labelColor)
		painter.setPen(pen)
		painter.setFont(QFont('disposabledroidBB', self.fontSize))
		self.poly()
		painter.drawText(self.rect, self.alignment, self.labeltext) 
		
class lineWidget(baseWidget):
	def __init__(self, w = None):
		super( lineWidget, self ).__init__()
		fontDatabase = QFontDatabase()
		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")
		self.line = QLineEdit()
		self.line.setFont(QFont('disposabledroidBB',12))
		self.line.setStyleSheet('QLineEdit{border-style: hidden; background-color: rgba(0,0,8,50);}')
		self.line.setFixedHeight(self.size().height()*0.05)
		h = QHBoxLayout()
		h.setSpacing(0)
		h.setContentsMargins(0,0,0,0)
		h.addWidget(self.line)
		self.setLayout(h)
		if w:
			self.setFixedWidth(w)
		fontDatabase    = QFontDatabase()
		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")
	def paint(self, painter):
		pass

class checkWidget(baseWidget):
	def __init__(self, stat = False, color = '#FF0066', w = 40):
		super(checkWidget, self ).__init__()
		self.checkColor = color
		self.checkStat  = stat
		fontDatabase    = QFontDatabase()
		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")
		if w:
			self.setFixedWidth(w)

	def paint(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		pen = QPen()
		self.poly()

		[txt, color] = ["  v  ", QColor(22,180,248)]if self.checkStat else ["  x  ", QColor(231,0,156)]
		painter.setFont(QFont('disposabledroidBB', 12))
		pen.setColor("#FFF")
		painter.setPen(pen)
		painter.drawText(self.rect, Qt.AlignCenter, '[   ]') 

		pen.setColor(color)
		painter.setPen(pen)
		painter.drawText(self.rect, Qt.AlignCenter, txt)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton :

			self.checkStat = not self.checkStat
			self.update()

class buttonWidget(labelWidget):
	def __init__(self, text = "label", color = '#FFFFFF', w = None, fontSize = 10, alignment = Qt.AlignCenter):
		super(buttonWidget, self ).__init__()

		self.labelColor = color
		self.labeltext  = text
		self.fontSize   = fontSize
		self.alignment  = alignment
		self.pressedColor = QColor(26,122,194,250)
		self.pressed = False
		self.hovered = False
		if w:
			self.setFixedWidth(w)

		fontDatabase    = QFontDatabase()
		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")


	def paint(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		pen = QPen()
		pen.setColor(QColor(self.labelColor))
		painter.setPen(pen)
		painter.setFont(QFont('disposabledroidBB', self.fontSize))
		self.poly()
		painter.drawText(self.rect, self.alignment, "[%s]" % self.labeltext) 

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton :
			self.labelColor, self.pressedColor = self.pressedColor, self.labelColor
			self.pressed = True
			self.update()	

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton :
			self.labelColor, self.pressedColor = self.pressedColor, self.labelColor
			self.pressed = False
			self.update()	

	def enterEvent(self, event):
		event.accept()
		self.hovered = True
		self.labelColor, self.pressedColor = self.pressedColor, self.labelColor
		self.update()	

	def leaveEvent(self, event):
		event.accept()
		self.hovered = False
		self.labelColor, self.pressedColor = self.pressedColor, self.labelColor
		self.update()	

class sepWidget(QWidget):
	def __init__(self):	
		super(sepWidget, self).__init__()
		self.poly()
		self.setMinimumHeight(15)
		self.setFixedWidth(10)
	def poly(self):
		s, p = self.size(), self.pos()
		x, y = p.x()+2, p.y()+2
		h, w = s.height()-4,  s.width()-4
		self.up   = [ QPoint(x, y),     QPoint(x+w/2, y+4), QPoint(x+w, y) ]
		self.down = [ QPoint(x+w, y+h),   QPoint(x+w/2, y+h-4), QPoint(x, y+h)]
	def paint(self, painter):
		pass			


class headWidget(QWidget):
	def __init__(self):	
		super(headWidget, self).__init__()
		self.poly()
		self.setMinimumHeight(15)
		self.setFixedWidth(8)
	def poly(self):
		s, p = self.size(), self.pos()
		x, y = p.x()+2, p.y()+2
		h, w = s.height()-4,  s.width()-4
		self.up   = [ QPoint(x, y+4),     QPoint(x+w, y+1)]
		self.down = [ QPoint(x+w, y+h),   QPoint(x, y+h-4)]	
	def paint(self, painter):
		pass		


class tailWidget(QWidget):
	def __init__(self):	
		super(tailWidget, self).__init__()
		self.poly()
		self.setMinimumHeight(15)
		self.setFixedWidth(8)
	def poly(self):
		s, p = self.size(), self.pos()
		x, y = p.x(), p.y()+2
		h, w = s.height()-4,  s.width()-4
		self.up   = [ QPoint(x, y+1),     QPoint(x+w, y+4)]
		self.down = [ QPoint(x+w, y+h-4), QPoint(x, y+h)]
	
	def paint(self, painter):
		pass		




def run():
	app = QApplication(sys.argv)
	MainWindow = MMultiWidget()
	MainWindow.show()
	app.exec_()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)

# run()	

