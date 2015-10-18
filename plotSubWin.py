import sys
import pickle
import PySide
import types
from   types import *
import   graphOptions as gOption
import graphSelectorWindow as gSelector
from   PySide.QtCore import *
from   PySide.QtGui  import *
from   pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.mainWindow = QMainWindow()
		self.lock = True
		self.ID   = -1
		self.resize(1000,800)

		self.initSettingToolbar()
		self.initPlotArea()


		self.option  = gOption.graphProperty()
		self.lineIDCounter    = -1
		self.lineIDDict       = {}

		self.plotIDCounter    = -1
		self.plotIDDict       = {}

		self.colorMap = [ (200,200,200,255), (255,0,0,255),   (0,0,255,255),  (20,200,0,255),
						  (255,0,115,255),   (190,150,0,255), (10,0,175,255), (140,67,10,255),
						  (255,0,255,255),   (15,110,0,255),  (0,37,102,255), (255,185,0,255),
						  (130,0,217,255),   (85,0,212,255)] 
		
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


	def addPlotHolder(self, plot, legend, viewBox):	
		self.plotIDCounter += 1
		plotID  = self.plotIDCounter
		self.plotIDDict[plotID] = plot, legend, viewBox
		print 'a'
		print self.plotIDCounter
		return self.plotIDCounter	

			
		
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
		viewBox  = CustomViewBox()
		plotArea = self.view.addPlot( viewBox = viewBox, enableMenu = False, title = graphTitle)
		legend   = pg.LegendItem((100,60), offset=(70,70))  # args are (size, offset)
		
		legend.setParentItem(plotArea.graphicsItem())   # Note we do NOT call plt.addItem in this case
		self.view.nextRow()
		self.addPlotHolder(plotArea, legend, viewBox)
		# self.w, self.l = plotArea, legend
		return plotArea, legend, viewBox#self.w, self.l



	def insertPlot(self, xAry      = None,        yAry      = None,        plotArea  = None, legend    = None,
						 plotName  = None,        lineColor = (0,0,0,255), lineWidth = 1,    lineStyle = QtCore.Qt.SolidLine, 
						 dotColor  = (0,0,0,255), dotSize   = 5,           dotSym    = 0,    addLegend = True ):
		Sym = [ 'o', 's', 't', 'd', '+' ]
		if plotName == None:
			plotName = 'Untitle {0}'.format(self.plotIDCounter)
			
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
		line.line_val(   name   = plotName,    color   = lineColor,
						 width  = lineWidth,   style   = lineStyle, 
						 symbol = Sym[dotSym], visible = True )		
		# line.line_color(lineColor)
		line.symbol_val( color   = dotColor,      size    = dotSize,
						 penC    = (0,255,0,255), penW    = 2,
						 outLine = False,         visible = True )

		plotArea.showGrid(x=True, y=True)
		if addLegend:
			legend.addItem( line, plotName )
		return line

