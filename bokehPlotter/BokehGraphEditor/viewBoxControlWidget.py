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
		self.setContentsMargins(0,0,0,0)
		box0 = self.setupGraphUI()
		box1 = self.setupGridUI()
		box2 = self.setupAxisUI()
		boxZ = MVBoxLayout()
		boxZ.addWidgets(box0, MHLine(),  box1, MHLine(), box2, 0)
		self.setLayout(boxZ)
		self.activeVlineListWidget = None


	def setupGraphUI(self):

		self.titleVisi = QCheckBox('Title Text:')
		self.titleLine = QLineEdit()
		self.titleEdit = QPushButton('...')

		self.titleVisi.setFixedWidth(85)
		self.titleEdit.setFixedWidth(25)
		hbox0            = MHBoxLayout(self.titleVisi, self.titleLine, self.titleEdit )

		vbox1            = MHBoxLayout()
		bdcLabel         = QLabel('Border Color')
		bdmLabel         = QLabel('Border Margins')
		bgcLabel         = QLabel('Background')

		self.bgColorLine   = MColorPicker()
		self.bdColorLine   = MColorPicker()
		self.bdMarginCombo = QComboBox()

		v1 = MVBoxLayout( bdcLabel, bgcLabel, bdmLabel   ).setFixedWidth(120).setAlignment(Qt.AlignHCenter)
		v2 = MVBoxLayout( self.bdColorLine, self.bgColorLine, self.bdMarginCombo   ).setFixedWidth(120)
		vbox1.addLayouts(v1, v2)

		hbox2           = MHBoxLayout()
		resLable        = QLabel('Graph Size( W x H ):')
		xLable          = QLabel('x')

		self.Gwidth     = QSpinBox()
		self.GHeight    = QSpinBox()
		self.Gwidth.setAlignment(Qt.AlignCenter)
		self.Gwidth.setRange (20, 2048)
		self.GHeight.setAlignment(Qt.AlignCenter)
		self.GHeight.setRange (20, 2048)
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





	def setPanelVal(self,  width      = None, height     = None, tools   = None, 
						   background = None, borderfill = None, viewNum = None,
						   text       = None,  **kwargs):

		if width is not None:
			self.Gwidth.setValue(width)
		if height is not None:
			self.GHeight.setValue(height)
		if background:
			self.bgColorLine.setColor(background)
		if borderfill:
			self.bdColorLine.setColor(borderfill)


		if text is not None:
			self.titleLine.setText(text)
		# if color:
		# 	self.plot.title_text_color      = color
		# if style:
		# 	self.plot.title_text_font_style = style
		# if size is not None:
		# 	self.plot.title_text_font_size  = str(size)+ "pt" * ("pt" not in str(size))



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
		v1 = self.setupAxisTextUI()
		self.setLayout(v1)

	def setupAxisTextUI(self):
		self.axisTitleChk  = QCheckBox('Axis Title:')
		self.axisTitleEdit = QPushButton('...')
		self.axisTitle     = QLineEdit()
		self.axisTitleChk.setFixedWidth(85)
		self.axisTitleEdit.setFixedWidth(25)
		h0 = MHBoxLayout(self.axisTitleChk, self.axisTitle, self.axisTitleEdit)
		h0.setSpacing(0)
		v1 = MVBoxLayout(h0, 0)

		return v1
		



def run():
	app        = QApplication(sys.argv)
	MainWindow = viewBoxControlWidget()
	MainWindow = scroll()
	MainWindow.show()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)
	app.exec_()
	
# run()		