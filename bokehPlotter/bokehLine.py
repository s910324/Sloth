
class bokehLine(object):
	def __init__(self, line, symbol = None, viewNum = None, parent = None):
		self.line    = line
		self.symbol  = symbol
		self.viewNum = viewNum
		self.style   = None
		self.val = {'name'    : self.line.name, 
					'color'   : self.line.line_color,
					'width'   : self.line.line_width,
					'style'   : None,
					'symbol'  : self.symbol, 
					'visible' : self.line.visible, 
					'viewNum' : self.viewNum}

	def line_val(self, name  = None, color  = None, width   = None,
					   style = None, symbol = None, visible = None, viewNum = None):
		if name is not None:
			self.line.name       = name
		if color:
			self.line.line_color = color	
		if width is not None:
			self.line.line_width = width
		if style:
			self.style           = style	
		if symbol:
			self.symbol          = symbol	
		if visible is not None:
			self.line.visible    = visible
		if viewNum is not None:
			self.viewNum         = viewNum

		self.val.update({'name'    : self.line.name})	
		self.val.update({'color'   : self.line.line_color})
		self.val.update({'width'   : self.line.line_width})
		self.val.update({'style'   : self.style})
		self.val.update({'symbol'  : self.symbol})
		self.val.update({'visible' : self.line.visible})
		self.val.update({'viewNum' : self.viewNum})
		return self.val
