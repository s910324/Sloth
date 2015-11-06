import sys

import numpy as np

from PySide.QtGui    import *
from PySide.QtCore   import *
from PySide.QtWebKit import *

from bokeh.resources import CDN
from bokeh.embed     import file_html
from bokeh.models    import LinearAxis, Range1d
from bokeh.plotting  import figure


class PlotWindowWidget(QMainWindow):
	def __init__(self, parent = None):
		super(PlotWindowWidget, self).__init__(parent)
		self.Web = QWebView()
		self.Web.setContextMenuPolicy(Qt.CustomContextMenu)
		self.div = self.plot()
		self.a = [self.div.x_range.start, self.div.x_range.end, self.div.y_range.start, self.div.y_range.end]
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

	def plot(self):
		N = 4000

		x = np.random.random(size=N) * 100
		y = np.random.random(size=N) * 100
		radii = np.random.random(size=N) * 1.5
		colors = ["#%02x%02x%02x" % (r, g, 150) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))]

		p1 = figure(title='Pan and Zoom Here', x_range=(0, 100), y_range=(0, 100),
		            tools='box_zoom,box_select,crosshair,reset', plot_width=400, plot_height=400, toolbar_location=None)
		p1.extra_y_ranges = {"foo": Range1d(start=-100, end=200)}
		p1.add_layout(LinearAxis(), 'right')
		p1.add_layout(LinearAxis(), 'above')
		p1.scatter(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)

	
		return p1

	def resetGraph(self):
		self.div.x_range = Range1d(start=self.a[0], end=self.a[1])
		self.div.y_range = Range1d(start=self.a[2], end=self.a[3])

		html = file_html(self.div, CDN, "my plot")
		self.Web.setHtml(html)
		print 'a'



if __name__ == '__main__':
	app = QApplication(sys.argv)
	window =  PlotWindowWidget()
	window.show()
	app.exec_()