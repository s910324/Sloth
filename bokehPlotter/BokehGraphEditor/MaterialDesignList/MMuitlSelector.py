import sys
import types        as types
from PySide         import QtGui
from PySide.QtGui   import *
from PySide.QtCore  import *

# class MColorPicker(QWidget):
# 	def __init__(self, color = None, parent = None):
# 		super(MColorPicker, self).__init__(parent)
# 		self.setUI()
# 		self.setContentsMargins(0,0,0,0)
# 		self.setMinimumHeight(55)

# 	def setUI(self):
# 		self.ColorView = MColorView()
# 		self.ColorView.setMinimumHeight(55)
# 		self.ColorView.setMinimumWidth(55)
# 		self.ColorView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
# 		self.ColorView.colorChanged.connect(self.setColor)
# 		self.RLine     = QSpinBox()
# 		self.GLine     = QSpinBox()
# 		self.BLine     = QSpinBox()
# 		self.RLine.setMaximum (255)
# 		self.GLine.setMaximum (255)
# 		self.BLine.setMaximum (255)
# 		self.RLine.setMinimum (0)
# 		self.GLine.setMinimum (0)
# 		self.BLine.setMinimum (0)
# 		self.RLine.setMinimumWidth (80)
# 		self.GLine.setMinimumWidth (80)
# 		self.BLine.setMinimumWidth (80)

# 		self.RLine.valueChanged.connect(self._valueChanged)
# 		self.GLine.valueChanged.connect(self._valueChanged)
# 		self.BLine.valueChanged.connect(self._valueChanged)


# 		hbox  = QHBoxLayout()
# 		hbox.setContentsMargins(0,0,0,0)
# 		vboxV = QVBoxLayout()
# 		vboxR = QVBoxLayout()
# 		vboxG = QVBoxLayout()
# 		vboxB = QVBoxLayout()
# 		vboxV.insertSpacerItem(0, QSpacerItem(0,0,vData = QSizePolicy.MinimumExpanding, hData = QSizePolicy.MinimumExpanding))
# 		vboxR.addStretch()
# 		vboxG.addStretch()
# 		vboxB.addStretch()
# 		vboxV.setContentsMargins(0,0,0,0)
# 		vboxR.setContentsMargins(0,0,0,0)
# 		vboxG.setContentsMargins(0,0,0,0)
# 		vboxB.setContentsMargins(0,0,0,0)

# 		vboxV.addWidget(self.ColorView)
# 		vboxR.addWidget(self.RLine)
# 		vboxG.addWidget(self.GLine)
# 		vboxB.addWidget(self.BLine)
# 		hbox.addLayout(vboxV)
# 		hbox.addLayout(vboxR)
# 		hbox.addLayout(vboxG)
# 		hbox.addLayout(vboxB)
# 		self.setLayout(hbox)

# 	def valueChanged(self):
# 		color = [self.RLine.value(), self.GLine.value(), self.BLine.value()]
# 		# self.changeColor(color)
# 		return color

# 	def _valueChanged(self):
# 		color = [self.RLine.value(), self.GLine.value(), self.BLine.value()]
# 		self.changeColor(color)
# 		return color

# 	def changeColor(self, color = None):
# 		oldSignal = self.ColorView.blockSignals(True)
# 		self.ColorView.changeColor(color)
# 		self.ColorView.blockSignals(oldSignal)

# 		return color

# 	def setColor(self,color = None):
# 		oldSignal = self.ColorView.blockSignals(True)
# 		self.RLine.setValue(color[0])
# 		self.GLine.setValue(color[1])
# 		self.BLine.setValue(color[2])
# 		self.ColorView.blockSignals(oldSignal)
# 		return color

