import sys
import pickle
import numpy as np

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

		data = self.loadCrew()
	
		self.div= self.plot(1, data)
		
		html = file_html(self.div, CDN, "my plot")
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

				self.addPlotLine(plotArea, data = data)
			html = self.insertPlot(plotPack)
		else:
			plotRange = self.getRange(dataSet)
			plotArea  = self.initPlotArea(rng = plotRange)
			self.addPlotHolder(plotArea, plotRange)
			for i, data in enumerate(dataSet):
				self.addPlotLine(plotArea, data = data)
	
			
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

		# legendText = 'plot'
		# plotArea.line(x, y, legend=legendText, line_color=colors)
		# plotArea.scatter(x, y, radius=radii, radius_dimension='y',  fill_color=colors, fill_alpha=1, line_color=None, legend=legendText)

		plotArea.legend.orientation           = "top_left"
		plotArea.legend.background_fill_alpha = 0.5
		plotArea.legend.border_line_width     = 1
		plotArea.legend.border_line_color     = "#C8C8C8"
		plotArea.legend.label_standoff        = 5
		plotArea.legend.glyph_width           = 20
		plotArea.legend.legend_spacing        = 5
		plotArea.legend.legend_padding        = 20


		return plotArea

	def addPlotLine(self, plotArea, data = [None, None], legendText = 'plot', radii = 0.01, color = "#00000"):
		x = np.array(data[0])
		y = np.array(data[1])
		plotArea.line(x, y, legend=legendText, line_color=color)
		plotArea.scatter(x, y, 
			radius          = radii, 
			radius_dimension= 'y',  
			fill_color      = color,
			fill_alpha      = 1, 
			line_color      = None, 
			legend          = legendText)


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

		html = file_html(self.div, CDN, "my plot")
		
		self.Web.setHtml(html)
		print 'a'

	def loadCrew(self):
		fileName = './savedData.pkl'
		package  = open( fileName, 'rb' )
		data = pickle.load( package )

		package.close()
		return data


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window =  PlotWindowWidget()
	window.show()
	app.exec_()