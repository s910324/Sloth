
class bokehSymbol(object):
	def __init__(self, symbol, parent = None):
		self.symbol  = symbol
		self.symbol.radius_dimension = 'y'
		self.symbol.radius_units     = 'screen'
		self.outLine = {'color'    : self.symbol.line_color,
						'width'    : self.symbol.line_width}	

		self.val     = {'color'    : self.symbol.fill_color,
						'size'     : self.symbol.size,
						'outLine'  : self.outLine}

	def symbol_color(self, color = None):
		if color:
			self.symbol.fill_color = color
		return self.symbol.fill_color

	def symbol_size(self, size = None):
		if size is not None:
			self.symbol.size = size
			print self.symbol.size
		return self.symbol.size

	def symbol_penColor(self, color = None):
		if color:
			self.symbol.line_color  = color
		return self.symbol.line_color	

	def symbol_penWidth(self, width = None):
		if width is not None:
			self.symbol.line_width  = width
		return self.symbol.line_width	


	def symbol_outLine(self, color = None, width = None):
		self.symbol_penColor(color)
		self.symbol_penWidth(width)
		return self.outLine


	def symbol_visible(self, visible = None ):
		if visible is not None:
			self.symbol.visible = visible
		return  self.symbol.visible

	def symbol_val(self, color   = None,   size    = None,
						 outLine = None,   visible = None):
		self.symbol_color(color)
		self.symbol_size(size)
		self.symbol_outLine(**outLine)
		self.symbol_visible(visible)
		return self.val
