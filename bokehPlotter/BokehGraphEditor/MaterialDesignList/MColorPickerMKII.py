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
		# self.setMinimumHeight(55)

	def setUI(self):
		self.ColorView = MColorView()
		self.ColorLine = QLineEdit()
		self.ColorLine.setText('#323232')
		self.ColorLine.setAlignment(Qt.AlignCenter)
		self.ColorView.colorChanged.connect(self.setColor)
		self.ColorLine.textChanged.connect(self._valueChanged)

		hbox  = QHBoxLayout()
		hbox.setContentsMargins(0,0,0,0)
		hbox.setSpacing(0)
		hbox.addWidget(self.ColorView)
		hbox.addWidget(self.ColorLine)
		self.setLayout(hbox)

	def valueChanged(self):
		color = self.ColorLine.text()
		# self.changeColor(color)
		return color

	def _valueChanged(self):
		color = self.ColorLine.text()
		self.changeColor(color)
		return color

	def changeColor(self, color = None):
		oldSignal = self.ColorView.blockSignals(True)
		self.ColorView.changeColor(color)
		self.ColorView.blockSignals(oldSignal)
		return color

	def setColor(self,color = None):
		oldSignal = self.ColorView.blockSignals(True)
		self.ColorLine.setText(color)
		self.ColorView.blockSignals(oldSignal)
		return color

class MColorView(QWidget):
	colorChanged  = Signal(str)
	def __init__(self, color = None, parent = None):
		super(MColorView, self).__init__(parent)
		self.setFixedSize(QSize(30,30))

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
		self.setMinimumWidth(self.size().height())
		size = self.size()
		w    = size.width()
		h    = size.height()
		r    = float(h if w >= h else w)/2 - 5

		pen = QPen()
		pen.setWidth(3)
		pen.setColor('#2B56A8')		
		painter.setPen(pen)
		painter.drawEllipse(QPointF(w/2, h/2), r, r)

		pen.setWidthF(2)
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
		if type(color) == types.UnicodeType:
			colorHEX = color
		else: 
			colorHEX = '#' + '%02x'%color.red() + '%02x'%color.green() + '%02x'%color.blue()
	
		colorHEX           = colorHEX.upper()
		self.choosed_color = colorHEX
		self.colorChanged.emit(colorHEX)
		self.update()
		return colorHEX

	def changeColor(self, color):
		if type(color) == types.UnicodeType:
			colorHEX = color
		else: 
			colorHEX = '#' + '%02x'%color.red() + '%02x'%color.green() + '%02x'%color.blue()
	
		colorHEX           = colorHEX.upper()
		self.choosed_color = colorHEX
		self.update()
		return colorHEX

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

# run()

