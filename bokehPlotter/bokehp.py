import sys
import pickle
import numpy as np
import os
from PySide.QtGui    import *
from PySide.QtCore   import *
from PySide.QtWebKit import *
from bokeh.resources import CDN
from bokeh.embed     import file_html
from bokeh.models    import ColumnDataSource, Grid, GridPlot, LinearAxis, Plot, Range1d
from bokeh.plotting  import figure, show, output_file,  vplot


class PlotWindowWidget(QMainWindow):
	def __init__(self, parent = None):
		super(PlotWindowWidget, self).__init__(parent)
		self.Web = QWebView()
		self.Web.setContextMenuPolicy(Qt.CustomContextMenu)
		self.lineIDCounter    = -1
		self.lineIDDict       = {}

		self.plotIDCounter    = -1
		self.plotIDDict       = {}

		data     = self.loadCrew()
		self.div = self.plot(0, data)

		html     = file_html(self.div, CDN, "my plot")
		online   = 'http://cdn.pydata.org/bokeh/release'
		offline  =  'file://' + os.getcwd() 
		html     = html.replace(online,  offline)

		self.Web.setHtml(html)
		self.setCentralWidget(self.Web)
		self.initToolBar()

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

	# def plot(self, stack, dataSet):
	# 	plotPack = []
	# 	if not stack:
	# 		for i, data in enumerate(dataSet):
	# 			plot, rng = self.addPlotArea(data)
	# 			self.addPlotHolder(plot, rng)
	# 			plotPack.append(plot)
	# 		html = self.insertPlot(plotPack)
	# 	else:
	# 		plot, rng = self.addPlotArea(dataSet)
	# 		self.addPlotHolder(plot, rng)
	# 		plotPack.append(plot)
	# 		html = self.insertPlot(plotPack)			
	# 	return html

	def plot(self, stack, dataSet):
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

		return html

	def getRange(self, dataSet):

		xMins, xMaxs, yMins, yMaxs = [], [], [], []
		for data in dataSet:
			xMins.append(min(data[0]))
			xMaxs.append(max(data[0]))
			yMins.append(min(data[1]))
			yMaxs.append(max(data[1]))
		xmin, xmax, ymin, ymax = min(xMins), max(xMaxs), min(yMins), max(yMaxs)

		spamX, spamY = [float(xmax-xmin)*0.05, float(ymin-ymin)*0.05]
		rng = [xmin-spamX, xmax+spamX, ymin-spamY, ymax+spamY]
		return rng

	def initPlotArea(self, title = "Unitled graph", rng = [0,1,0,1],  w=800, h=300, bgc = "#001133", bdc = "#001133"):
		tool  = 'box_zoom,box_select,crosshair, save, reset'
		[xmin, xmax, ymin, ymax] = rng

		plotArea = figure(title=title, 
			x_range         = (xmin, xmax), 
			y_range         = (ymin, ymax), 
			tools           = tool, 
			plot_width      = w, 
			plot_height     = h, 
			background_fill = "#001133", 
			border_fill     = "#001133" )


		plotArea.title_text_color      = "#C8C8C8"
		plotArea.title_text_font_style = "bold"
		plotArea.title_text_font_size  = "10pt"

		plotArea.add_layout(LinearAxis(axis_line_color = "#C8C8C8" ), 'right')
		plotArea.add_layout(LinearAxis(axis_line_color = "#C8C8C8" ), 'above')

		plotArea.xaxis.axis_line_color        = "#C8C8C8"
		plotArea.xaxis.major_label_text_color = "#C8C8C8"
		plotArea.xaxis.major_tick_line_color  = "#C8C8C8"
		plotArea.xaxis.major_tick_line_width  = 1
		plotArea.xaxis.minor_tick_line_color  = "#C8C8C8"
		plotArea.xaxis.minor_tick_line_width  = 1

		plotArea.yaxis.axis_line_color        = "#C8C8C8"
		plotArea.yaxis.major_label_text_color = "#C8C8C8"
		plotArea.yaxis.major_tick_line_color  = "#C8C8C8"
		plotArea.yaxis.major_tick_line_width  = 1
		plotArea.yaxis.minor_tick_line_color  = "#C8C8C8"
		plotArea.yaxis.minor_tick_line_width  = 1

		plotArea.xaxis.major_tick_in  =  5 
		plotArea.xaxis.major_tick_out =  0
		plotArea.xaxis.minor_tick_in  =  3
		plotArea.xaxis.minor_tick_out =  0

		plotArea.yaxis.major_tick_in  =  5 
		plotArea.yaxis.major_tick_out =  0
		plotArea.yaxis.minor_tick_in  =  3
		plotArea.yaxis.minor_tick_out =  0


		plotArea.xgrid.grid_line_color = "#C8C8C8"
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

	def addPlotArea(self, data):
		x     = np.array(data[0])
		y     = np.array(data[1])

		radii = 0.008
		
		colors       = ["#%02x%02x%02x" % (200,200,200) for i in range(len(x))]
		spamX, spamY = [float(max(x)-min(x))*0.05, float(max(y)-min(y))*0.05]

		plotArea = figure(title='Pan and Zoom Here', x_range=(min(x)-spamX, max(x)+spamX), y_range=(min(y)-spamY, max(y)+spamY),
		            tools='box_zoom,box_select,crosshair, save, reset', plot_width=800, plot_height=300,
		            background_fill="#001133", border_fill="#001133")

		plotArea.title_text_color      = "#C8C8C8"
		plotArea.title_text_font_style = "bold"
		plotArea.title_text_font_size  = "10pt"

		plotArea.add_layout(LinearAxis(axis_line_color="#C8C8C8" ), 'right')
		plotArea.add_layout(LinearAxis(axis_line_color="#C8C8C8" ), 'above')

		plotArea.xaxis.axis_line_color        = "#C8C8C8"
		plotArea.xaxis.major_label_text_color = "#C8C8C8"
		plotArea.xaxis.major_tick_line_color  = "#C8C8C8"
		plotArea.xaxis.major_tick_line_width  = 1
		plotArea.xaxis.minor_tick_line_color  = "#C8C8C8"
		plotArea.xaxis.minor_tick_line_width  = 1

		plotArea.yaxis.axis_line_color        = "#C8C8C8"
		plotArea.yaxis.major_label_text_color = "#C8C8C8"
		plotArea.yaxis.major_tick_line_color  = "#C8C8C8"
		plotArea.yaxis.major_tick_line_width  = 1
		plotArea.yaxis.minor_tick_line_color  = "#C8C8C8"
		plotArea.yaxis.minor_tick_line_width  = 1

		plotArea.xaxis.major_tick_in  =  5 
		plotArea.xaxis.major_tick_out =  0
		plotArea.xaxis.minor_tick_in  =  3
		plotArea.xaxis.minor_tick_out =  0

		plotArea.yaxis.major_tick_in  =  5 
		plotArea.yaxis.major_tick_out =  0
		plotArea.yaxis.minor_tick_in  =  3
		plotArea.yaxis.minor_tick_out =  0


		plotArea.xgrid.grid_line_color = "#C8C8C8"
		plotArea.xgrid.grid_line_alpha =  0.5
		plotArea.xgrid.grid_line_dash  = [3,3]
		plotArea.ygrid.grid_line_color = "#C8C8C8"
		plotArea.ygrid.grid_line_alpha =  0.5
		plotArea.ygrid.grid_line_dash  = [3,3]

		legendText = 'plot'
		plotArea.line(x, y, legend=legendText, line_color=colors)
		plotArea.scatter(x, y, radius=radii, radius_dimension='y',  fill_color=colors, fill_alpha=1, line_color=None, legend=legendText)

		plotArea.legend.orientation           = "top_left"
		plotArea.legend.background_fill_alpha = 0.5
		plotArea.legend.border_line_width     = 1
		plotArea.legend.border_line_color     = "#C8C8C8"
		plotArea.legend.label_standoff        = 5
		plotArea.legend.glyph_width           = 20
		plotArea.legend.legend_spacing        = 5
		plotArea.legend.legend_padding        = 20
		# output_file("les_mis.html")
		# show(p1)
		# plotArea.toolbar_location = None
		plotRange = [min(x)-spamX, max(x)+spamX, min(y)-spamY, max(y)+spamY]
		return plotArea, plotRange


	def insertPlot(self, plotSets):
		
		layout = vplot(*plotSets)
		output_file("les_mis.html")
		# show(layout)
		for plot in plotSets:
			plot.toolbar_location = None
		return layout

	def resetGraph(self):
		for ID in self.plotIDDict:
			plot, rng = self.plotIDDict[ID]
			plot.x_range = Range1d(start=rng[0], end=rng[1])
			plot.y_range = Range1d(start=rng[2], end=rng[3])
		for ID in self.lineIDDict:
			line = self.lineIDDict[ID]
			line.line_visible(False)
		html = file_html(self.div, CDN, "my plot")
		online   = 'http://cdn.pydata.org/bokeh/release'
		offline  =  'file://' + os.getcwd() 
		html = html.replace(online,  offline)
		self.Web.setHtml(html)
		self.Web.reload()
		print 'a'

	def loadCrew(self):
		fileName = './savedData.pkl'
		package  = open( fileName, 'rb' )
		data = pickle.load( package )

		package.close()
		return data


class bokehPlot(object):
	def __init__(self, plot, parent = None):
		self.title = [None, None, None, None]

	def plot_title(self, text  = None, color = None, 
						 style = None, size  = None):
		if text is not None:
			self._plot_.title                 = text
		
		if color:
			self._plot_.title_text_color      = color
		
		if style:
			self._plot_.title_text_font_style = style

		if size is not None:
			self._plot_.title_text_font_size  = str(size)+"pt"

		self.title = [text, color, style, size]
		return self.title
	# def plot_axis():

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

	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window =  PlotWindowWidget()
	window.show()
	app.exec_()