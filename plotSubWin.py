import sys
import pickle
import PySide
import types
from   types import *
import   graphOptions as gOption
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


# from QtVariant import QtGui, QtCore
# from PyQt4.QtCore import *
# from PyQt4.QtGui  import *

#from scipy.stats import futil
#from scipy.sparse.csgraph import _validation


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.mainWindow = QMainWindow()
		self.lock = True
		self.ID   = -1
		self.resize(1000,800)
		self.plotCounter = 0
#        self.initSettingDocker()
		self.initSettingToolbar()
		self.initPlotArea()
		self.plotLineHolder = []

		self.option  = gOption.graphProperty()
		self.lineIDCounter = -1
		self.lineIDDict    = {}

		self.colorMap = [ (200,200,200,255), (255,0,0,255), (0,0,255,255), (20,200,0,255),
					(255,0,115,255), (190,150,0,255), (10,0,175,255), (140,67,10,255),
					(255,0,255,255), (15,110,0,255), (0,37,102,255), (255,185,0,255),
					(130,0,217,255), (85,0,212,255)] 
		'''        
		p6 = win.addPlot(title="Updating plot")
		curve = p6.plot(pen='y')
		data = np.random.normal(size=(10,1000))
		ptr = 0
		def update():
			global curve, data, ptr, p6
			curve.setData(data[ptr%10])
			if ptr == 0:
				p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
			ptr += 1
		timer = QtCore.QTimer()
		timer.timeout.connect(update)
		timer.start(50)

		
		lr = pg.LinearRegionItem([400,700])
		lr.setZValue(-10)
		p8.addItem(lr)
		
		p9 = win.addPlot(title="Zoom on selected region")
		p9.plot(data2)
		def updatePlot():
			p9.setXRange(*lr.getRegion(), padding=0)
		def updateRegion():
			lr.setRegion(p9.getViewBox().viewRange()[0])
		lr.sigRegionChanged.connect(updatePlot)
		p9.sigXRangeChanged.connect(updateRegion)
		updatePlot()
		'''
			  
#        xAry = [2,3,5,7,11,15,21]
#        yAry = (xAry) 
#        zAry = [4,6,3,6,234,3,23]
#        w,l = self.addPlotArea()
#        self.insertPlot(xAry, yAry, w, l)
#        self.view.nextRow()        
#        w,l = self.addPlotArea()
#        self.insertPlot(xAry, zAry, w, l)
#        self.finitPlotArea(w)
#
#    
#    def initSettingDocker(self):
#        self.settingDockWidget = QDockWidget("  ::  Settings ::", self)
#        self.settingDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
#        self.settingDockWidget.setAllowedAreas(Qt.BottomDockWidgetArea and Qt.TopDockWidgetArea)
#        self.addDockWidget(Qt.BottomDockWidgetArea, self.settingDockWidget)
#        self.settings = PlotSettings()
#        self.settingDockWidget.setWidget(self.settings)
		
	def initSettingToolbar(self):
		self.graphBar   = QToolBar('plot options')
		self.addToolBar( Qt.TopToolBarArea , self.graphBar )

		selectAction    = QAction('Select area', self)
		optionAction    = QAction('Optons', self)
		crosshairAction = QAction('Enable CrossHair', self)
		addHLineAction  = QAction('Insert Horizontal Line', self)
		addVLineAction  = QAction('Insert Verticle Line', self)
		
		self.graphBar.addAction(optionAction)
		self.graphBar.addAction(selectAction)
		self.graphBar.addAction(crosshairAction)
		self.graphBar.addAction(addHLineAction)
		self.graphBar.addAction(addVLineAction)

		optionAction.triggered.connect(self.showOptionPanel)
		addHLineAction.triggered.connect(self.addLine)    

	def showOptionPanel(self):
		self.option.importPlotItems(self.lineIDDict)

		self.option.show()

	def addLineHolder(self, line):	
		self.lineIDCounter += 1
		lineID  = self.lineIDCounter
		self.lineIDDict[lineID] = line		
		return self.lineIDCounter	
					
		
	def initPlotArea(self):
		pg.setConfigOption('background', '#001133')
		pg.setConfigOption('foreground', '#888888')
		self.view = pg.GraphicsLayoutWidget()         
		scrollBarH = QScrollBar()
		scrollBarV = QScrollBar()
		self.view.setHorizontalScrollBar(scrollBarH)
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.view.setVerticalScrollBar(scrollBarV)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		
#        self.view.setBaseSize(2000,2000)
#        self.view.scale(1.5,1)
#        self.view.setFixedSize(self.size().height()*1.5, self.size().height())
		self.setCentralWidget(self.view)
