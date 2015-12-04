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
		self.html = None
		self.setCentralWidget(self.Web)
		self.initToolBar()
		self.show()

	def initToolBar(self):
		self.toolbar = QToolBar()
		self.addToolBar( Qt.TopToolBarArea , self.toolbar)
		resetAction = QAction('reset', self)
		self.toolbar.addAction(resetAction)
		resetAction.triggered.connect(self.resetGraph)

	def addLineHolder(self, line):	
		self.lineIDCounter += 1
		lineID  = self.lineIDCounter
		self.lineIDDict[lineID] = line
		return self.lineIDCounter	

	def addPlotHolder(self, plot, rng):	
		self.plotIDCounter += 1
		plotID  = self.plotIDCounter
		self.plotIDDict[plotID] = plot, rng
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
				plotRange = self.getRange([data])

				plotArea  = self.initPlotArea(rng = plotRange)
				self.addPlotHolder(plotArea, plotRange)
				plotPack.append(plotArea)

				legendText = 'plot ' + str(self.lineIDCounter + 1)
				line       =  self.addPlotLine(plotArea,legendText = legendText, data = data)
				self.addLineHolder(line)
				
			html = self.insertPlot(plotPack)

		else:
			plotRange = self.getRange(dataSet)
			plotArea  = self.initPlotArea(rng = plotRange)
			self.addPlotHolder(plotArea, plotRange)
			for i, data in enumerate(dataSet):
				legendText = 'plot ' + str(self.lineIDCounter + 1)
				line       =  self.addPlotLine(plotArea,legendText = legendText, data = data)
				self.addLineHolder(line)
			
			plotPack.append(plotArea)
			html = self.insertPlot(plotPack)	


		html      = file_html(html, CDN, "my plot")
		online    = 'http://cdn.pydata.org/bokeh/release'
		offline   =  'file://' + os.getcwd() + '/BokehJS'
		self.html = html.replace(online,  offline)
		self.Web.setHtml(self.html)
		self.Web.reload()
		return self.html

	
	def initPlotArea(self, title = "Unitled graph", rng = [0,1,0,1],  w=800, h=300, bgc = "#001133", bdc = "#001133"):
		tool  = 'box_zoom,box_select,crosshair, save, reset'
		[xmin, xmax, ymin, ymax] = rng

		plotArea = figure(
			x_range         = (xmin, xmax), 
			y_range         = (ymin, ymax), 
			plot_width      = w, 
			plot_height     = h)

		plotWrapper         = bokehPlot(plotArea)

		spec            = {'width'      : w,
						   'height'     : h,
						   'tools'      : tool,
						   'background' : "#001133",
						   'borderfill' : "#001133"}

		title           = {'text'     : title,
						   'color'    : "#AFAFAF",
						   'style'    : "bold",
						   'size'     : 10}

		majorTick       = { 'tickIn'  : 5,
							'tickOut' : 0,
							'width'   : 1,
							'color'   : "#AFAFAF"}  

		minorTick       = { 'tickIn'  : 3,
							'tickOut' : 0,
							'width'   : 1,
							'color'   : "#AFAFAF"}  

		plotArea.add_layout(LinearAxis(), 'right')
		plotArea.add_layout(LinearAxis(), 'above')

		plotWrapper.plot_spec( **spec)
		plotWrapper.plot_title(**title)
		for index in range(len(plotArea.axis)):
			other = "y" if index == 2 else ""
			text  = "x" if index == 1 else other
			
			axis_label = {'text'     : text,
						  'color'    : "#AFAFAF"}
			plotWrapper.plot_axis(num   = index,      color     = '#AFAFAF', width     = 1, 
								  label = axis_label, majorTick = majorTick, minorTick = minorTick)


		plotArea.xgrid.grid_line_color = "#AFAFAF"
		plotArea.xgrid.grid_line_alpha =  0.5
		plotArea.xgrid.grid_line_dash  = [3,3]
		plotArea.ygrid.grid_line_color = "#C8C8C8"
		plotArea.ygrid.grid_line_alpha =  0.5
		plotArea.ygrid.grid_line_dash  = [3,3]
		return plotArea

	

	def addPlotLine(self, plotArea, data = [None, None], legendText = 'plot', radii = 0.005, 
						  color = "#c8c8c8", width = 1.5, symbol = 'o', visible = True):
		x    = np.array(data[0])
		y    = np.array(data[1])
		l    = plotArea.line(x, y, legend=legendText, line_color=color, line_width = width, visible = visible)
		line = bokehLine(l.glyph)

		line.line_val( 
			name    = legendText, 
			color   = color, 
			width   = width,
			style   = None, 
			symbol  = symbol, 
			visible = visible, 
			viewNum = None
			)

		if symbol != None:
			plotArea.scatter(x, y, 
				radius          = radii, 
				radius_dimension= 'y',  
				fill_color      = color,
				fill_alpha      = 1, 
				line_color      = None, 
				legend          = legendText)

		plotArea.legend.orientation           = "top_left"
		plotArea.legend.background_fill_alpha = 0.5
		plotArea.legend.border_line_width     = 1
		plotArea.legend.border_line_color     = "#C8C8C8"
		plotArea.legend.label_standoff        = 5
		plotArea.legend.glyph_width           = 20
		plotArea.legend.legend_spacing        = 5
		plotArea.legend.legend_padding        = 20
		return line


	def insertPlot(self, plotSets):
		
		layout = vplot(*plotSets)
		output_file("les_mis.html")
		# show(layout)
		for plot in plotSets:
			plot.toolbar_location = None
		return layout

	def resetGraph(self):
		# for ID in self.plotIDDict:
		# 	plot, rng = self.plotIDDict[ID]
		# 	plot.x_range = Range1d(start=rng[0], end=rng[1])
		# 	plot.y_range = Range1d(start=rng[2], end=rng[3])
		for ID in self.lineIDDict:
			line = self.lineIDDict[ID]
			line.line_visible(False)
		# html = file_html(self.div, CDN, "my plot")
		# online   = 'http://cdn.pydata.org/bokeh/release'
		# offline  =  'file://' + os.getcwd() 
		# html = html.replace(online,  offline)
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

