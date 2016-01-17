import sys
import types
from   PySide.QtGui       import *
from   PySide.QtCore      import *
from   QLineNumber        import *
from   viewLineList       import *
from   MaterialDesignList.MColorPickerMKII import MColorPicker
from   MaterialDesignList.MUtilities       import *



class scroll(QScrollArea):
	def __init__(self, parent=None):
		super(scroll, self).__init__(parent)
		payload = viewBoxControlWidget()
		self.setFixedWidth(430)
		self.setContentsMargins(0,0,0,0)
		self.setWidget(payload)

class viewBoxControlWidget (QWidget):
	def __init__(self, parent=None):
		super(viewBoxControlWidget , self).__init__(parent)

		box0 = self.setupGraphUI()
		box1 = self.setupGridUI()
		box2 = self.setupAxisUI()
		boxZ = MVBoxLayout()
		boxZ.addWidgets(box0, MHLine(), box1, MHLine(), box2, 0)
		self.setLayout(boxZ)
		self.activeVlineListWidget = None


	def setupGraphUI(self):

		self.titleVisi = QCheckBox('Title Text:')
		self.titleLine = QLineEdit()
		self.titleEdit = QPushButton('...')

		self.titleVisi.setFixedWidth(85)
		self.titleEdit.setFixedWidth(25)
		hbox0            = MHBoxLayout(self.titleVisi, self.titleLine, self.titleEdit )

		vbox1            = MVBoxLayout()
		bdcLabel         = QLabel('Border Color')
		bdmLabel         = QLabel('Border Margins')
		bgcLabel         = QLabel('Background')

		self.bgColorLine   = MColorPicker()
		self.bdColorLine   = MColorPicker()
		self.bdMarginCombo = QComboBox()

		h1 = MHBoxLayout( bdcLabel, bgcLabel, bdmLabel   ).setFixedWidth(120).setAlignment(Qt.AlignHCenter)
		h2 = MHBoxLayout( self.bdColorLine, self.bgColorLine, self.bdMarginCombo   ).setFixedWidth(120)
		vbox1.addLayouts(h1, h2)

		hbox2           = MHBoxLayout()
		resLable        = QLabel('Graph Size( W x H ):')
		xLable          = QLabel('x')

		self.Gwidth     = QSpinBox()
		self.GHeight    = QSpinBox()
		self.Gwidth.setAlignment(Qt.AlignCenter)
		self.GHeight.setAlignment(Qt.AlignCenter)
		xLable.setFixedWidth(6)
		resLable .setFixedWidth(120)
		hbox2.addWidgets(resLable, self.Gwidth, xLable, self.GHeight)

		vbox = MVBoxLayout(hbox0, MHLine(), vbox1, MHLine(), hbox2, 25 )
		groupBox = MGroupBox('Graph Options:')
		groupBox.addLayout(vbox)
		box = QVBoxLayout()
		box.addWidget(groupBox)
		return box


	def setupGridUI(self):

		self.showMajorGrid = QCheckBox("Show Major Grid")
		self.showMinorGrid = QCheckBox("Show Minor Grid")
		h0 =  MHBoxLayout( 0, self.showMajorGrid, 25, self.showMinorGrid ).setFixedWidth(120)

		
		GCLabel           = QLabel("Grid Color:")
		self.majorGCLine  = MColorPicker()
		self.minorGCLine  = MColorPicker()
		self.majorGCLine.setFixedWidth(120)
		self.minorGCLine.setFixedWidth(120)		
		h1 = MHBoxLayout(  GCLabel, 0, self.majorGCLine, 30, self.minorGCLine)


		GWLabel           = QLabel("Line Style:")
		self.majorGWSpin  = QSpinBox()
		self.minorGWSpin  = QSpinBox()

		self.majorGSCombo = QComboBox()
		self.minorGSCombo = QComboBox()	

		self.majorGWSpin.setFixedWidth(40)
		self.minorGWSpin.setFixedWidth(40)

		self.majorGSCombo.setFixedWidth(80)
		self.minorGSCombo.setFixedWidth(80)	

		h2 = MHBoxLayout(  GWLabel, 0, self.majorGWSpin, self.majorGSCombo, 35, self.minorGWSpin, self.minorGSCombo)

		h2.setSpacing(0)


	


		v0   = MVBoxLayout(h0, MHLine(), h1, MHLine(), h2, 25)
		group = MGroupBox('Grid Options:')
		group.addLayout(v0)
		box = QHBoxLayout()
		box.addWidget(group)

		return box


	def setupAxisUI(self):
		groupBox     = MGroupBox('Axis Options:')
		self.axisTab = MAxisTabWidget()
		groupBox.addWidget(self.axisTab)
		box = MVBoxLayout(groupBox)

		return box





	def setPanelVal(self, name  = None, color  = None, width   = None,
						  style = None, symbol = None, visible = None, viewNum = None):
		if name is not None:
			self.nameLine.setText(name)
		if color:
			self.lColorLine.setText(str(color))
		if width is not None:
			self.lWidthLine.setText(str(width))
		# if style:			
		# 	self.lStyleLine.set
		if symbol:
			self.symbol     = symbol
			self.symbol_val = symbol.symbol_val()
			self.oColorLine.setText(self.symbol_val['outLine']['color'])
			self.oWidthLine.setText(str(self.symbol_val['outLine']['width']))
			self.outlineVisi.setChecked(self.symbol_val['outLine']['visible'])
			self.sColorLine.setText(self.symbol_val['color'])
			self.sSizeLine.setText(str(self.symbol_val['size']))
			self.symbolVisi.setChecked(self.symbol_val['visible'])

		if visible:
			self.lineVisi.setChecked(True)
		else:
			self.lineVisi.setChecked(False)
		return self.getPanelVal()


	def getPanelVal(self):
		self.outLine_val = {'color'   : self.oColorLine.text(),
							'width'   : float(self.oWidthLine.text()),	
							'visible' : self.outlineVisi.isChecked()}	

		self.symbol_val  = {'color'   : self.sColorLine.text(),
							'size'    : float(self.sSizeLine.text()),
							'outLine' : self.outLine_val,
							'visible' : self.symbolVisi.isChecked()}						
		
		self.symbol.symbol_val(**self.symbol_val)
		self.val         = {'name'    : self.nameLine.text(),
							'color'   : self.lColorLine.text(),
							'width'   : float(self.lWidthLine.text()),
							'style'   : None,
							'symbol'  : self.symbol, 
							'visible' : self.lineVisi.isChecked(), 
							'viewNum' : None}
		return self.val





