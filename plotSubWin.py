import sys
import PySide
from PySide.QtCore import *
from PySide.QtGui  import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from types import *

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
		self.graphBar = QToolBar('plot options')
		self.addToolBar( Qt.TopToolBarArea , self.graphBar)

		selectAction    = QAction('Select area', self)
		crosshairAction = QAction('Enable CrossHair', self)
		addHLineAction = QAction('Insert Horizontal Line', self)
		addVLineAction = QAction('Insert Verticle Line', self)
		
		self.graphBar.addAction(selectAction)
		self.graphBar.addAction(crosshairAction)
		self.graphBar.addAction(addHLineAction)
		self.graphBar.addAction(addVLineAction)
		#nextAction.triggered.connect(self.test2)    
		
					
		
	def initPlotArea(self):
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')
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
				self.plotLineHolder.append(line)
			else:
				plotAry = xAry if xAry != None else yAry
				xAry = np.linspace( 0, len( plotAry )-1, len( plotAry ))
				yAry = np.array( plotAry )
				line = plotArea.plot( np.array(xAry), np.array(yAry), name = plotName,
								  pen=pg.mkPen(color = lineColor, width=lineWidth, style=lineStyle), symbol = Sym[dotSym] ) 
				self.plotLineHolder.append(line)
			line.setSymbolBrush( pg.mkBrush(  color = dotColor ))
			line.setSymbolPen(   None )
			line.setSymbolSize( dotSize )
			plotArea.showGrid(x=True, y=True)
#            line.setPen(pg.mkPen(color = (255,0,0,255), width=5, style=QtCore.Qt.SolidLine))
#            self.w.setLabel('left', "Y Axis", units='A')
#            self.w.setLabel('bottom', "Y Axis", units='s')
#            self.w.setLogMode(x=True, y=False)
			legend.addItem( line, plotName )        


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
#                        
#class PlotSettings(QWidget):
#    def __init__(self, parent = None):
#        super(PlotSettings, self).__init__(parent)
#        self.XAxisLabel = QLabel('bottom Range:')
#        self.YAxisLabel = QLabel('left   Range:')
#        self.TAxisLabel = QLabel('top    Range:')
#        self.RAxisLabel = QLabel('right  Range:')
#        self.LDashLabel  = QLabel('<-')
#        self.RDashLabel  = QLabel('->')
#        self.UnitLabel  = QLabel(' ||    Label / Unit: ')
#        self.SlashLabel  = QLabel('/')
#        
#        self.XMaxEdit   = QLineEdit() 
#        self.XTickEdit  = QLineEdit() 
#        self.XMinEdit   = QLineEdit() 
#        self.XUnitEdit  = QLineEdit() 
#        self.XLabelEdit = QLineEdit() 
#        
#        self.YMaxEdit   = QLineEdit() 
#        self.YTickEdit  = QLineEdit() 
#        self.YMinEdit   = QLineEdit() 
#        self.YUnitEdit  = QLineEdit() 
#        self.YLabelEdit = QLineEdit() 
#        
#        self.TMaxEdit   = QLineEdit() 
#        self.TTickEdit  = QLineEdit() 
#        self.TMinEdit   = QLineEdit() 
#        self.TUnitEdit  = QLineEdit() 
#        self.TLabelEdit = QLineEdit()
#        
#        self.RMaxEdit   = QLineEdit() 
#        self.RTickEdit  = QLineEdit() 
#        self.RMinEdit   = QLineEdit() 
#        self.RUnitEdit  = QLineEdit() 
#        self.RLabelEdit = QLineEdit()
#        
#        self.Vbox  = QVBoxLayout()
#        self.Vbox.addLayout(self.HboxB)
#        self.Vbox.addLayout(self.HboxL)
#        self.Vbox.addLayout(self.HboxT)
#        self.Vbox.addLayout(self.HboxR)
#        self.HboxB = QHBoxLayout()
#        self.HboxL = QHBoxLayout()
#        self.HboxT = QHBoxLayout()
#        self.HboxR = QHBoxLayout()
#        
#        self.HboxB.addWidget( self.XAxisLabel  )
#        self.VboxB.addWidget( self.Xma    )
#        grid = QGridLayout()
#        grid.setSpacing(10)
#        grid.addWidget(XAxisLabel, 0,0)
#        grid.addWidget(XMaxEdit,   0,1)
#        #grid.addWidget(LDashLabel, 0,2)
#        grid.addWidget(XTickEdit,  0,3)
#        #grid.addWidget(RDashLabel, 0,4)
#        grid.addWidget(XMinEdit,   0,5)
#        #grid.addWidget(UnitLabel,  0,6)
#        grid.addWidget(XLabelEdit, 0,7)
#        #grid.addWidget(SlashLabel, 0,8)
#        grid.addWidget(XUnitEdit,  0,9)
#        
#        grid.addWidget(LAxisLabel, 1,0)
#        grid.addWidget(YMaxEdit,   1,1)
#        grid.addWidget(LDashLabel, 1,2)
#        grid.addWidget(YTickEdit,  1,3)
#        grid.addWidget(RDashLabel, 1,4)
#        grid.addWidget(YMinEdit,   1,5)
#        grid.addWidget(UnitLabel,  1,6)
#        grid.addWidget(YLabelEdit, 1,7)
#        grid.addWidget(SlashLabel, 1,8)
#        grid.addWidget(YUnitEdit,  1,9)
#        
#        grid.addWidget(TAxisLabel, 2,0)
#        grid.addWidget(TMaxEdit,   2,1)
#        #grid.addWidget(LDashLabel, 2,2)
#        grid.addWidget(TTickEdit,  2,3)
#        #grid.addWidget(RDashLabel, 2,4)
#        grid.addWidget(TMinEdit,   2,5)
#        #grid.addWidget(UnitLabel,  2,6)
#        grid.addWidget(TLabelEdit, 2,7)
#        #grid.addWidget(SlashLabel, 2,8)
#        grid.addWidget(TUnitEdit,  2,9)
#        
#        grid.addWidget(RAxisLabel, 3,0)
#        grid.addWidget(RMaxEdit,   3,1)
#        #grid.addWidget(DashLabel, 3,2)
#        grid.addWidget(RTickEdit,  3,3)
#        #grid.addWidget(RDashLabel, 3,4)
#        grid.addWidget(RMinEdit,   3,5)
#        #grid.addWidget(UnitLabel,  3,6)
#        grid.addWidget(RLabelEdit, 3,7)
#        #grid.addWidget(SlashLabel, 3,8)
#        grid.addWidget(RUnitEdit,  3,9)
#        
#        self.setLayout( grid )
#        #self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()    
	app.exec_()
	sys.exit