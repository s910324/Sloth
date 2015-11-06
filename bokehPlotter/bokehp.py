import sys
import pickle
import numpy as np

from PySide.QtGui    import *
from PySide.QtCore   import *
from PySide.QtWebKit import *

from bokeh.resources import CDN
from bokeh.embed     import file_html
from bokeh.models    import ColumnDataSource, Grid, GridPlot, LinearAxis, Plot, Range1d
from bokeh.plotting  import figure


class PlotWindowWidget(QMainWindow):
	def __init__(self, parent = None):
		super(PlotWindowWidget, self).__init__(parent)
		self.Web = QWebView()
		self.Web.setContextMenuPolicy(Qt.CustomContextMenu)
		data = self.loadCrew()
		self.div, self.rng = self.plot(data)
		
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

	def plot(self, data):

		p1,p2 = data
		
		x = np.array(p1[0])
		y = np.array(p2[1])

		radii = 0.005
		
		colors = ["#%02x%02x%02x" % (200,200,200) for i in range(len(x))]

		p1 = figure(title='Pan and Zoom Here', x_range=(min(x), max(x)), y_range=(min(y), max(y)),
		            tools='box_zoom,box_select,crosshair,reset', plot_width=800, plot_height=300, toolbar_location=None,
		            background_fill="#001133", border_fill="#001133")


		p1.add_layout(LinearAxis(axis_line_color="#C8C8C8" ), 'right')
		p1.add_layout(LinearAxis(axis_line_color="#C8C8C8" ), 'above')

		p1.xaxis.axis_line_color       = "#C8C8C8"
		p1.xaxis.major_tick_line_color = "#C8C8C8"
		p1.xaxis.major_tick_line_width = 1
		p1.xaxis.minor_tick_line_color = "#C8C8C8"
		p1.xaxis.minor_tick_line_width = 1

		p1.yaxis.axis_line_color       = "#C8C8C8"
		p1.yaxis.major_tick_line_color = "#C8C8C8"
		p1.yaxis.major_tick_line_width = 1
		p1.yaxis.minor_tick_line_color = "#C8C8C8"
		p1.yaxis.minor_tick_line_width = 1

		p1.xaxis.major_tick_in  =  5 
		p1.xaxis.major_tick_out =  0
		p1.xaxis.minor_tick_in  =  3
		p1.xaxis.minor_tick_out =  0

		p1.yaxis.major_tick_in  =  5 
		p1.yaxis.major_tick_out =  0
		p1.yaxis.minor_tick_in  =  3
		p1.yaxis.minor_tick_out =  0

	

		p1.xgrid.grid_line_color = "#00ffC8"
		p1.xgrid.grid_line_alpha = 0.5
		p1.xgrid.grid_line_dash  = [5,5]
		p1.ygrid.grid_line_alpha = 0.5
		p1.ygrid.grid_line_dash  = [5,5]
		p1.scatter(x, y, radius=radii, fill_color=colors, fill_alpha=1, line_color=None)

	
		return p1, [min(x), max(x), min(y), max(y)]

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