class bokehPlot(object):
	def __init__(self, plot, parent=None):
		super(bokehPlot, self).__init__()
		self.plot  = plot
		self.xaxis = self.plot.axis[0]
		self.yaxis = self.plot.axis[1]

		self.spec              = {'width'      : self.plot.plot_width,
								  'height'     : self.plot.plot_height,
								  'tools'      : self.plot.tools,
								  'background' : self.plot.background_fill,
								  'borderfill' : self.plot.border_fill} 

		self.title             = {'text'    : self.plot.title,
								  'color'   : self.plot.title_text_color ,
								  'style'   : self.plot.title_text_font_style,
								  'size'    : self.plot.title_text_font_size}

		self.xaxis_label       = {'text'    : self.xaxis.axis_label,
								  'color'   : self.xaxis.axis_label_text_color}

		self.yaxis_label       = {'text'    : self.yaxis.axis_label,
								  'color'   : self.yaxis.axis_label_text_color}

		self.xaxis_majorTick   = {'tickIn'  : self.xaxis.major_tick_in,
								  'tickOut' : self.xaxis.major_tick_out,
								  'width'   : self.xaxis.major_tick_line_width,
								  'color'   : self.xaxis.major_tick_line_color}  

		self.xaxis_minorTick   = {'tickIn'  : self.xaxis.minor_tick_in,
								  'tickOut' : self.xaxis.minor_tick_out,
								  'width'   : self.xaxis.minor_tick_line_width,
								  'color'   : self.xaxis.minor_tick_line_color}  
 
		self.yaxis_majorTick   = {'tickIn'  : self.yaxis.major_tick_in,
								  'tickOut' : self.yaxis.major_tick_out,
								  'width'   : self.yaxis.major_tick_line_width,
								  'color'   : self.yaxis.major_tick_line_color}  

		self.yaxis_minorTick   = {'tickIn'  : self.yaxis.minor_tick_in,
								  'tickOut' : self.yaxis.minor_tick_out,
								  'width'   : self.yaxis.minor_tick_line_width,
								  'color'   : self.yaxis.minor_tick_line_color}   

	def plot_spec(self,  width      = None, height     = None, tools = None, 
						 background = None, borderfill = None):
		if width is not None:
			self.plot.plot_width                   = width
		if height is not None:
			self.plot.plot_height                  = height
		if background:
			self.plot.background_fill              = background
		if borderfill:
			self.plot.border_fill                  = borderfill

		return self.plot_spec


	def plot_title(self, text  = None, color = None, 
						 style = None, size  = None):
		if text is not None:
			self.plot.title                        = text
		if color:
			self.plot.title_text_color             = color
		if style:
			self.plot.title_text_font_style        = style
		if size is not None:
			self.plot.title_text_font_size         = str(size)+"pt"

		return self.title


	def plot_xaxis(self, color     = None, width     = None, label = None,
						 majorTick = None, minorTick = None):
		if color:
			self.xaxis_color                  = color
		if width is not None:
			self.xaxis_width                  = width
		if label:
			self.plot_xaxis_label(**label)
		if majorTick:
			self.plot_xaxis_majorTick(**majorTick)
		if minorTick:
			self.plot_xaxis_minorTick(**minorTick)

		return self.xaxis


	def plot_xaxis_label(self, text = None, color = None):
		if text is not None:
			self.xaxis.axis_label            = text
		if color:
			self.xaxis.axis_label_text_color = color

		return self.xaxis_label


	def plot_xaxis_majorTick(self, tickIn = None, tickOut = None, width = None, color  = None):
		if tickIn  is not None:
			self.xaxis.major_tick_in         = tickIn 
		if tickOut is not None:
			self.xaxis.major_tick_out        = tickOut 
		if width   is not None:
			self.xaxis.major_tick_line_width = width
		if color:
			self.xaxis.major_tick_line_color = color

		return self.xaxis_majorTick


	def plot_xaxis_minorTick(self, tickIn = None, tickOut = None, width = None, color  = None):
		if tickIn  is not None:
			self.xaxis.minor_tick_in         = tickIn 
		if tickOut is not None:
			self.xaxis.minor_tick_out        = tickOut 
		if width   is not None:
			self.xaxis.minor_tick_line_width = width
		if color:
			self.xaxis.minor_tick_line_color = color

		return self.xaxis_minorTick


	def plot_yaxis(self, color     = None, width     = None, label = None,
						   majorTick = None, minorTick = None):
		if color:
			self.yaxis_color                  = color
		if width is not None:
			self.yaxis_width                  = width
		if label:
			self.plot_yaxis_label(**label)
		if majorTick:
			self.plot_yaxis_majorTick(**majorTick)
		if minorTick:
			self.plot_yaxis_minorTick(**minorTick)

		return self.yaxis

	def plot_yaxis_label(self, text = None, color = None):
		if text is not None:
			self.yaxis.axis_label                  = text
		if color:
			self.yaxis.axis_label_text_color       = color

		return self.yaxis_label

	def plot_yaxis_majorTick(self, tickIn = None, tickOut = None, width = None, color  = None):
		if tickIn  is not None:
			self.yaxis.major_tick_in          = tickIn 
		if tickOut is not None:
			self.yaxis.major_tick_out         = tickOut 
		if width   is not None:
			self.yaxis.major_tick_line_width  = width
		if color:
			self.yaxis.major_tick_line_color  = color

		return self.yaxis_majorTick

	def plot_yaxis_minorTick(self, tickIn = None, tickOut = None, width = None, color  = None):
		if tickIn  is not None:
			self.yaxis.minor_tick_in          = tickIn 
		if tickOut is not None:
			self.yaxis.minor_tick_out         = tickOut 
		if width   is not None:
			self.yaxis.minor_tick_line_width  = width
		if color:
			self.yaxis.minor_tick_line_color  = color

		return self.yaxis_minorTick		


	def plot_axis(self, num   = None, color     = None, width     = None, 
						label = None, majorTick = None, minorTick = None):
		if num is not None:
			axis = self.plot.axis[num]
			if color:
				axis.axis_line_color                  = color
			if width is not None:
				axis.axis_line_width                  = width
			if label:
				self.plot_axis_label(    num = num, **label)
			if majorTick:
				self.plot_axis_majorTick(num = num, **majorTick)
			if minorTick:
				self.plot_axis_minorTick(num = num, **minorTick)

			# return axis


	def plot_axis_label(self, num = None, text = None, color = None):
		if num is not None:
			axis = self.plot.axis[num]
			if text is not None:
				axis.axis_label                  = text
			if color:
				axis.axis_label_text_color       = color

		axis_label = {'text'    : axis.axis_label,
					  'color'   : axis.axis_label_text_color}

		return axis_label

	def plot_axis_majorTick(self, num     = None, tickIn = None, 
								  tickOut = None, width  = None, color  = None):
		if num is not None:
			axis = self.plot.axis[num]
			if tickIn  is not None:
				axis.major_tick_in          = tickIn 
			if tickOut is not None:
				axis.major_tick_out         = tickOut 
			if width   is not None:
				axis.major_tick_line_width  = width
			if color:
				axis.major_tick_line_color  = color

			axis_majorTick   = {'tickIn'  : axis.major_tick_in,
								'tickOut' : axis.major_tick_out,
								'width'   : axis.major_tick_line_width,
								'color'   : axis.major_tick_line_color}
		return axis_majorTick


	def plot_axis_minorTick(self, num     = None, tickIn = None, 
								  tickOut = None, width  = None, color  = None):
		if num is not None:
			axis = self.plot.axis[num]
			if tickIn  is not None:
				axis.minor_tick_in          = tickIn 
			if tickOut is not None:
				axis.minor_tick_out         = tickOut 
			if width   is not None:
				axis.minor_tick_line_width  = width
			if color:
				axis.minor_tick_line_color  = color
				
			axis_minorTick   = {'tickIn'  : axis.minor_tick_in,
								'tickOut' : axis.minor_tick_out,
								'width'   : axis.minor_tick_line_width,
								'color'   : axis.minor_tick_line_color}
		return axis_minorTick 	


