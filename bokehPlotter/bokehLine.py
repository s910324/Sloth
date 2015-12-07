
class bokehLine(object):
	def __init__(self, line, symbol = None, viewNum = None, parent = None):
		self.line    = line
		self.symbol  = symbol
		self.viewNum = viewNum
		self.val = {'name'    : self.line.name, 
					'color'   : self.line.line_color,
					'width'   : self.line.line_width,
					'style'   : None,
					'symbol'  : self.symbol, 
					'visibe'  : self.line.visible, 
					'viewNum' : self.viewNum}

		self.data,    self.name,    self.color  = None, None, None
		self.width,   self.style,   self.symbol = None, None, None
		self.visible, self.viewNum, self.line   = None, None, line

	def line_name(self, name = None):
		if name is not None:
			self.name      = name
			self.line.name = name
		return self.name

	def line_color(self, color = None ):
		if color:
			self.color           = color
			self.line.line_color = color
		return self.color

	def line_width(self, width = None ):
		if width:
			self.width           = width
			self.line.line_width = width
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
			self.visible      = visible
			self.line.visible = visible
		return  self.visible	


	def line_viewNum(self, viewNum = None):
		if viewNum is not None:
			self.viewNum = viewNum
		return self.viewNum

	def line_val(self, name  = None, color  = None, width   = None,
					   style = None, symbol = None, visible = None, viewNum = None):
		self.line_name(name)
		self.line_color(color)
		self.line_width(width)
		self.line_style(style)
		self.line_symbol(symbol)
		self.line_visible(visible)
		self.line_viewNum(viewNum)

		return self.val
