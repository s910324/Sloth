import sys
import os
import re
import types        as types
from PySide         import QtGui
from PySide.QtGui   import *
from PySide.QtCore  import *
from PySide.QtWebKit import *
import bokeh
from bokeh.resources import CDN
from bokeh.embed     import file_html
from bokeh.models    import ColumnDataSource, Grid, GridPlot, LinearAxis, Plot, Range1d
from bokeh.plotting  import figure, show, output_file,  vplot
class MSymbolStylePicker(QWidget):
	def __init__(self, style = "circle", parent = None):
		super(MSymbolStylePicker, self).__init__(parent)
		self.setUpUI()



	def setUpUI(self):
		self.styleView  = MSymbolStyleView()
		self.styleCombo = QComboBox()
		self.size       = QSpinBox()
		text = ["Circle",  "CircleX", "Cross", "Diamond",  "DiamondCross","Square",
				"SquareX", "InvertedTriangle", "Triangle", "X", "Asterisk"]
		self.styleCombo.addItems(text)

		hbox = QHBoxLayout()
		hbox.addWidget(self.styleView)
		hbox.addWidget(self.styleCombo)
		hbox.addWidget(self.size)
		self.styleCombo.currentIndexChanged.connect(self.changeSymbol)
		self.size.valueChanged.connect(self.changeSize)
		self.setLayout(hbox)

	def changeSymbol(self):
		self.styleView.setScatterSymbol(self.styleCombo.currentText())

	def changeSize(self):
		self.styleView.symbol_val(size = self.size.value())


class MSymbolStyleView(QWidget):
	def __init__(self, style = "circle", parent = None):
		super(MSymbolStyleView, self).__init__(parent)
		self.html     = None
		self.plotArea = None
		self.scatter  = None
		
		self.setUpUI()
		self.initPlotArea(style = style)
		self.setFixedSize(130, 130)

	def setUpUI(self):
		box      = QHBoxLayout()		
		self.Web = QWebView()
		self.Web.setContextMenuPolicy(Qt.CustomContextMenu)
		box.addWidget(self.Web)
		self.setLayout(box)
		box.setContentsMargins(0,0,0,0)
		self.setContentsMargins(0,0,0,0)

	def drawSymbol(self, html = None):
		html      = file_html(html, CDN, "my plot")
		online    = 'http://cdn.pydata.org/bokeh/release'
		offline   =  'file://' + os.getcwd().split('/BokehGraphEditor')[0] + '/BokehJS'
		self.html = html.replace(online,  offline)
		self.Web.setHtml(self.html)
		self.Web.reload()

	def initPlotArea(self, style = None):
		self.plotArea = figure(

			plot_width         = 100, 
			plot_height        = 100,
			background_fill    = "#c1c1c1",
			border_fill        = "#c1c1c1",
			min_border         = 0)

		self.plotArea.xaxis.visible    = False
		self.plotArea.yaxis.visible    = False
		self.plotArea.toolbar_location = None
		self.scatter = self.plotArea.scatter([0], [0], marker = style.lower(), size = 88)

		
		
		self.html    = vplot( self.plotArea )
		self.drawSymbol(self.html)
		return self.html

	def setScatterSymbol(self, val = "Circle"):
		models    = bokeh.models.glyphs
		
		changeVal = self.scatter.glyph.changed_properties_with_values()
		glyph     = {
			"Circle"          : models.Circle(**changeVal),
			"CircleX"         : models.CircleX(**changeVal),
			"Cross"           : models.Cross(**changeVal),
			"Diamond"         : models.Diamond(**changeVal),
			"DiamondCross"    : models.DiamondCross(**changeVal),
			"Square"          : models.Square(**changeVal),
			"SquareX"         : models.SquareX(**changeVal),
			"InvertedTriangle": models.InvertedTriangle(**changeVal),
			"Triangle"        : models.Triangle(**changeVal),
			"X"               : models.X(**changeVal),
			"Asterisk"        : models.Asterisk(**changeVal)}
		
		self.scatter.set(glyph = glyph[val])
		self.html = vplot( self.plotArea )
		self.drawSymbol(self.html)
		return self.html


	# def symbol_outLine(self, color = None, width = None, visible = None):
	# 	if color:
	# 		self.scatter.line_color  = color
	# 	if width   is not None:
	# 		self.scatter.line_width  = width
	# 	if visible is not None:
	# 		self.scatter.line_alpha  = 255 if visible <= 1 else 0
			
	# 	self.outLine.update({'color'   : self.scatter.line_color})
	# 	self.outLine.update({'width'   : self.scatter.line_width})
	# 	self.outLine.update({'visible' : self.scatter.line_alpha})
	# 	return self.outLine

	def symbol_val(self, color   = None,   size    = None,
						 outLine = None,   visible = None):
		symbol = self.scatter.glyph
		if color:
			symbol.fill_color = color
		if size is not None:
			symbol.size = size	
		# if outLine:
		# 	self.symbol_outLine(**outLine)
		if visible is not None:
			symbol.visible = visible	

		# self.val.update({'color'   : symbol.fill_color})
		# self.val.update({'size'    : symbol.size})
		# # self.val.update({'outLine' : self.outLine})
		# self.val.update({'visible' : symbol.visible})
		# return self.val
		self.html = vplot( self.plotArea )
		self.drawSymbol(self.html)
		return self.html

def run():
	app        = QApplication(sys.argv)
	MainWindow = MSymbolStylePicker()
	# MainWindow = MSymbolStyleView()
	MainWindow.show()
	app.exec_()
	import os
	print "   *-*-*-*-* deBug mode is on *-*-*-*-*"
	print "File Path: " + os.path.realpath(__file__)

run()