class bokehLine(object):
	def __init__(self, line, parent = None):
		self.data,    self.name,    self.color  = None, None, None
		self.width,   self.style,   self.symbol = None, None, None
		self.visible, self.viewNum, self._line_ = None, None, line

	def line_name(self, name = None):
		if name:
			self.name = name
		return self.name

	def line_color(self, color = None ):
		if color:
			self.color = color
			self._line_.line_color = color
		return self.color

	def line_width(self, width = None ):
		if width:
			self.width = width
			self._line_.line_width = width
		return self.width	

	def line_style(self, style = None ):
		if style:
			self.style = style

		return self.style	

	def line_symbol(self, symbol = None ):
		if symbol:
			self.symbol = symbol
		return self.symbol

	def line_visible(self, visible = None ):
		if visible is not None:
			self._line_.visible = visible
		return  self.visible	


	def line_viewNum(self, viewNum = None):
		if viewNum is not None:
			self.viewNum = viewNum
		return self.viewNum

	def line_val(self, name  = None, color  = None, width   = None,
					   style = None, symbol = None, visible = None, viewNum = None):
		
		return [self.line_name(name),     self.line_color(color),
				self.line_width(width),   self.line_style(style),
				self.line_symbol(symbol), self.line_visible(visible), self.line_viewNum(viewNum)]


