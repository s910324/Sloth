import sys
import types        as types
from PySide         import QtGui
from PySide.QtGui   import *
from PySide.QtCore  import *
from MMutiWidget    import MMultiWidget


class MColorView(QWidget):
	colorChanged = Signal(list)
	def __init__(self, color = None, parent = None):
		super(MColorView, self).__init__(parent)
		self.painter      = QPainter()
		self.axisColor    = "#000000" 
		self.majorTKColor = "#000000" 
		self.minorTKColor = "#000000"
		self.labelColor   = "#000000"
		self.initColorView()

		box0 = QVBoxLayout()
		box1 = self.initAxisTitleUI()
		box2 = self.initAxisLineUI()
		box3 = self.initMajorUI()
		box4 = self.initAxisLineUI()
		box0.addLayout(box1)
		box0.addLayout(box2)
		box0.addLayout(box3)
		box0.addLayout(box4)
		box0.addStretch()
		self.setLayout(box0)

		self.setFixedHeight(490)
		self.setFixedWidth(425)

	def initAxisTitleUI(self):
		hbox0 = QHBoxLayout()
		vbox0 = QVBoxLayout()

		hboxN = QHBoxLayout()
		d = MMultiWidget(bdcolor = '#aaa')

		d.addCheck(w=55)

		d.addSep()
		d.addLabel(text = "LABEL")
		d.addSep()
		d.addLabel(text = " ", w = 55)

		hboxN.addWidget(d)
		
		vbox0.addLayout(hboxN)


		hbox1 = QHBoxLayout()
		self.axisTitleLable   = CLableWidget(text = "TITLE", color = "#FF0066", checkble = True, checkStat = True)
		a = MMultiWidget()
		# a.addCheck()
		# a.addSep()
		a.addLabel(text="text:",w = 55)
		a.addSep()
		a.addLine()
		a.addSep()
		a.addButton(text="edit",w = 55)
		

		self.axisTitleText    = QLineEdit()
		self.axisTitleItalic  = QCheckBox()
		self.axisTitleBold    = QCheckBox()
		self.axisItalicLabel  = CLableWidget(w = 22, text = "I")
		self.axisBoldLabel    = CLableWidget(w = 22, text = "B")
		
		
		hbox1.addWidget(a)
		# hbox1.addWidget(self.axisTitleText)
		# hbox1.addWidget(self.axisItalicLabel )
		# hbox1.addWidget(self.axisTitleItalic)
		# hbox1.addWidget(self.axisBoldLabel)
		# hbox1.addWidget(self.axisTitleBold )
		
		vbox0.addLayout(hbox1)
		vbox0.addSpacing(5)

		hbox2 = QHBoxLayout()
		b = MMultiWidget()
		b.addLabel(text="bold",w = 55)
		b.addCheck()


		c = MMultiWidget()
		c.addLabel(text="italic",w = 55)
		c.addCheck()

		d = MMultiWidget()
		d.addLabel(text="font",w = 55)
		d.addLine(w = 55)
		e = MMultiWidget()
		e.addLabel(text="size",w = 55)
		e.addLine(w = 55)

		self.axisFontLabel    = CLableWidget(text = "FONT")
		self.axisTitleFont    = QComboBox()
		self.axisSizeLabel    = CLableWidget(text = "SIZE")
		self.axisTitleSize    = QComboBox()
		# hbox2.addWidget(self.axisFontLabel)
		# hbox2.addWidget(self.axisTitleFont)
		hbox2.addWidget(b)
		hbox2.addStretch()
		hbox2.addWidget(c)
		hbox2.addStretch()
		hbox2.addWidget(d)
		
	
		# hbox2.addWidget(e)
		# hbox2.addSpacing(35)

		# hbox2.addWidget(self.axisSizeLabel)
		# hbox2.addWidget(self.axisTitleSize)
		vbox0.addLayout(hbox2)
		vbox0.addSpacing(45)

		

		hbox0.addSpacing(15)
		hbox0.addLayout(vbox0)
		return hbox0


	def initAxisLineUI(self):
		hbox0 = QHBoxLayout()
		vbox0 = QVBoxLayout()

		hbox1              = QHBoxLayout()
		axisLable          = CLableWidget(text = "AXIS", color = "#FF0066", checkble = True, checkStat = True)
		
		self.axisFromCtrl  = QDoubleSpinBox()
		self.axisToCtrl    = QDoubleSpinBox()
		hbox1.addWidget(axisLable)


		
		hbox1.addStretch()
		vbox0.addLayout(hbox1)
		vbox0.addSpacing(5)


		hbox2         = QHBoxLayout()
		axisFromLable = CLableWidget(text = "RANGE")
		axisToLable   = CLableWidget(text = "TO")
		self.axisFromCtrl = QDoubleSpinBox()
		self.axisToCtrl   = QDoubleSpinBox()
		hbox2.addWidget(axisFromLable)
		hbox2.addWidget(self.axisFromCtrl)
		hbox2.addSpacing(35)
		hbox2.addWidget(axisToLable)
		hbox2.addWidget(self.axisToCtrl)
		vbox0.addLayout(hbox2)
		vbox0.addSpacing(5)


		hbox3         = QHBoxLayout()
		axisFormLable = CLableWidget(text = "FORMAT")
		axisSizeLable = CLableWidget(text = "SIZE")
		self.axisFormCtrl = QComboBox()
		self.axisSizeCtrl = QComboBox()


		hbox3.addWidget(axisFormLable)
		hbox3.addWidget(self.axisFormCtrl)
		hbox3.addSpacing(35)
		hbox3.addWidget(axisSizeLable)
		hbox3.addWidget(self.axisSizeCtrl)
		vbox0.addLayout(hbox3)
		

		vbox0.addSpacing(10)
		vbox0.addStretch()

		hbox0.addSpacing(15)
		hbox0.addLayout(vbox0)
		return hbox0



	def initMajorUI(self):
		hbox0 = QHBoxLayout()
		vbox0 = QVBoxLayout()

		hbox1         = QHBoxLayout()
		axisLable     = CLableWidget(text = "MajorTK", color = "#FF0066", checkble = True, checkStat = True)
		self.axisVisibe    = QCheckBox()
		self.axisFromCtrl  = QDoubleSpinBox()
		self.axisToCtrl    = QDoubleSpinBox()
		hbox1.addWidget(axisLable)
		hbox1.addWidget(self.axisVisibe)
		hbox1.addStretch()
		vbox0.addLayout(hbox1)
		vbox0.addSpacing(5)


		hbox2         = QHBoxLayout()
		axisFromLable = CLableWidget(text = "TickIn")
		axisToLable   = CLableWidget(text = "TickOut")
		self.axisFromCtrl = QDoubleSpinBox()
		self.axisToCtrl   = QDoubleSpinBox()
		hbox2.addWidget(axisFromLable)
		hbox2.addWidget(self.axisFromCtrl)
		hbox2.addSpacing(35)
		hbox2.addWidget(axisToLable)
		hbox2.addWidget(self.axisToCtrl)
		vbox0.addLayout(hbox2)
		vbox0.addSpacing(5)


		hbox3         = QHBoxLayout()
		axisFormLable = CLableWidget(text = "FORMAT")
		axisSizeLable = CLableWidget(text = "WIDTH")
		self.axisFormCtrl = QComboBox()
		self.axisSizeCtrl = QComboBox()


		hbox3.addWidget(axisFormLable)
		hbox3.addWidget(self.axisFormCtrl)
		hbox3.addSpacing(35)
		hbox3.addWidget(axisSizeLable)
		hbox3.addWidget(self.axisSizeCtrl)
		vbox0.addLayout(hbox3)
		

		vbox0.addSpacing(10)
		vbox0.addStretch()

		hbox0.addSpacing(15)
		hbox0.addLayout(vbox0)
		return hbox0

	def initColorView(self):
		x, y, w, h1, h2        = 5,8,15,130, 130
		self.labelColorView    = objColorView(x, y,                   w, h1, color = self.labelColor,   obj = "label")
		self.axisColorView     = objColorView(x, y + h1           -w, w, h2, color = self.axisColor,    obj = "axis")
		self.MajorTKColorView  = objColorView(x, y + h1 + h2   - 2*w, w, h2, color = self.majorTKColor, obj = "majorTK")
		self.MinorTKColorView  = objColorView(x, y + h1 + h2*2 - 3*w, w, h2, color = self.minorTKColor, obj = "minorTK")


	def paintEvent(self, event):
		self.painter.begin(self)
		self.drawWidget()
		self.painter.end()


	def drawWidget(self):
		painter = self.painter
		self.labelColorView.paint(painter)
		self.axisColorView.paint(painter)
		self.MajorTKColorView.paint(painter)
		self.MinorTKColorView.paint(painter)

		self.update() 


	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			if self.labelColorView.rect.contains(int(event.x()), int(event.y())):
				self.showColorDialog(self.labelColorView)
			if self.axisColorView.rect.contains(int(event.x()), int(event.y())):
				self.showColorDialog(self.axisColorView)
			if self.MajorTKColorView.rect.contains(int(event.x()), int(event.y())):
				self.showColorDialog(self.MajorTKColorView)			
			if self.MinorTKColorView.rect.contains(int(event.x()), int(event.y())):
				self.showColorDialog(self.MinorTKColorView)

	def showColorDialog(self, objColorView):
		self.colour_chooser = QColorDialog()
		self.colour_chooser.currentColorChanged.connect(objColorView.changeColor)
		self.colour_chooser.show()



