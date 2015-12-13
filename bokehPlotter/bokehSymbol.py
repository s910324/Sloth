
class bokehSymbol(object):
	def __init__(self, symbol, parent = None):
		self.symbol  = symbol
		self.symbol.radius_dimension = 'y'
		self.symbol.radius_units     = 'screen'
		self.outLine = {'color'   : self.symbol.line_color,
						'width'   : self.symbol.line_width,
						'visible' : self.symbol.line_alpha}	

		self.val     = {'color'   : self.symbol.fill_color,
						'size'    : self.symbol.size,
						'outLine' : self.outLine,
						'visible' : self.symbol.visible}

	# def symbol_color(self, color = None):
	# 	if color:
	# 		self.symbol.fill_color = color
	# 	return self.symbol.fill_color

	# def symbol_size(self, size = None):
	# 	if size is not None:
	# 		self.symbol.size = size
	# 		print self.symbol.size
	# 	return self.symbol.size

	# def symbol_penColor(self, color = None):
	# 	if color:
	# 		self.symbol.line_color  = color
	# 	return self.symbol.line_color	

	# def symbol_penWidth(self, width = None):
	# 	if width is not None:
	# 		self.symbol.line_width  = width
	# 	return self.symbol.line_width	


	def symbol_outLine(self, color = None, width = None, visible = None):
		if color:
			self.symbol.line_color  = color
		if width   is not None:
			self.symbol.line_width  = width
		if visible is not None:
			self.symbol.line_alpha  = 255 if visible <= 1 else 0
			
		self.outLine.update({'color'   : self.symbol.line_color})
		self.outLine.update({'width'   : self.symbol.line_width})
		self.outLine.update({'visible' : self.symbol.line_alpha})
		return self.outLine


	# def symbol_visible(self, visible = None ):
	# 	if visible is not None:
	# 		self.symbol.visible = visible
	# 	return  self.symbol.visible

	def symbol_val(self, color   = None,   size    = None,
						 outLine = None,   visible = None):
		if color:
			self.symbol.fill_color = color
		if size is not None:
			self.symbol.size = size	
		if outLine:
			self.symbol_outLine(**outLine)
		if visible is not None:
			self.symbol.visible = visible	

		self.val.update({'color'   : self.symbol.fill_color})
		self.val.update({'size'    : self.symbol.size})
		self.val.update({'outLine' : self.outLine})
		self.val.update({'visible' : self.symbol.visible})
		return self.val