# class bokehSymbol(object):
# 	def __init__(self, data = [None, None], parent = None):
# 		self.color   = color
# 		self.size    = size
# 		self.outline = outline
# 		self.width   = width
# 		self.visible = visible
# 	def symbol_color(self, color = None):
# 		if color:
# 			self.scolor = color
# 			self.setSymbolBrush(pg.mkBrush(color = color))
# 		return self.scolor

# 	def symbol_size(self, size = None):
# 		if size:
# 			self.ssize = size
# 			self.setSymbolSize(size)
# 		return self.ssize

# 	def symbol_penColor(self, penC = None):
# 		if penC:
# 			self.spenColor = penC
# 			self.setSymbolPen(pg.mkPen(color = penC))
# 		return self.spenColor	

# 	def symbol_penWidth(self, penW = None):
# 		if penW != None:
# 			pen = self.symbol_penColor()
# 			self.spenWidth = penW
# 			if penW <= 0:
# 				self.symbol_penColor((pen[0], pen[1], pen[2], 0))
# 			if penW >  0:
# 				self.symbol_penColor((pen[0], pen[1], pen[2], 255))
# 				self.spenWidth = penW
# 			self.setSymbolPen(pg.mkPen(width = penW))
# 		return self.spenWidth	

# 	def symbol_outLine(self, outLine = None ):
# 		pen   = self.symbol_penColor()
# 		if outLine == True:
# 			self.symbol_penColor( (pen[0],   pen[1],   pen[2],   255))
# 			self.soutLine = outLine
# 		if outLine == False:
# 			self.symbol_penColor( (pen[0],   pen[1],   pen[2],   0))
# 			self.soutLine = outLine
# 		return self.soutLine

# 	def symbol_visible(self, visible = None ):
# 		color = self.symbol_color()
# 		if visible == True:
# 			self.symbol_color((   color[0], color[1], color[2], 255))
# 			self.svisible = visible
# 		if visible == False:
# 			self.symbol_color((    color[0], color[1], color[2], 0))
# 			self.symbol_outLine(False)
# 			self.svisible = visible
# 		return  self.svisible	



# 	def symbol_val(self, color   = None, size  = None,
# 						   penC    = None, penW  = None,
# 						   outLine = None, visible = None):
# 		return [self.symbol_color(color),     self.symbol_size(size),
# 				self.symbol_penColor(penC),   self.symbol_penWidth(penW),
# 				self.symbol_outLine(outLine), self.symbol_visible(visible)]

	

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