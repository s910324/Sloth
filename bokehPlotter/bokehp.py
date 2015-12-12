from __future__ import absolute_import
import sys
import types
import pickle
import numpy as np
import os
from PySide.QtGui    import *
from PySide.QtCore   import *
from PySide.QtWebKit import *
import bokeh
from bokeh.resources import CDN
from bokeh.embed     import file_html
from bokeh.models    import ColumnDataSource, Grid, GridPlot, LinearAxis, Plot, Range1d
from bokeh.plotting  import figure, show, output_file,  vplot
# sys.path.append("./BokehGraphEditor")
from BokehGraphEditor import EditorWindow 
from BokehGraphEditor.MaterialDesignList import *
try:
	from bokehPlot   import bokehPlot
	from bokehAxis   import bokehAxis
	from bokehLine   import bokehLine
	from bokehSymbol import bokehSymbol
except:
	from bokehPlotter.bokehPlot   import bokehPlot
	from bokehPlotter.bokehAxis   import bokehAxis
	from bokehPlotter.bokehLine   import bokehLine
	from bokehPlotter.bokehSymbol import bokehSymbol

class PlotWindowWidget(QMainWindow):
	def __init__(self, parent = None):
		super(PlotWindowWidget, self).__init__(parent)
		self.lock = True
		self.ID   = -1
		self.resize(1000,800)
		self.Web = QWebView()
		self.Web.setContextMenuPolicy(Qt.CustomContextMenu)
		self.lineIDCounter    = -1
		self.lineIDDict       = {}

		self.plotIDCounter    = -1
		self.plotIDDict       = {}
		self.html             = None
		self.setCentralWidget(self.Web)
		self.initToolBar()
		self.optionWindow     = None
		self.show()


	def initToolBar(self):
		self.toolbar  = QToolBar()
		resetAction   = QAction('reset', self)
		optionsAction = QAction('_Options', self)		
		self.toolbar.addAction(resetAction)
		self.toolbar.addAction(optionsAction)
		
		resetAction.triggered.connect(self.resetGraph)
		optionsAction.triggered.connect(self.showOptionPanel)
		self.addToolBar( Qt.TopToolBarArea , self.toolbar)

	def showOptionPanel(self):
		self.optionWindow = EditorWindow.EditorWindow()
		self.optionWindow.valChanged.connect(self.resetGraph)
		self.optionWindow.importPlotItems(self.plotIDDict, self.lineIDDict)
		self.optionWindow.show()

	def addLineHolder(self, lineWrap):	
		self.lineIDCounter += 1
		lineID  = self.lineIDCounter
		self.lineIDDict[lineID] = lineWrap
		return self.lineIDCounter	

	def addPlotHolder(self, plotWrap, rng):	
		self.plotIDCounter += 1
		plotID  = self.plotIDCounter
		self.plotIDDict[plotID] = plotWrap, rng
		return self.plotIDCounter	


	def getRange(self, dataSet):
		xMins, xMaxs, yMins, yMaxs = [], [], [], []
		for data in dataSet:
			xMins.append(min(data[0]))
			xMaxs.append(max(data[0]))
			yMins.append(min(data[1]))
			yMaxs.append(max(data[1]))
		xmin, xmax, ymin, ymax = min(xMins), max(xMaxs), min(yMins), max(yMaxs)

		spamX, spamY = [float(xmax-xmin)*0.05, float(ymax-ymin)*0.05]
		rng = [xmin-spamX, xmax+spamX, ymin-spamY, ymax+spamY]

		return rng


	def plotData(self, stack, dataSet):
		plotPack = []
		if not stack:
			for i, data in enumerate(dataSet):
				num       = self.lineIDCounter + 1
				plotRange = self.getRange([data])

				plotWrap  = self.initPlotArea(rng = plotRange, num = num)
				self.addPlotHolder(plotWrap, plotRange)
				plotPack.append(plotWrap)

				legendText = 'plot ' + str(num)
				lineWrap   =  self.addPlotLine(plotWrap,legendText = legendText, data = data)
				self.addLineHolder(lineWrap)
				
			html = self.insertPlot(plotPack)

		else:
			num       = self.lineIDCounter + 1
			plotRange = self.getRange(dataSet)
			plotWrap  = self.initPlotArea(rng = plotRange, num = num)
			self.addPlotHolder(plotWrap, plotRange)
			for i, data in enumerate(dataSet):
				legendText = 'plot ' + str(num)
				lineWrap   =  self.addPlotLine(plotWrap, legendText = legendText, data = data)
				self.addLineHolder(lineWrap)
			
			plotPack.append(plotWrap)
			html = self.insertPlot(plotPack)	


		html      = file_html(html, CDN, "my plot")
		online    = 'http://cdn.pydata.org/bokeh/release'
		offline   =  'file://' + os.getcwd() + '/BokehJS'
		self.html = html.replace(online,  offline)
		self.Web.setHtml(self.html)
		self.Web.reload()
		return self.html

	
	def initPlotArea(self, title = "Unitled graph", rng = [0,1,0,1], num = 0, w=800, h=300, bgc = "#001133", bdc = "#001133"):
		tool  = 'box_zoom,box_select,crosshair, save, reset'
		[xmin, xmax, ymin, ymax] = rng

		plotArea = figure(
			x_range         = (xmin, xmax), 
			y_range         = (ymin, ymax), 
			plot_width      = w, 
			plot_height     = h)

		plotWrapper         = bokehPlot(plotArea, num)

		spec            = {'width'      : w,
						   'height'     : h,
						   'tools'      : tool,
						   'background' : "#001133",
						   'borderfill' : "#001133",
						   'viewNum'    : num}

		title           = {'text'     : title,
						   'color'    : "#AFAFAF",
						   'style'    : "bold",
						   'size'     : 10}


		plotWrapper.plot_spec( **spec)
		plotWrapper.plot_title(**title)
		plotArea.add_layout(LinearAxis(axis_line_color = "#C8C8C8" ), 'right')
 		plotArea.add_layout(LinearAxis(axis_line_color = "#C8C8C8" ), 'above')		
		for index in range(len(plotArea.axis)):

			axisWrapper = bokehAxis(plotArea, index)
			plotWrapper.axis.append(axisWrapper)

			other = "y" if index == 2 else ""
			text  = "x" if index == 1 else other

			axis_label       = {'text'      : text,
								'color'     : "#AFAFAF"}

			axis_majorTick   = {'tickIn'    : 5,
								'tickOut'   : 0,
								'width'     : 1,
								'color'     : "#AFAFAF"}  

			axis_minorTick   = {'tickIn'    : 3,
								'tickOut'   : 0,
								'width'     : 1,
								'color'     : "#AFAFAF"}  

	 		axis_val         = {'color'     : "#AFAFAF",
								'width'     : "#AFAFAF",
								'label'     : axis_label,
								'majorTick' : axis_majorTick,
								'minorTick' : axis_minorTick}			
			axisWrapper.plot_axis(**axis_val)

		plotArea.xgrid.grid_line_color = "#AFAFAF"
		plotArea.xgrid.grid_line_alpha =  0.5
		plotArea.xgrid.grid_line_dash  = [3,3]
		plotArea.ygrid.grid_line_color = "#C8C8C8"
		plotArea.ygrid.grid_line_alpha =  0.5
		plotArea.ygrid.grid_line_dash  = [3,3]
		return plotWrapper

	

	def addPlotLine(self, plotWrap, data = [None, None], legendText = 'plot', radii = 2, 
						  color = "#c8c8c8", width = 1.5, symbol = 'o', visible = True):
		viewNum  = plotWrap.spec['viewNum']
		plotArea = plotWrap.plot
		x    = np.array(data[0])
		y    = np.array(data[1])
		
		if symbol != None:
			scatter       = plotArea.scatter(x, y, legend = legendText)
			symbolWrapper = bokehSymbol(scatter.glyph)

			outLine = { 'color'    : color,
						'width'    : None}		
			val     = { 'color'    : color,
						'size'     : radii,
						'outLine'  : outLine,
						'visible'  : True}
			symbolWrapper.symbol_val(**val)
		else:
			symbolWrapper = None

		l    = plotArea.line(x, y, legend=legendText, line_color=color, line_width = width, visible = visible)
		lineWrapper = bokehLine(l.glyph)
		lineWrapper.line_val( 
			name    = legendText, 
			color   = color, 
			width   = width,
			style   = None, 
			symbol  = symbolWrapper, 
			visible = visible, 
			viewNum = viewNum
			)
		
		plotArea.legend.orientation           = "top_left"
		plotArea.legend.background_fill_alpha = 0.5
		plotArea.legend.border_line_width     = 1
		plotArea.legend.border_line_color     = "#C8C8C8"
		plotArea.legend.label_standoff        = 5
		plotArea.legend.glyph_width           = 20
		plotArea.legend.legend_spacing        = 5
		plotArea.legend.legend_padding        = 20
		return lineWrapper


	def insertPlot(self, plotSets):
		plotSets = [wrapper.plot for wrapper in plotSets]
		layout   = vplot( *plotSets )
		output_file("les_mis.html")
		# show(layout)
		for plot in plotSets:
			plot.toolbar_location = None
		return layout

	def resetGraph(self):


		plotPack = []
		for ID in self.plotIDDict:
			plotWrap, rng = self.plotIDDict[ID]
			plotPack.append(plotWrap)

		html      = self.insertPlot(plotPack)	
		html      = file_html(html, CDN, "my plot")
		online    = 'http://cdn.pydata.org/bokeh/release'
		offline   =  'file://' + os.getcwd() + '/BokehJS'
		self.html = html.replace(online,  offline)
		self.Web.setHtml(self.html)
		self.Web.reload()


	def saveCrew(self, dataSet):
		fileName   = './savedData.pkl'
		fileHolder = open(fileName, 'wb')
		try:
			pickle.dump(dataSet, fileHolder)
		except (EnvironmentError, pickle.PicklingError) as err:
			raise SaveError(str(err))
		fileHolder.close()

	def loadCrew(self):
		fileName = './savedData.pkl'
		package  = open( fileName, 'rb' )
		data = pickle.load( package )

		package.close()
		return data

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

def Debugger():
	app  = QApplication(sys.argv)
	form = PlotWindowWidget()
	data = form.loadCrew()
	form.plotData(0, data)
	form.lock = False
	form.show()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)
	app.exec_()
Debugger()