class MAxisTabWidget(QTabWidget):
	def __init__(self, parent = None):
		super(MAxisTabWidget, self).__init__(parent)
		self.addAxis()
		self.addAxis()
		self.addAxis()
		self.addAxis()

	def addAxis(self):
		self.addTab(MAxisTab(), 'x axis')

class MAxisTab(QWidget):
	def __init__(self, parent = None):
		super(MAxisTab, self).__init__(parent)	
		gbox1 = self.setupAxisTextUI()

		boxz  = MVBoxLayout(gbox1, MHLine(), 0)
		self.setLayout(boxz)

	def setupAxisTextUI(self):
		titleLabel     = QLabel('Axis Title:')
		self.axisTitle = QLineEdit()
		self.setBold   = QCheckBox('B')
		self.setItalic = QCheckBox('I')

		styleLabel     = QLabel('Size/Font:')
		colorLabel     = QLabel('title color:')
		self.textSize  = QSpinBox()
		self.textFont  = QComboBox()
		self.textColor = MColorPicker()
		titleLabel.setFixedWidth(90)
		styleLabel.setFixedWidth(90)
		colorLabel.setFixedWidth(85)
		self.textSize.setFixedWidth(40)
		self.textFont.setFixedWidth(80)
		self.setBold.setFixedWidth(35)
		self.setItalic.setFixedWidth(35)
		self.textColor.setFixedWidth(120)
		h0 = MHBoxLayout(titleLabel, self.axisTitle)
		h1 = MHBoxLayout(styleLabel, self.textSize, self.textFont, 0, self.setBold, 15, self.setItalic, 0)
		h2 = MHBoxLayout(colorLabel, self.textColor,0 )
		h0.setSpacing(0)
		h1.setSpacing(0)
		v1 = MVBoxLayout(h0, MHLine(), h1, MHLine(), h2,  0)
		textGroupBox = MGroupBox('Axis Text:').addLayout(v1)
		return textGroupBox
		



def run():
	app        = QApplication(sys.argv)
	MainWindow = viewBoxControlWidget()
	MainWindow = scroll()
	MainWindow.show()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)
	app.exec_()
	
run()		