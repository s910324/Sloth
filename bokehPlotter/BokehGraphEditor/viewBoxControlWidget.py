import sys
import types
from   PySide.QtGui       import *
from   PySide.QtCore      import *
from   QLineNumber        import *
from   viewLineList       import *
from   MaterialDesignList.MColorPickerMKII import MColorPicker
from   MaterialDesignList.MUtilities       import *




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
		self.activeViewBoxListWidget = None


	def setupGraphUI(self):
		self.titleVisi     = QCheckBox('Show Title Text')
		self.titleLine     = QLineEdit()
		self.titleBold     = QCheckBox('B')
		self.titleItal     = QCheckBox('I')
		self.titleSize     = QSpinBox()
		self.titleFont     = QComboBox()
		
		h0a = MHBoxLayout(self.titleVisi, 0)
		h0b = MHBoxLayout(self.titleLine)
		h0c = MHBoxLayout(QLabel("Size"), self.titleSize,0, QLabel("Font"), self.titleFont, 0, self.titleBold, self.titleItal)


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

		vbox = MVBoxLayout(h0a, 5, h0b, 5, h0c, MHLine(), vbox1, MHLine(), hbox2, 25 )
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
						   title      = None, **kward):

		if width is not None:
			self.Gwidth.setValue(width)
		if height is not None:
			self.GHeight.setValue(height)
		if background:
			self.bgColorLine.setColor(background)
		if borderfill:
			self.bdColorLine.setColor(borderfill)


		print title

		if title: 
		#title visibility, font and color, need to connect submit val to frontend. [build 71]
			if title['text'] is not None:
				self.titleLine.setText(title['text'])

			if title['size']['value']:
				size = int(title['size']['value'][:-2])
				self.titleSize.setValue(size)

			if title['style'] is not None:
				if 'bold' in title['style']:
					self.titleBold.setChecked(True)
				else:
					self.titleBold.setChecked(False)
				if 'italic' in title['style']:
					self.titleItal.setChecked(True)
				else:
					self.titleItal.setChecked(False)



	def getPanelVal(self):
		width      = self.Gwidth.value()
		height     = self.GHeight.value()
		background = self.bgColorLine.getColor()
		borderfill = self.bdColorLine.getColor()
		text       = self.titleLine.text()

		
		color,style,size  = None, None, None
		title = {'text'       : text       if text       else None,
				 'color'      : color      if color      else None,
				 'style'      : style      if style      else None,
				 'size'       : size       if size       else None}
	
		viewNum, tools = None, None
		spec  = {'width'      : width      if width      else None,
				 'height'     : height     if height     else None,
				 'tools'      : tools      if tools      else None,
				 'background' : background if background else None,
				 'borderfill' : borderfill if borderfill else None,
				 'viewNum'    : viewNum    if viewNum    else None,
				 'title'      : title      if title      else None}

		return spec





class MAxisTabWidget(QTabWidget):
	def __init__(self, parent = None):
		super(MAxisTabWidget, self).__init__(parent)
		self.addAxis()

	def addAxis(self):
		self.addTab(MAxisTab(), 'X Bottom Axis')
		self.addTab(MAxisTab(), 'X Top Axis')
		self.addTab(MAxisTab(), 'Y Bottom Axis')
		self.addTab(MAxisTab(), 'Y Top Axis')

