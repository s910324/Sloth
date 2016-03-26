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

		self.FontIndc = QPushButton('No Font Avaliable')
		self.SizeIndc = QPushButton('N/A')
		self.FontItal = QCheckBox('B')
		self.FontBold = QCheckBox('I')
		self.SizeIndc.setFixedWidth(70)
		self.FontItal.setFixedWidth(40)
		self.FontBold.setFixedWidth(40)
		h0 	   = MHBoxLayout(MHLine(), label0, MHLine())
		h1 	   = MHBoxLayout(MHLine(), label1, MHLine())
		h2     = MHBoxLayout(MHLine(), label2, MHLine())


		hStyle = MHBoxLayout(self.FontBold, self.FontItal)
		hStyle.setContentsMargins(0,0,0,0)

		v0 = MVBoxLayout(h0, self.FontIndc)
		v1 = MVBoxLayout(h1, self.SizeIndc)
		v2 = MVBoxLayout(h2, hStyle)
		v0.setContentsMargins(0,0,0,0)
		v1.setContentsMargins(0,0,0,0)
		v2.setContentsMargins(0,0,0,0)
		hb = MHBoxLayout(v0, v1, v2)
		hb.setContentsMargins(2,2,2,2)
		self.setLayout(hb)



def Debugger():
	app  = QApplication(sys.argv)
	form = MFontPicker()
	form.show()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)
	app.exec_()
Debugger()