#        self.setWindowTitle(winTitle)


	def addPlotArea(self, graphTitle = ''):
		self.vb = CustomViewBox()
		self.w = self.view.addPlot( viewBox = self.vb, enableMenu = False, title = graphTitle)
		self.view.nextRow()
		self.l = pg.LegendItem((100,60), offset=(70,70))  # args are (size, offset)
		self.l.setParentItem(self.w.graphicsItem())   # Note we do NOT call plt.addItem in this case
		return self.w, self.l
	



	def insertPlot(self, xAry = None, yAry = None, plotArea = None, legend = None, plotName = None, 
				lineColor = (0,0,0,255), lineWidth = 1, lineStyle = QtCore.Qt.SolidLine, 
				dotColor  = (0,0,0,255), dotSize   = 4,  dotSym = 0    ):
			Sym = [ 'o', 's', 't', 'd', '+' ]
			if plotName == None:
				plotName = 'Untitle {0}'.format(self.plotCounter)
				self.plotCounter += 1
			if ( xAry != None and yAry != None):
				line = plotArea.plot( np.array(xAry), np.array(yAry), name = plotName,
								  pen=pg.mkPen(color = lineColor, width=lineWidth, style=lineStyle), symbol = Sym[dotSym] ) 

			else:
				plotAry = xAry if xAry != None else yAry
				xAry = np.linspace( 0, len( plotAry )-1, len( plotAry ))
				yAry = np.array( plotAry )
				line = plotArea.plot( np.array(xAry), np.array(yAry), name = plotName,
								  pen=pg.mkPen(color = lineColor, width = lineWidth, style = lineStyle), symbol = Sym[dotSym] ) 

			self.addLineHolder(line)

			self.reWrapp_line(line)
			line.line_val(name  = plotName,  color  = lineColor,   width   = lineWidth,
				    	  style = lineStyle, symbol = Sym[dotSym], visible = True)		

			line.setSymbolBrush( pg.mkBrush(  color = dotColor ))
			line.setSymbolPen(   None )
			line.setSymbolSize( dotSize )
			plotArea.showGrid(x=True, y=True)
#            line.setPen(pg.mkPen(color = (255,0,0,255), width=5, style=QtCore.Qt.SolidLine))
#            self.w.setLabel('left', "Y Axis", units='A')
#            self.w.setLabel('bottom', "Y Axis", units='s')
#            self.w.setLogMode(x=True, y=False)
			legend.addItem( line, plotName )     


	def reWrapp_line(self, target):
		def line_name(target, name = None):
			if name:
				target.lname = name
			return target.lname

		def line_color(target, color = None ):
			if color:
				target.lcolor = color
			return target.lcolor

		def line_width(target, width = None ):
			if width:
				target.lwidth = width
			return target.lwidth	

		def line_style(target, style = None ):
			if style:
				target.lstyle = style
			return target.lstyle	

		def line_symbol(target, symbol = None ):
			if  symbol:
				target.lsymbol = symbol
			return target.lsymbol

		def line_visible(target, visible = None ):

			if visible is not None:
				target.setVisible(visible)
			target.lvisible = target.isVisible()
				
			return  target.lvisible	

		def line_val(target, name  = None, color  = None, width = None,
				    		 style = None, symbol = None, visible = None):

			return [target.line_name(name),     target.line_color(color),
					target.line_width(width),   target.line_style(style),
					target.line_symbol(symbol), target.line_visible(visible)]

		target.line_name    = types.MethodType(line_name,    target)
		target.line_color   = types.MethodType(line_color,   target)
		target.line_width   = types.MethodType(line_width,   target)
		target.line_style   = types.MethodType(line_style,   target)
		target.line_symbol  = types.MethodType(line_symbol,  target)
		target.line_visible = types.MethodType(line_visible, target)
		target.line_val     = types.MethodType(line_val,     target)


	def finitPlotArea(self, plotArea = None, legend = None, axisNameAry = None, unitAry = None, showAxis = [1, 1, 1, 1]):
		axisNameAry = axisNameAry if type(axisNameAry) == ListType else ['','','','']
		unitAry     = unitAry     if type(unitAry)     == ListType else ['','','','']
		showAxis    = showAxis    if type(showAxis)    == ListType else [ 1, 1, 1, 1]

		for i in range( 0, len(unitAry) - len(axisNameAry)):
			unitAry.append('')
		if len(axisNameAry) > 0:
			plotArea.setLabel(axis = 'bottom', text = axisNameAry[0], units = unitAry[0], unitPrefix = None )
		if len(axisNameAry) > 1:
			plotArea.setLabel(axis = 'left',   text = axisNameAry[1], units = unitAry[1], unitPrefix = None )
		if len(axisNameAry) > 2:
			plotArea.setLabel(axis = 'top',    text = axisNameAry[2], units = unitAry[2], unitPrefix = None )
		if len(axisNameAry) > 3:
			plotArea.setLabel(axis = 'right',  text = axisNameAry[3], units = unitAry[3], unitPrefix = None )
		self.w.showAxis('bottom', show= showAxis[0])
		self.w.showAxis('left',   show= showAxis[1])                
		self.w.showAxis('top',    show= showAxis[2])
		self.w.showAxis('right',  show= showAxis[3])

	def plotData(self, stack, dataSet):
		try:
			if stack:
				p,l = self.addPlotArea('graphtitle')

			for i, data in enumerate(dataSet):
				plotArrayX, plotArrayY = data
				if stack:
					print 'plot stacked plots'
					self.insertPlot(plotArrayX, plotArrayY, plotArea = p, legend = l, lineColor = self.colorMap[i%14], dotColor = self.colorMap[i%14])
				
				if not stack:
					print 'plot unstacked plots'
					p,l = self.addPlotArea('graphtitle')
					self.insertPlot(plotArrayX, plotArrayY, plotArea = p, legend = l, lineColor = self.colorMap[i%14], dotColor = self.colorMap[i%14])
					self.finitPlotArea(plotArea = p, legend = l) #'multiplot'				

			if stack:
				self.finitPlotArea(plotArea = p, legend = l)

		except AttributeError:
			raise AttributeError

	def addLine(self):
		point1, point2 = [-1.6, 151.6], [1.6, 151.6]
		line     = pg.GraphItem()
		position = np.array([ point1, point2 ])
		adjust   = np.array([[ 0, 1 ]])
		penStyle = pg.mkPen(color=(200, 200, 255), style=QtCore.Qt.DotLine)
		symbols  = ['x','x']

		line.setData(pos=position, adj=adjust, pen=penStyle, size=1, symbol=symbols, pxMode=True,)
		self.vb.addItem(line)
		self.addLineHolder(line)
		
		def rewrapp_name( name = None ):
			if name:
				self.name = name
			return self.name
		# self.reWrapp( line )
		line.line_name = rewrapp_name
		line.line_name('line{0}'.format(self.lineIDCounter))
		return line
	

	def modifyPlot(self):
		print 'a'
