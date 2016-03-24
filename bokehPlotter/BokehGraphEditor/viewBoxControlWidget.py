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
		width      = self.Gwidth.value()
		height     = self.GHeight.value()
		background = self.bgColorLine.getColor()
		borderfill = self.bdColorLine.getColor()
		print borderfill
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

		self.axisLineChk   = QCheckBox("Show Axis Line")
		ARLabel            = QLabel("Axis Range:")
		dashLabel          = QLabel(" - ")
		self.axisUPRngLine = QLineNumber()
		self.axisDNRngLine = QLineNumber()
		self.axisUPRngLine.setFixedWidth(80)
		self.axisDNRngLine.setFixedWidth(80)
		h1 = MHBoxLayout( self.axisLineChk, 0)
		h2 = MHBoxLayout(  ARLabel, 0, self.axisUPRngLine, dashLabel, self.axisDNRngLine)


		AWLabel            = QLabel("Axis Style (width/format):")
		self.axisWSpin     = QSpinBox()
		self.axisSCombo    = QComboBox()
		self.axisWSpin.setFixedWidth(40)
		self.axisSCombo.setFixedWidth(80)
		h3 = MHBoxLayout(  AWLabel, 0, self.axisWSpin, self.axisSCombo)


		ACLabel            = QLabel("Axis Color:")
		self.axisCLine     = MColorPicker()
		self.axisCLine.setFixedWidth(120)
		h4 = MHBoxLayout(  ACLabel, 0, self.axisCLine)

		AMajorTkLabel      = QLabel("Major Tick Step:")
		self.AMajorTkLine  = QLineNumber()
		self.AMajorTkAdvPB = QPushButton("...")
		self.AMajorTkLine.setFixedWidth(80)
		self.AMajorTkAdvPB.setFixedWidth(30)

		AMinorTkLabel      = QLabel("Minor Tick Step:")
		self.AMinorTkLine  = QLineNumber()
		self.AMinorTkAdvPB = QPushButton("...")
		self.AMinorTkLine.setFixedWidth(80)
		self.AMinorTkAdvPB.setFixedWidth(30)

		h5 = MHBoxLayout(  AMajorTkLabel, 0, self.AMajorTkLine, self.AMajorTkAdvPB)
		h6 = MHBoxLayout(  AMinorTkLabel, 0, self.AMinorTkLine, self.AMinorTkAdvPB)



		MajorTkChk         = QCheckBox("Show Major Tick")
		h7a = MHBoxLayout(  MajorTkChk, 0)

		MajorTkCLabel      = QLabel("Major Tick Width:")
		self.MajorTkCLine  = MColorPicker()
		self.MajorTkCLine.setFixedWidth(120)
		h7b = MHBoxLayout(  MajorTkCLabel, 0, self.MajorTkCLine)

		MajorTkWLabel      = QLabel("Major Tick Width:")
		MajorTkWidthLine   = QLineNumber()
		MajorTkWidthLine.setFixedWidth(80)
		h7c = MHBoxLayout(  MajorTkWLabel, 0, MajorTkWidthLine)

		MajorTkInLabel     = QLabel("Major Tick IN:")
		MajorTkOutLabel    = QLabel("  Out:")
		MajorTkInLine      = QLineNumber()
		MajorTkOutLine     = QLineNumber()
		MajorTkInLine.setFixedWidth(80)
		MajorTkOutLine.setFixedWidth(80)
		h7d = MHBoxLayout(  MajorTkInLabel, 0, MajorTkInLine, MajorTkOutLabel, MajorTkOutLine)



		MinorTkChk         = QCheckBox("Show Minor Tick")
		h8a = MHBoxLayout(  MinorTkChk, 0)

		MinorTkCLabel      = QLabel("Minor Tick Width:")
		self.MinorTkCLine  = MColorPicker()
		self.MinorTkCLine.setFixedWidth(120)
		h8b = MHBoxLayout(  MinorTkCLabel, 0, self.MinorTkCLine)

		MinorTkWLabel      = QLabel("Minor Tick Width:")
		MinorTkWidthLine   = QLineNumber()
		MinorTkWidthLine.setFixedWidth(80)
		h8c = MHBoxLayout(  MinorTkWLabel, 0, MinorTkWidthLine)

		MinorTkInLabel     = QLabel("Minor Tick IN:")
		MinorTkOutLabel    = QLabel("  Out:")
		MinorTkInLine      = QLineNumber()
		MinorTkOutLine     = QLineNumber()
		MinorTkInLine.setFixedWidth(80)
		MinorTkOutLine.setFixedWidth(80)
		h8d = MHBoxLayout(  MinorTkInLabel, 0, MinorTkInLine, MinorTkOutLabel, MinorTkOutLine)
		
		v1 = MVBoxLayout(h0, MHLine(),
			h1,  5, h2,  5, h3,  5, h4, 15, h5, 5, h6, MHLine(),
			h7a, 5, h7b, 5, h7c, 5, h7d, MHLine(),
			h8a, 5, h8b, 5, h8c, 5, h8d, MHLine(),
		 0)

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