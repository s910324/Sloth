from bokehAxis import bokehAxis
class bokehPlot(object):
	def __init__(self, plot, parent=None):
		super(bokehPlot, self).__init__()
		self.viewNum    = None
		self.plot       = plot
		self.axis       = []

		self.title      = {'text'       : self.plot.title,
						   'color'      : self.plot.title_text_color ,
						   'style'      : self.plot.title_text_font_style,
						   'size'       : self.plot.title_text_font_size}

		# print self.plot.grid[0].grid_line_color


		# self.xMajorGrid = {'color'      : self.plot.xgrid.grid_line_color,
		# 				   'dash'       : self.plot.xgrid.grid_line_dash,
		# 				   'width'      : self.plot.xgrid.grid_line_width}

		# self.xMinorGrid = {'color'      : self.plot.xgrid.minor_grid_line_color,
		# 				   'dash'       : self.plot.xgrid.minor_grid_line_dash,
		# 				   'width'      : self.plot.xgrid.minor_grid_line_width}

		# self.yMajorGrid = {'color'      : self.plot.ygrid.grid_line_color,
		# 				   'dash'       : self.plot.ygrid.grid_line_dash,
		# 				   'width'      : self.plot.ygrid.grid_line_width}

		# self.yMinorGrid = {'color'      : self.plot.ygrid.minor_grid_line_color,
		# 				   'dash'       : self.plot.ygrid.minor_grid_line_dash,
		# 				   'width'      : self.plot.ygrid.minor_grid_line_width}

		# self.grid       = {'xMajorGrid' : self.xMajorGrid,
		# 				   'xMinorGrid' : self.xMinorGrid,
		# 				   'yMajorGrid' : self.yMajorGrid,
		# 				   'yMinorGrid' : self.yMinorGrid}


		self.spec       = {'width'      : self.plot.plot_width,
						   'height'     : self.plot.plot_height,
						   'tools'      : self.plot.tools,
						   'background' : self.plot.background_fill
,
						   'borderfill' : self.plot.border_fill
,
						   'viewNum'    : self.viewNum}#,
						   # 'title'      : self.title,
						   # 'grid'       : self.grid}					 
		


	def plot_spec(self,  width      = None, height     = None, tools   = None, 
						 background = None, borderfill = None, viewNum = None,
						 title      = None):
		if width is not None:
			self.plot.plot_width            = width
		if height is not None:
			self.plot.plot_height           = height
		if background:
			self.plot.background_fill       = background
		if borderfill:
			self.plot.border_fill           = borderfill
		if viewNum is not None:
			self.viewNum                    = viewNum
		if title:
			self.title                      = self.plot_title(**title)

		self.spec.update({'width'      : self.plot.plot_width})
		self.spec.update({'height'     : self.plot.plot_height})
		self.spec.update({'background' : self.plot.background_fill})
		self.spec.update({'borderfill' : self.plot.border_fill})
		self.spec.update({'viewNum'    : self.viewNum})
		self.spec.update({'title'      : self.title})
		return self.spec


	def plot_title(self, text  = None, color = None, 
						 style = None, size  = None):
		if text is not None:
			self.plot.title                 = text
		if color:
			self.plot.title_text_color      = color
		if style:
			self.plot.title_text_font_style = style
		if size is not None:
			self.plot.title_text_font_size  = str(size)+ "pt" * ("pt" not in str(size))

		self.title.update({'text'  : self.plot.title})			
		self.title.update({'color' : self.plot.title_text_color})			
		self.title.update({'style' : self.plot.title_text_font_style})
		self.title.update({'size'  : self.plot.title_text_font_size})
		return self.title