class MAxisTab(QWidget):
	def __init__(self, parent = None):
		super(MAxisTab, self).__init__(parent)	
		v1 = self.setupAxisTextUI()
		self.setLayout(v1)

	def setupAxisTextUI(self):
		self.axisTitleChk  = QCheckBox('Show Axis Title')
		self.axisTitle     = QLineEdit()
		self.axisTitleBold = QCheckBox('B')
		self.axisTitleItal = QCheckBox('I')
		self.axixTitleSize = QSpinBox()
		self.axixTitleFont = QComboBox()
		
		h0a = MHBoxLayout(self.axisTitleChk, 0)
		h0b = MHBoxLayout(self.axisTitle)
		h0c = MHBoxLayout(QLabel("Size"), self.axixTitleSize,0, QLabel("Font"), self.axixTitleFont, 0, self.axisTitleBold, self.axisTitleItal)


		self.axisLineChk   = QCheckBox("Show Axis Line")
		ARLabel            = QLabel("Axis Range:")
		dashLabel          = QLabel(" - ")
		self.axisUPRngLine = QLineNumber()
		self.axisDNRngLine = QLineNumber()
		self.axisUPRngLine.setFixedWidth(80)
		self.axisDNRngLine.setFixedWidth(80)
		h1a = MHBoxLayout( self.axisLineChk, 0)
		h1b = MHBoxLayout(  ARLabel, 0, self.axisUPRngLine, dashLabel, self.axisDNRngLine)


		AWLabel            = QLabel("Axis Style (width/format):")
		self.axisWSpin     = QSpinBox()
		self.axisSCombo    = QComboBox()
		self.axisWSpin.setFixedWidth(40)
		self.axisSCombo.setFixedWidth(80)
		h1c = MHBoxLayout(  AWLabel, 0, self.axisWSpin, self.axisSCombo)


		ACLabel            = QLabel("Axis Color:")
		self.axisCLine     = MColorPicker()
		self.axisCLine.setFixedWidth(120)
		h1d = MHBoxLayout(  ACLabel, 0, self.axisCLine)

		AMajorTkLabel      = QLabel("Major Tick Step:")
		self.AMajorTkLine  = QLineNumber()
		self.AMajorTkAdvPB = QPushButton("...")
		self.AMajorTkLine.setFixedWidth(80)
		self.AMajorTkAdvPB.setFixedWidth(30)
		h1e = MHBoxLayout(  AMajorTkLabel, 0, self.AMajorTkLine, self.AMajorTkAdvPB)

		AMinorTkLabel      = QLabel("Minor Tick Step:")
		self.AMinorTkLine  = QLineNumber()
		self.AMinorTkAdvPB = QPushButton("...")
		self.AMinorTkLine.setFixedWidth(80)
		self.AMinorTkAdvPB.setFixedWidth(30)
		h1f = MHBoxLayout(  AMinorTkLabel, 0, self.AMinorTkLine, self.AMinorTkAdvPB)



		MajorTkChk         = QCheckBox("Show Major Tick")
		h2a = MHBoxLayout(  MajorTkChk, 0)

		MajorTkCLabel      = QLabel("Major Tick Width:")
		self.MajorTkCLine  = MColorPicker()
		self.MajorTkCLine.setFixedWidth(120)
		h2b = MHBoxLayout(  MajorTkCLabel, 0, self.MajorTkCLine)

		MajorTkWLabel      = QLabel("Major Tick Width:")
		MajorTkWidthLine   = QLineNumber()
		MajorTkWidthLine.setFixedWidth(80)
		h2c = MHBoxLayout(  MajorTkWLabel, 0, MajorTkWidthLine)

		MajorTkInLabel     = QLabel("Major Tick IN:")
		MajorTkOutLabel    = QLabel("  Out:")
		MajorTkInLine      = QLineNumber()
		MajorTkOutLine     = QLineNumber()
		MajorTkInLine.setFixedWidth(80)
		MajorTkOutLine.setFixedWidth(80)
		h2d = MHBoxLayout(  MajorTkInLabel, 0, MajorTkInLine, MajorTkOutLabel, MajorTkOutLine)

		label             = QLabel("Major Tick Font")
		label.setAlignment(Qt.AlignHCenter)
		h2e = MHBoxLayout(MHLine(), label, MHLine())
		self.MajorTkLBold = QCheckBox('B')
		self.MajorTkLItal = QCheckBox('I')
		self.MajorTkLSize = QSpinBox()
		self.MajorTkLFont = QComboBox()
		h2f = MHBoxLayout(QLabel("Size"), self.MajorTkLSize,0, QLabel("Font"), self.MajorTkLFont, 0, self.MajorTkLBold, self.MajorTkLItal)



		MinorTkChk         = QCheckBox("Show Minor Tick")
		h3a = MHBoxLayout(  MinorTkChk, 0)

		MinorTkCLabel      = QLabel("Minor Tick Width:")
		self.MinorTkCLine  = MColorPicker()
		self.MinorTkCLine.setFixedWidth(120)
		h3b = MHBoxLayout(  MinorTkCLabel, 0, self.MinorTkCLine)

		MinorTkWLabel      = QLabel("Minor Tick Width:")
		MinorTkWidthLine   = QLineNumber()
		MinorTkWidthLine.setFixedWidth(80)
		h3c = MHBoxLayout(  MinorTkWLabel, 0, MinorTkWidthLine)

		MinorTkInLabel     = QLabel("Minor Tick IN:")
		MinorTkOutLabel    = QLabel("  Out:")
		MinorTkInLine      = QLineNumber()
		MinorTkOutLine     = QLineNumber()
		MinorTkInLine.setFixedWidth(80)
		MinorTkOutLine.setFixedWidth(80)
		h3d = MHBoxLayout(  MinorTkInLabel, 0, MinorTkInLine, MinorTkOutLabel, MinorTkOutLine)

		label             = QLabel("Minor Tick Font")
		label.setAlignment(Qt.AlignHCenter)
		h3e = MHBoxLayout(MHLine(), label, MHLine())
		self.MinorTkLBold = QCheckBox('B')
		self.MinorTkLItal = QCheckBox('I')
		self.MinorTkLSize = QSpinBox()
		self.MinorTkLFont = QComboBox()
		h3f = MHBoxLayout(QLabel("Size"), self.MinorTkLSize,0, QLabel("Font"), self.MinorTkLFont, 0, self.MinorTkLBold, self.MinorTkLItal)


		
		v1 = MVBoxLayout(
			h0a, 5, h0b, 5, h0c, MHLine(),
			h1a, 5, h1b, 5, h1c, 5, h1d, 15, h1e, 5, h1f, MHLine(),
			h2a, 5, h2b, 5, h2c, 5, h2d, 15, h2e, 5, h2f, MHLine(),
			h3a, 5, h3b, 5, h3c, 5, h3d, 15, h3e, 5, h3f, MHLine(),
		 0)

		return v1
		

	def setAxisValue(self):
		pass
	
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