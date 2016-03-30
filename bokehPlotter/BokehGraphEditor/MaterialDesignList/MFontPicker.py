import sys
import types
from   PySide.QtGui       import *
from   PySide.QtCore      import *
from   MUtilities       import *


class MFontPicker (QWidget):
	def __init__(self, parent=None):
		super(MFontPicker, self).__init__(parent)
		self.setContentsMargins(0,0,0,0)
		label0 = QLabel('Font')
		label1 = QLabel('Size')
		label2 = QLabel('Style')
		label0.setAlignment(Qt.AlignCenter)
		label1.setAlignment(Qt.AlignCenter)
		label2.setAlignment(Qt.AlignCenter)


		self.FontIndc = QPushButton('Helvetica')
		self.SizeIndc = QPushButton('10')
		self.FontItal = QCheckBox('B')
		self.FontBold = QCheckBox('I')
		self.SizeIndc.setFixedWidth(70)
		self.FontItal.setFixedWidth(40)
		self.FontBold.setFixedWidth(40)
		self.SizeIndc.clicked.connect(self.showFontDialog)
		self.FontIndc.clicked.connect(self.showFontDialog)

		h0 	   = MHBoxLayout(MHLine(), label0, MHLine()).setFixedHeight(10)
		h1 	   = MHBoxLayout(MHLine(), label1, MHLine()).setFixedHeight(10)
		h2     = MHBoxLayout(MHLine(), label2, MHLine()).setFixedHeight(10)
		hStyle = MHBoxLayout(self.FontBold, self.FontItal)

		v0     = MVBoxLayout(h0, self.FontIndc)
		v1     = MVBoxLayout(h1, self.SizeIndc)
		v2     = MVBoxLayout(h2, hStyle)
		v0.setSpacing(0)
		v1.setSpacing(0)
		v2.setSpacing(0)

		hb = MHBoxLayout(v0, v1, v2)
		hb.setContentsMargins(2,2,2,2)
		self.setLayout(hb)


	def showFontDialog(self):
		self.enablePanel(False)
		self.FDialog = QFontDialog()
		font         = self.FontIndc.text()
		size         = int(self.SizeIndc.text())
		(font, ok)   = self.FDialog.getFont(QFont("Helvetica [Cronyx]", 10))
		if ok : self.setPanelFont(font)
		self.enablePanel(True)


	def enablePanel(self, enable = True):
		self.FontIndc.setEnabled(enable)
		self.SizeIndc.setEnabled(enable)
		self.FontBold.setEnabled(enable)
		self.FontItal.setEnabled(enable)

	def getDialogValue(self):
		self.enablePanel(True)
		self.FontIndc.setText()
		self.SizeIndc.setText()
		# self.FontBold.
		# self.FontItal.

	def setPanelFont(self, f):
		fontName = f.family()
		fontSize = f.pointSize()
		self.FontIndc.setText(fontName)
		self.SizeIndc.setText(str(fontSize))
		print "selected font: %s - %dpt" % (fontName, fontSize)



def Debugger():
	app  = QApplication(sys.argv)
	form = MFontPicker()
	form.show()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)
	app.exec_()
Debugger()