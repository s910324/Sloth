import sys
import types        as types
from PySide         import QtGui
from PySide.QtGui   import *
from PySide.QtCore  import *

class MColorPicker(QWidget):
	def __init__(self, color = None, parent = None):
		super(MColorPicker, self).__init__(parent)
		self.setUI()
		self.setContentsMargins(0,0,0,0)
		self.setMinimumHeight(55)

	def setUI(self):
		self.ColorView = MColorView()
		self.ColorView.setMinimumHeight(55)
		self.ColorView.setMinimumWidth(55)
		self.ColorView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.ColorView.colorChanged.connect(self.setColor)
		self.RLine     = QSpinBox()
		self.GLine     = QSpinBox()
		self.BLine     = QSpinBox()
		self.RLine.setMaximum (255)
		self.GLine.setMaximum (255)
		self.BLine.setMaximum (255)
		self.RLine.setMinimum (0)
		self.GLine.setMinimum (0)
		self.BLine.setMinimum (0)
		self.RLine.setMinimumWidth (80)
		self.GLine.setMinimumWidth (80)
		self.BLine.setMinimumWidth (80)

		self.RLine.valueChanged.connect(self._valueChanged)
		self.GLine.valueChanged.connect(self._valueChanged)
		self.BLine.valueChanged.connect(self._valueChanged)


		hbox  = QHBoxLayout()
		hbox.setContentsMargins(0,0,0,0)
		vboxV = QVBoxLayout()
		vboxR = QVBoxLayout()
		vboxG = QVBoxLayout()
		vboxB = QVBoxLayout()
		vboxV.insertSpacerItem(0, QSpacerItem(0,0,vData = QSizePolicy.MinimumExpanding, hData = QSizePolicy.MinimumExpanding))
		vboxR.addStretch()
		vboxG.addStretch()
		vboxB.addStretch()
		vboxV.setContentsMargins(0,0,0,0)
		vboxR.setContentsMargins(0,0,0,0)
		vboxG.setContentsMargins(0,0,0,0)
		vboxB.setContentsMargins(0,0,0,0)

		vboxV.addWidget(self.ColorView)
		vboxR.addWidget(self.RLine)
		vboxG.addWidget(self.GLine)
		vboxB.addWidget(self.BLine)
		hbox.addLayout(vboxV)
		hbox.addLayout(vboxR)
		hbox.addLayout(vboxG)
		hbox.addLayout(vboxB)
		self.setLayout(hbox)

	def valueChanged(self):
		color = [self.RLine.value(), self.GLine.value(), self.BLine.value()]
		# self.changeColor(color)
		return color

	def _valueChanged(self):
		color = [self.RLine.value(), self.GLine.value(), self.BLine.value()]
		self.changeColor(color)
		return color

	def changeColor(self, color = None):
		oldSignal = self.ColorView.blockSignals(True)
		self.ColorView.changeColor(color)
		self.ColorView.blockSignals(oldSignal)

		return color

	def setColor(self,color = None):
		oldSignal = self.ColorView.blockSignals(True)
		self.RLine.setValue(color[0])
		self.GLine.setValue(color[1])
		self.BLine.setValue(color[2])
		self.ColorView.blockSignals(oldSignal)
		return color

class MColorView(QWidget):
	colorChanged  = Signal(list)
	def __init__(self, color = None, parent = None):
		super(MColorView, self).__init__(parent)
		self.resize(48, 48)
		if color == None:
			self.choosed_color = '#323232'
		else:
			self.choosed_color = color

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
		r    = float(h if w >= h else w)/2 - 5

		pen = QPen()
		pen.setWidth(6)
		pen.setColor('#2B56A8')		
		painter.setPen(pen)
		painter.drawEllipse(QPointF(w/2, h/2), r, r)

		pen.setWidth(3)
		pen.setColor('#111450')
		painter.setPen(pen)
		painter.setBrush(QColor(self.choosed_color))
		painter.drawEllipse(QPointF(w/2, h/2), r, r)

		self.previewRect = QRectF(w/2 - r, h/2 - r, w/2 + r, h/2 + r)



	def showColorDialog(self):
		self.colour_chooser = QColorDialog()
		self.colour_chooser.blockSignals(True)
		self.colour_chooser.currentColorChanged.connect(self._changeColor)
		self.colour_chooser.blockSignals(False)
		self.colour_chooser.show()

	def _changeColor(self, color):
		
		if type(color) == types.ListType and len(color) == 3:
			print 'a'
			self.choosed_color = QColor(color[0], color[1], color[2])
			colorRGB           = color
		else:
			self.choosed_color = color
			colorRGB           = [color.red(), color.green(), color.blue()]
		self.colorChanged.emit(colorRGB)
		self.update()

		return colorRGB

	def changeColor(self, color):
		if type(color) == types.ListType and len(color) == 3:
			self.choosed_color = QColor(color[0], color[1], color[2])
			colorRGB           = color
		else:
			self.choosed_color = color
			colorRGB           = [color.red(), color.green(), color.blue()]
		[r,g,b] = colorRGB
		print '#'+ '%02x'%r + '%02x'%g + '%02x'%b
		# self.colorChanged.emit(colorRGB)
		self.update()

		return colorRGB
	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			if self.previewRect.contains(int(event.x()), int(event.y())):
				self.showColorDialog()
				
		else:
			event.ignore()



def run():
	app = QApplication(sys.argv)
	MainWindow = MColorPicker()
	MainWindow.show()
	app.exec_()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)

run()