#            self.w.setLabel('left', "Y Axis", units='A')
#            self.w.setLabel('bottom', "Y Axis", units='s')
#            self.w.setLogMode(x=True, y=False)
 


	def reWrapp_line(self, target):
		target.lcolor = None
		target.lwidth = None
		target.lstyle = None
		def line_name(target, name = None):
			if name:
				target.lname = name
			return target.lname

		def line_color(target, color = None ):
			if color:
				target.lcolor = color
				width = target.lwidth
				style = target.lstyle
				if style != None or width != None:
					target.line_setPen(color = color, width = width, style = style)
			return target.lcolor

		def line_width(target, width = None ):
			if width:
				target.lwidth = width
				color = target.lcolor
				style = target.lstyle
				if color != None or style != None:
					target.line_setPen(color = color, width = width, style = style)
			return target.lwidth	

		def line_style(target, style = None ):
			if style:
				target.lstyle = style
				width = target.lwidth
				color = target.lcolor
				if color != None or width != None:
					target.line_setPen(color = color, width = width, style = style)
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
		
		def line_setPen(target, color = None, width = None, style = None):
			if color == None:
				color = target.lcolor
			if width == None:
				width = target.lwidth
			if style == None:
				style = target.lstyle

			target.setPen(pg.mkPen(color = color, width = width, style = style))
			return color, width, style


		def line_val(target, name  = None, color  = None, width = None,
				    		 style = None, symbol = None, visible = None):

			if sum([ elem != None for elem in [color, width, style]]) > 1:
				target.line_setPen(color = color, width = width, style = style)
			
			return [target.line_name(name),     target.line_color(),
					target.line_width(),        target.line_style(),
					target.line_symbol(symbol), target.line_visible(visible)]

		def symbol_color(target, color = None):
			if color:
				target.scolor = color
				target.setSymbolBrush(pg.mkBrush(color = color))
			return target.scolor

		def symbol_size(target, size = None):
			if size:
				target.ssize = size
				target.setSymbolSize(size)
			return target.ssize

		def symbol_penColor(target, penC = None):
			if penC:
				target.spenColor = penC
				target.setSymbolPen(pg.mkPen(color = penC))
			return target.spenColor	

		def symbol_penWidth(target, penW = None):
			if penW != None:
				pen = target.symbol_penColor()
				target.spenWidth = penW
				if penW <= 0:
					target.symbol_penColor((pen[0], pen[1], pen[2], 0))
				if penW >  0:
					target.symbol_penColor((pen[0], pen[1], pen[2], 255))
					target.spenWidth = penW
				target.setSymbolPen(pg.mkPen(width = penW))
			return target.spenWidth	

		def symbol_outLine(target, outLine = None ):
			pen   = target.symbol_penColor()
			if outLine == True:
				target.symbol_penColor( (pen[0],   pen[1],   pen[2],   255))
				target.soutLine = outLine
			if outLine == False:
				target.symbol_penColor( (pen[0],   pen[1],   pen[2],   0))
				target.soutLine = outLine
			return target.soutLine

		def symbol_visible(target, visible = None ):
			color = target.symbol_color()
			if visible == True:
				target.symbol_color((   color[0], color[1], color[2], 255))
				target.svisible = visible
			if visible == False:
				target.symbol_color((    color[0], color[1], color[2], 0))
				target.symbol_outLine(False)
				target.svisible = visible
			return  target.svisible	



		def symbol_val(target, color   = None, size  = None,
							   penC    = None, penW  = None,
							   outLine = None, visible = None):
			return [target.symbol_color(color),    target.symbol_size(size),
					target.symbol_penColor(penC),  target.symbol_penWidth(penW),
					target.symbol_outLine(outLine), target.symbol_visible(visible)]

		target.line_name       = types.MethodType(line_name,       target)
		target.line_color      = types.MethodType(line_color,      target)
		target.line_width      = types.MethodType(line_width,      target)
		target.line_style      = types.MethodType(line_style,      target)
		target.line_symbol     = types.MethodType(line_symbol,     target)
		target.line_visible    = types.MethodType(line_visible,    target)
		target.line_setPen     = types.MethodType(line_setPen,     target)
		target.line_val        = types.MethodType(line_val,        target)

		target.symbol_color    = types.MethodType(symbol_color,    target)
		target.symbol_size     = types.MethodType(symbol_size,     target)
		target.symbol_penColor = types.MethodType(symbol_penColor, target)
		target.symbol_penWidth = types.MethodType(symbol_penWidth, target)		
		target.symbol_visible  = types.MethodType(symbol_visible,  target)
		target.symbol_outLine  = types.MethodType(symbol_outLine,  target)
		target.symbol_val      = types.MethodType(symbol_val,      target)



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


		# self.w.showAxis('bottom', show= showAxis[0])
		# self.w.showAxis('left',   show= showAxis[1])                
		# self.w.showAxis('top',    show= showAxis[2])
		# self.w.showAxis('right',  show= showAxis[3])
		plotArea.showAxis('bottom', show= showAxis[0])
		plotArea.showAxis('left',   show= showAxis[1])                
		plotArea.showAxis('top',    show= showAxis[2])
		plotArea.showAxis('right',  show= showAxis[3])

	def plotData(self, stack, dataSet):
		try:
			linePack = []
			if stack:
				p,l,v = self.addPlotArea('graphtitle')

			for i, data in enumerate(dataSet):
				plotArrayX, plotArrayY = data
				if stack:
					print 'plot stacked plots'
					line = self.insertPlot(plotArrayX, plotArrayY, plotArea = p, legend = l, lineColor = self.colorMap[i%14], dotColor = self.colorMap[i%14])
				
				if not stack:
					print 'plot unstacked plots'
					p,l,v = self.addPlotArea('graphtitle')
					line  = self.insertPlot(plotArrayX, plotArrayY, plotArea = p, legend = l, lineColor = self.colorMap[i%14], dotColor = self.colorMap[i%14])
					self.finitPlotArea(plotArea = p, legend = l) #'multiplot'				
				linePack.append(line)

			if stack:
				self.finitPlotArea(plotArea = p, legend = l)
			return linePack
		except AttributeError:
			raise AttributeError

	def addLine(self, plotArea = None, data = [-1.6, 1.6, 151.6, 151.6]):

		plotArrayX, plotArrayY = [data[0], data[2]], [data[1], data[3]]
		p, l, v    = self.plotIDDict[plotArea]
		lineColor  = (255,0,0,255)
		line       = self.insertPlot(plotArrayX, plotArrayY, plotArea = p, legend = l, lineColor = lineColor, dotColor = lineColor, addLegend = False)

		# self.addLineHolder(line)

		
		plotName   = 'line{0}'.format(self.lineIDCounter)
		lineWidth  = 2
		lineStyle  = Qt.SolidLine
		lineSymbol = 2
		self.reWrapp_line(line)

		line.line_val(   name   = plotName,       color   = lineColor,
						 width  = lineWidth,      style   = lineStyle, 
						 symbol = lineSymbol,     visible = True )		

		line.symbol_val( color   = lineColor,     size    = 5,
						 penC    = (0,255,0,255), penW    = 2,
						 outLine = False,         visible = True )


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
		self.text = pg.TextItem(html=u'<div style="text-align: center";><span style="color: rgba(255, 255, 255, 0); font-size: 35pt; ">x</span><span style="color: rgba(255, 255, 255, 180); font-size: 35pt; ">S e l e c t e d</span><span style="color: rgba(255, 255, 255, 0); font-size: 35pt; ">x</span></div>', anchor=(0.5,0.5), border='fff8', fill=None)
		self.text.border.setWidth(2)
		self.text.border.setStyle(Qt.DotLine)
		self.text.setVisible(False)
		self.addItem(self.text)


	def setSelect(self, selected):
		if selected:
		
			brush = pg.mkBrush(color = "#2FA000")
			brush.setStyle(Qt.Dense6Pattern)
			xRange, yRange = self.childrenBounds()
			self.setBackgroundColor(brush)
			self.text.setPos((xRange[0]+xRange[1])/2, (yRange[0]+yRange[1])/2)
			self.text.setVisible(True)
		else:
			self.setBackgroundColor(None)
			self.text.setVisible(False)
		

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

		data = self.loadCrew()

		self.plot.plotData(0, data)
		p, l, v = self.plot.plotIDDict[1]

		# v.setBackgroundColor('#880000')
		self.v = v
		self.a = False
		# self.v.setDisable()


		self.setCentralWidget(self.plot)
		self.resize(900,700)


	def setPen(self):

		a = gSelector.graphSelector()
		a.requestPreview.connect(self.plot.addLine, Qt.QueuedConnection)

		a.addPlotHolders(self.plot.plotIDDict)
		a.show()

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