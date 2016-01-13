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
		boxZ = QVBoxLayout()
		boxZ.addLayout(box0)
		boxZ.addLayout(box1)
		boxZ.addLayout(box2)
		boxZ.addStretch()
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

		vbox = QVBoxLayout()
		vbox.addLayout(hbox0)
		vbox.addLayout(MHLine())
		vbox.addLayout(vbox1)
		vbox.addLayout(MHLine())
		vbox.addLayout(hbox2)
		vbox.addLayout(MHLine())
		vbox.addSpacing(25)
		# groupBox = QGroupBox('Graph Options:')
		groupBox = MGroupBox('Graph Options:')
		groupBox.addLayout(vbox)
		box = QVBoxLayout()
		box.addWidget(groupBox)
		return box


	def setupGridUI(self):

		self.showMajorGrid = QCheckBox("major Tick")
		self.showMinorGrid = QCheckBox("minor Tick")
		h0 =  MHBoxLayout( 0, self.showMajorGrid, 65, self.showMinorGrid ).setFixedWidth(85)

		
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


	


		v0   = MVBoxLayout(h0, MHLine(), h1, MHLine(), h2, MHLine())
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




# class MHLine(QHBoxLayout):
# 	def __init__(self, *args):
# 		super(MHLine, self).__init__()
# 		hline = QFrame()
# 		hline.setFrameStyle( QFrame.HLine  |  QFrame.Plain )
# 		hline.setFrameShadow( QFrame.Sunken )
# 		hline.setLineWidth(1)
# 		self.addSpacing(15)
# 		self.addWidget(hline)
# 		self.addSpacing(15)


# class MVLine(QVBoxLayout):
# 	def __init__(self, *args):
# 		super(MVLine, self).__init__()

# 		vline = QFrame()
# 		vline.setFrameStyle( QFrame.VLine  |  QFrame.Plain )
# 		vline.setFrameShadow( QFrame.Sunken )
# 		vline.setLineWidth(1)
# 		self.addSpacing(15)
# 		self.addWidget(vline)
# 		self.addSpacing(15)


# class MultiHBoxLayout(QHBoxLayout):
# 	def __init__(self, *args):
# 		super(MultiHBoxLayout, self).__init__()
# 		if args:
# 			self.addWidgets(*args)

# 	def addWidgets(self, *args):
# 		for widget in args:
# 			try:
# 				if widget == 0 :
# 					self.addStretch()
# 				elif type(widget) == types.IntType:
# 					self.addSpacing(widget)
# 				else:
# 					self.addWidget(widget)
# 			except:
# 				self.addLayout(widget)

# 	def addLayouts(self, *args):
# 		self.addWidgets(*args)


# class MultiVBoxLayout(QVBoxLayout):
# 	def __init__(self, *args):
# 		super(MultiVBoxLayout, self).__init__()
# 		if args:
# 			self.addWidgets(*args)

# 	def addWidgets(self, *args):
# 		for widget in args:
# 			try:
# 				if widget == 0 :
# 					self.addStretch()
# 				elif type(widget) == types.IntType:
# 					self.addSpacing(widget)
# 				else:
# 					self.addWidget(widget)
# 			except:
# 				self.addLayout(widget)

# 	def addLayouts(self, *args):
# 		self.addWidgets(*args)


class MAxisTabWidget(QTabWidget):
	def __init__(self, parent = None):
		super(MAxisTabWidget, self).__init__(parent)
		self.addAxis()
		self.addAxis()
		self.addAxis()
		self.addAxis()

	def addAxis(self):
		self.addTab(MAxisTab(), 'test')

class MAxisTab(QWidget):
	def __init__(self, parent = None):
		super(MAxisTab, self).__init__(parent)	
		pass

# class MGroupBox(QWidget):
# 	def __init__(self, title = None, parent = None):
# 		super(MGroupBox, self).__init__(parent)	
		
# 		self.MTitle = MGroupTitle(title)
# 		self.Midget = QWidget()
# 		self.v1     = QVBoxLayout()
# 		self.v2     = QVBoxLayout()
# 		self.h1     = QHBoxLayout()
# 		self.v1.addWidget(self.MTitle)
# 		self.v1.addLayout(self.h1)
# 		self.v1.addWidget(self.Midget)
# 		self.Midget.setLayout(self.v2)
# 		self.h1.addSpacing(25)


# 		self.v1.setSpacing(0)
# 		self.h1.setSpacing(0)
# 		self.v1.setContentsMargins(0,0,0,0)
# 		self.h1.setContentsMargins(0,0,0,0)
# 		self.setContentsMargins(0,0,0,0)
# 		self.setLayout(self.v1)
# 		self.MTitle.statChanged.connect(self.changeVisibility)

# 	def changeVisibility(self, stat):
# 		self.Midget.setVisible(stat)	

# 	def addWidget(self, widget = None):
# 		try:
# 			self.v2.addWidget(widget)
# 		except:
# 			self.v2.addLayout(widget)

# 	def addLayout(self, widget = None):	
# 		self.addWidget(widget)

# class MGroupTitle(QWidget):
# 	statChanged = Signal(bool)
# 	def __init__(self, title = None, parent = None):
# 		super(MGroupTitle, self).__init__(parent)	
# 		self.setFixedHeight(20)

# 		self.setContentsMargins(0,0,0,0)
# 		self.title = title
# 		self.stat  = True
# 		m = QHBoxLayout()
# 		m.setContentsMargins(0,0,0,0)
# 		m.setSpacing(0)
# 		l = QLabel(title)
# 		l.setFont(QFont('Helvetica [Cronyx]', 10, QFont.Bold))
# 		m.addSpacing(35)
# 		m.addWidget(l)
# 		self.setLayout(m)
		

# 	def paintEvent(self, event):
# 		painter = QPainter()
# 		painter.begin(self)
# 		self.drawWidget(painter)
# 		painter.end() 

# 	def drawWidget(self, painter):
# 		painter.setRenderHint(QPainter.Antialiasing)
# 		w, h     = self.size().width(), self.size().height()-2
# 		x, y     = self.pos().x(), self.pos().y()+1
# 		self.ctrlRect = QRectF(x+3, y+2, h-4, h-4)

# 		pen = QPen(QColor("#353535"))
# 		br  = QBrush(QColor("#353535"))
# 		br.setStyle(Qt.Dense4Pattern)
# 		pen.setWidthF(0.1)
# 		painter.setPen(pen)
# 		painter.setBrush(br)
# 		painter.drawEllipse(self.ctrlRect)
# 		painter.drawRect(QRect(x+25, y, w, h))


		
# 		pen = QPen()
# 		pen.setColor(QColor("#E2065F"))
# 		painter.setPen(pen)	
# 		painter.setFont(QFont('Helvetica [Cronyx]', 12, QFont.Bold))
# 		self.statTXT = "-" if self.stat else "+"
# 		painter.drawText(self.ctrlRect, Qt.AlignCenter, self.statTXT )
# 		pen.setColor(QColor("#CCC"))
# 		painter.setFont(QFont('Helvetica [Cronyx]', 10, QFont.Bold))
# 		painter.setPen(pen)	
# 		# painter.drawText(QRect(x+30, y, w, h), Qt.AlignLeft|Qt.AlignVCenter, self.title)


# 	def mousePressEvent(self, event):
# 		if self.ctrlRect.contains(event.pos()):
# 			self.stat = not self.stat
# 			self.statChanged.emit(self.stat)
# 			self.update()


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