class CLableWidget(QWidget):
	def __init__(self, w = 62, h = 22, text = None, color = "#F0F0F0", bgcolor = "#1c1c1c", checkble = False, checkStat = False):	
		super(CLableWidget, self).__init__()

		self.text         = text
		fontDatabase      = QFontDatabase()
		self.color        = color
		self.bgcolor      = bgcolor
		self.bdcolor      = bgcolor
		self.Hoverbdcolor = bgcolor

		#checkRELEATD

		self.alignment    = Qt.AlignCenter
		self.checkStat    = checkStat
		self.checkEnabled = checkble
		if checkble:
			self.enableCheck()

		self.checkBGcolor = '#f0f0f0'

		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")

		if w:
			self.setFixedWidth(w)
		if h:
			self.setFixedHeight(h)

	def paintEvent(self, event):
		self.painter = QPainter()
		self.painter.begin(self)
		self.paint(self.painter)
		self.painter.end()


	def paint(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		size           = self.size()
		self.drawRect  = QRect(1, 1, size.width()-2, size.height()-2)
		self.textRect  = QRect(15, 1, size.width()-2-15, size.height()-2) if self.checkEnabled else self.drawRect
				
		pen            = QPen()
		brush          = QBrush(QColor(self.bgcolor))
		brush.setStyle(Qt.Dense5Pattern)
		pen.setWidth(0)
		pen.setColor(self.bdcolor)
		painter.setBrush(brush)
		painter.setPen(pen)
		painter.drawRect(self.drawRect)
		pen.setColor(self.color)
		painter.setPen(pen)
		painter.setFont(QFont('disposabledroidBB', 10))
		painter.drawText(self.textRect, Qt.AlignCenter, self.text) 

		self.drawCheckWidget(painter)

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
		self.Hoverbdcolor = '#FF0066'

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton and self.checkEnabled :
			self.checkStat = not self.checkStat
			print self.checkStat

	def enterEvent(self,event):
		self.bdcolor      = self.Hoverbdcolor
		self.checkBGcolor = '#ff0066'

	def leaveEvent(self,event):
		self.bdcolor      = self.bgcolor
		self.checkBGcolor = '#f0f0f0'

class smallColorView(QWidget):
	colorChanged  = Signal(list)
	def __init__(self, color = '#000000'):	
		super(smallColorView, self).__init__()
		self.color   = color
		self.bdcolor      = '#1c1c1c'
		self.Hoverbdcolor = '#8E0054'
	def paintEvent(self, event):
		self.painter = QPainter()
		self.painter.begin(self)
		self.drawWidget()
		self.painter.end()

	def drawWidget(self):
		painter      = self.painter
		painter.setRenderHint(QPainter.Antialiasing)
		[x, y, w, h] = [1, 2, self.size().width()-6, self.size().height()-4]
		peak         = 8
		hpeak        = peak/2
		spare        = ((h-peak)/2)

		self.points  = [QPointF(x,y),         QPointF(w+x, y),    
						QPointF(w+x,spare+y), QPointF(hpeak +w+x,spare+hpeak+y), QPointF(w+x,spare+peak+y), 
						QPointF(w+x,h+y),     QPointF(+x, h+y)]
				
		pen          = QPen()
		brush        = QBrush(QColor(self.color))
		pen.setWidth(2)
		pen.setColor(self.bdcolor)
		painter.setBrush(brush)
		painter.setPen(pen)
		Polygon = QPolygonF(self.points, fillRule=Qt.WindingFill )
		painter.drawPolygon(Polygon)

	def changeColor(self, color):
		self.color = color

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.showColorDialog()

	def enterEvent(self,event):
		self.bdcolor, self.Hoverbdcolor = self.Hoverbdcolor, self.bdcolor

	def leaveEvent(self,event):
		self.bdcolor, self.Hoverbdcolor = self.Hoverbdcolor, self.bdcolor


	def showColorDialog(self):
		self.colour_chooser = QColorDialog()
		self.colour_chooser.currentColorChanged.connect(self.changeColor)
		self.colour_chooser.show()


class objColorView(object):
	colorChanged  = Signal(list)
	def __init__(self, x, y, w, h, color = '#000000', obj = None):	
		super(objColorView, self).__init__()
		self.color   = color
		self.rect    = QRect(x, y+w, x+w, y+h-2*w)
		self.switch  = {"axis":self.axisPoints(x,y,w,h), "label":self.labelPoints(x,y,w,h), "majorTK":self.majorTKPoints(x,y,w,h), "minorTK":self.minorTKPoints(x,y,w,h)}
		self.points  = self.switch[obj]

	def paint(self, painter = None):
		painter.setRenderHint(QPainter.Antialiasing)		
		pen        = QPen()
		brush      = QBrush(QColor(self.color))
		pen.setWidth(2)
		pen.setColor('#8E0054')
		painter.setBrush(brush)
		painter.setPen(pen)
		Polygon = QPolygonF(self.points, fillRule=Qt.WindingFill )
		painter.drawPolygon(Polygon)

	def changeColor(self, color):
		self.color = color

	def labelPoints(self, x, y, w, h):
		return [QPointF(0+x,0+y),     QPointF(w+x, 0+y),    
				QPointF(w+x,0.6*w+y), QPointF(1.25*w+x,0.9*w+y), QPointF(w+x,1.2*w+y), 
				QPointF(w+x,h-w+y),   QPointF(0+x, h+y)]

	def axisPoints(self, x, y, w, h):
		return [QPointF(0+x,w+y),     QPointF(w+x, 0+y),    
				QPointF(w+x,0.6*w+y), QPointF(1.25*w+x,0.9*w+y), QPointF(w+x,1.2*w+y), 
				QPointF(w+x,h-w+y),   QPointF(0+x, h+y)]


	def majorTKPoints(self, x, y, w, h):
		return [QPointF(0+x,w+y),     QPointF(w+x, 0+y),    
				QPointF(w+x,0.6*w+y), QPointF(1.25*w+x,0.9*w+y), QPointF(w+x,1.2*w+y), 
				QPointF(w+x,h-w+y),   QPointF(0+x, h+y)]

	def minorTKPoints(self, x, y, w, h):
		return [QPointF(0+x,w+y),     QPointF(w+x, 0+y),    
				QPointF(w+x,0.6*w+y), QPointF(1.25*w+x,0.9*w+y), QPointF(w+x,1.2*w+y), 
				QPointF(w+x,h+y),   QPointF(0+x, h+y)]



def run():
	app = QApplication(sys.argv)
	MainWindow = MColorView()
	MainWindow.show()
	app.exec_()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)

run()