#
#    def resizeEvent(self, event):
#        print 'a'
#        self.view.setFixedSize(self.size().height() * 1.5, self.size().height() * 0.95)
	def closeEvent(self, event):
		if self.lock:
			self.showMinimized()
			event.ignore()

		else:
			self.showMaximized()
			event.accept()

	def unlock(self) :
		self.lock = False

	def lock(self) :
		self.lock = True	




		
class CustomViewBox(pg.ViewBox):
	def __init__(self, *args, **kwds):
		pg.ViewBox.__init__(self, *args, **kwds)
		self.setMouseMode(self.RectMode)

	def mouseClickEvent(self, ev):
		if ev.button() == QtCore.Qt.RightButton:
			self.autoRange()
			
	def mouseDragEvent(self, ev):
		if ev.button() == QtCore.Qt.RightButton:
			ev.ignore()
		else:
			pg.ViewBox.mouseDragEvent(self, ev)   

#        

class DebugWindow(QMainWindow):
	def __init__(self, parent=None):
		super(DebugWindow, self).__init__(parent)
		self.plot          = MainWindow()
		self.plot.lock     = False
		self.toolbar       = QToolBar('main function')
		self.selectAction  = QAction('select', self)
		self.addColAction  = QAction('add Col', self)
		self.rmvColAction  = QAction('rmv Col', self)

		self.toolbar.addAction(self.selectAction)
		self.toolbar.addAction(self.addColAction)
		self.toolbar.addAction(self.rmvColAction)

		self.selectAction.triggered.connect(self.setPen)
		# self.addColAction.triggered.connect(self.table.rmvCol)
		# self.rmvColAction.triggered.connect(self.table.addCol)

		self.addToolBar( Qt.TopToolBarArea , self.toolbar)

		# self.table.setRowCount(200)
		# self.table.addCol(15)


		data = self.loadCrew()
		self.plot.plotData(1, data)

		self.setCentralWidget(self.plot)
		self.resize(900,700)
		self.a = 0

	def setPen(self):
		line = self.plot.lineIDDict[0]
		print line.curve.setPen('#009900')
		# print dir(line.curve.setPen())

		# line.setPen(pg.mkPen(color = (0,255,0,255) ))

	def saveData(self, data):
		fileName   = './savedData.pkl'
		fileHolder = open(fileName, 'wb')
		try:
			pickle.dump(data, fileHolder)
		except (EnvironmentError, pickle.PicklingError) as err:
			raise SaveError(str(err))
		
		fileHolder.close()

	def loadCrew(self):
		fileName = './savedData.pkl'
		package  = open( fileName, 'rb' )
		data = pickle.load( package )

		package.close()
		return data
def Debugger():
	app  = QApplication(sys.argv)
	form = DebugWindow()
	form.show()
	app.exec_()
Debugger()