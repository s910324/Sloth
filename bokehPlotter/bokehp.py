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
		data = self.loadCrew()
	
		self.div= self.plot(0, data)
		
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


	def plot(self, stack, dataSet):
		plotPack = []
		if not stack:
			for i, data in enumerate(dataSet):
				plot, rng = self.addPlotArea(data)
				plotPack.append(plot)
			html = self.insertPlot(plotPack)
		return html


	def addPlotArea(self, data):
		x     = np.array(data[0])
		y     = np.array(data[1])

		radii = 0.008
		
		colors       = ["#%02x%02x%02x" % (200,200,200) for i in range(len(x))]
		spamX, spamY = [float(max(x)-min(x))*0.05, float(max(y)-min(y))*0.05]

		p1 = figure(title='Pan and Zoom Here', x_range=(min(x)-spamX, max(x)+spamX), y_range=(min(y)-spamY, max(y)+spamY),
		            tools='box_zoom,box_select,crosshair, save, reset', plot_width=800, plot_height=300,
		            background_fill="#001133", border_fill="#001133")

		p1.title_text_color      = "#C8C8C8"
		p1.title_text_font_style = "bold"
		p1.title_text_font_size  = "10pt"

		p1.add_layout(LinearAxis(axis_line_color="#C8C8C8" ), 'right')
		p1.add_layout(LinearAxis(axis_line_color="#C8C8C8" ), 'above')

		p1.xaxis.axis_line_color        = "#C8C8C8"
		p1.xaxis.major_label_text_color = "#C8C8C8"
		p1.xaxis.major_tick_line_color  = "#C8C8C8"
		p1.xaxis.major_tick_line_width  = 1
		p1.xaxis.minor_tick_line_color  = "#C8C8C8"
		p1.xaxis.minor_tick_line_width  = 1

		p1.yaxis.axis_line_color        = "#C8C8C8"
		p1.yaxis.major_label_text_color = "#C8C8C8"
		p1.yaxis.major_tick_line_color  = "#C8C8C8"
		p1.yaxis.major_tick_line_width  = 1
		p1.yaxis.minor_tick_line_color  = "#C8C8C8"
		p1.yaxis.minor_tick_line_width  = 1

		p1.xaxis.major_tick_in  =  5 
		p1.xaxis.major_tick_out =  0
		p1.xaxis.minor_tick_in  =  3
		p1.xaxis.minor_tick_out =  0

		p1.yaxis.major_tick_in  =  5 
		p1.yaxis.major_tick_out =  0
		p1.yaxis.minor_tick_in  =  3
		p1.yaxis.minor_tick_out =  0


		p1.xgrid.grid_line_color = "#C8C8C8"
		p1.xgrid.grid_line_alpha =  0.5
		p1.xgrid.grid_line_dash  = [3,3]
		p1.ygrid.grid_line_color = "#C8C8C8"
		p1.ygrid.grid_line_alpha =  0.5
		p1.ygrid.grid_line_dash  = [3,3]

		legendText = 'plot'
		p1.line(x, y, legend=legendText, line_color=colors)
		p1.scatter(x, y, radius=radii, radius_dimension='y',  fill_color=colors, fill_alpha=1, line_color=None, legend=legendText)

		p1.legend.orientation           = "top_left"
		p1.legend.background_fill_alpha = 0.5
		p1.legend.border_line_width     = 1
		p1.legend.border_line_color     = "#C8C8C8"
		p1.legend.label_standoff        = 5
		p1.legend.glyph_width           = 20
		p1.legend.legend_spacing        = 5
		p1.legend.legend_padding        = 20
		# output_file("les_mis.html")
		# show(p1)
		# p1.toolbar_location = None
		return p1, [min(x)-spamX, max(x)+spamX, min(y)-spamY, max(y)+spamY]


	def insertPlot(self, plotSets):
		
		layout = vplot(*plotSets)
		output_file("les_mis.html")
		show(layout)
		for plot in plotSets:
			plot.toolbar_location = None
		return layout

	def resetGraph(self):
		self.div.x_range = Range1d(start=self.rng[0], end=self.rng[1])
		self.div.y_range = Range1d(start=self.rng[2], end=self.rng[3])

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