class MColorView(QWidget):
	colorChanged = Signal(list)
	def __init__(self, color = None, parent = None):
		super(MColorView, self).__init__(parent)
		self.painter      = QPainter()
		self.axisColor    = "#000000" 
		self.majorTKColor = "#000000" 
		self.minorTKColor = "#000000" 
		self.initColorView()
		self.initAxisLabel()
		self.initMajorTkLabel()

		box1 = self.initAxisUI()
		self.setLayout(box1)

		self.setFixedHeight(305)
		self.setFixedWidth(425)

	def initAxisUI(self):
		hbox0 = QHBoxLayout()
		vbox0 = QVBoxLayout()
		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox3 = QHBoxLayout()
		self.axisNameLable   = QLineEdit()
		self.axisStyleButton = QPushButton("..")

		self.axisStartCtrl   = QDoubleSpinBox()
		self.axisEndCtrl     = QDoubleSpinBox()
		self.axisWidthCtrl   = QDoubleSpinBox()
		self.axisFormCtrl    = QComboBox()

		self.axisNameLable.setFixedHeight(25)
		self.axisStyleButton.setFixedHeight(25)	
		self.axisStartCtrl .setFixedHeight(25)  
		self.axisEndCtrl.setFixedHeight(25)	
		self.axisWidthCtrl.setFixedHeight(25)	
		self.axisFormCtrl.setFixedHeight(25)	
		self.axisStyleButton.setFixedWidth(25)	
		self.axisWidthCtrl.setFixedWidth(110)
		self.axisStartCtrl.setFixedWidth(110)	
		self.axisEndCtrl.setFixedWidth(110)
		self.axisFormCtrl.setFixedHeight(110)		

		hbox1.addWidget(self.axisNameLable)
		hbox1.addWidget(self.axisStyleButton)

		hbox2.addWidget(self.axisStartCtrl)
		hbox2.addSpacing(100)
		hbox2.addWidget(self.axisEndCtrl)

		
		hbox3.addWidget(self.axisWidthCtrl)
		hbox3.addSpacing(100)
		hbox3.addWidget(QComboBox())

		vbox0.addLayout(hbox1)
		vbox0.addLayout(hbox2)
		vbox0.addLayout(hbox3)
		vbox0.addStretch()

		hbox0.addSpacing(75)
		hbox0.addLayout(vbox0)
		return hbox0




	def initColorView(self):
		x, y, w, h1, h2, h3    = 5,8,15,125,95,95
		self.axisColorView     = objColorView(x, y,           w, h1, color = self.axisColor,    obj = "axis")
		self.MajorTKColorView  = objColorView(x, y+h1-w,      w, h2, color = self.majorTKColor, obj = "majorTK")
		self.MinorTKColorView  = objColorView(x, y+h1+h2-2*w, w, h3, color = self.minorTKColor, obj = "minorTK")
	
	def initAxisLabel(self)	:
		self.axix_name_label   = costomLable(28,  14, 55, 20, "LABEL",    color = "#FF0066")
		self.axix_from_label   = costomLable(28,  44, 55, 20, "START")
		self.axix_to_label     = costomLable(240, 44, 55, 20, "END")
		self.axix_width_label  = costomLable(28,  75, 55, 20, "WIDTH")
		self.axix_format_label = costomLable(240, 75, 55, 20, "STYLE")

	def initMajorTkLabel(self)	:
		self.MajoTk_label      = costomLable(28,  120, 55, 20, "MajorTK", color = "#FF0066")
		self.MinoTk_label      = costomLable(28,  200, 55, 20, "MinorTK", color = "#FF0066")
		# self.axix_from_label   = costomLable(28,  44, 45, 20, "START")
		# self.axix_to_label     = costomLable(250, 44, 45, 20, "END")
		# self.axix_width_label  = costomLable(28,  75, 45, 20, "WIDTH")
		# self.axix_format_label = costomLable(250, 75, 45, 20, "STYLE")

	def paintEvent(self, event):
		self.painter.begin(self)
		self.drawWidget()
		self.painter.end()


	def drawWidget(self):
		painter = self.painter
		self.axisColorView.paint(painter)
		self.MajorTKColorView.paint(painter)
		self.MinorTKColorView.paint(painter)
		self.axix_name_label.paint(painter)
		self.axix_from_label.paint(painter)
		self.axix_to_label.paint(painter)
		self.axix_width_label.paint(painter)
		self.axix_format_label.paint(painter)


		self.MajoTk_label.paint(painter)
		self.MinoTk_label.paint(painter)

		self.update() 


	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
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


class costomLable(object):
	def __init__(self, x, y, w, h, text = None, color = "#F0F0F0", bgcolor = "#1c1c1c"):	
		super(costomLable, self).__init__()
		self.rect    = QRect(x, y, w, h)
		self.text    = text
		fontDatabase = QFontDatabase()
		self.color   = color
		self.bgcolor = bgcolor
		fontDatabase.addApplicationFont("./MFont/disposabledroid-bb.regular.ttf")

	def paint(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)		
		pen        = QPen()
		brush      = QBrush(QColor(self.bgcolor))
		brush.setStyle(Qt.Dense5Pattern)
		pen.setWidth(0)
		pen.setColor(self.bgcolor)
		painter.setBrush(brush)
		painter.setPen(pen)
		painter.drawRect (self.rect)
		pen.setColor(self.color)
		painter.setPen(pen)
		painter.setFont(QFont('disposabledroidBB', 10))
		painter.drawText(self.rect, Qt.AlignCenter, self.text)        


class objColorView(object):
	colorChanged  = Signal(list)
	def __init__(self, x, y, w, h, color = '#000000', obj = None):	
		super(objColorView, self).__init__()
		self.color   = color
		self.rect    = QRect(x, y+w, x+w, y+h-2*w)
		self.switch  = {"axis":self.axisPoints(x,y,w,h), "majorTK":self.majorTKPoints(x,y,w,h), "minorTK":self.minorTKPoints(x,y,w,h)}
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

	def axisPoints(self, x, y, w, h):
		return [QPointF(0+x,0+y),     QPointF(w+x, 0+y),    
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
