class bokehAxis(object):
	def __init__(self, bokehPlot = None, axisNum = None, parent=None):
		super(bokehAxis, self).__init__()
		self.plot    = bokehPlot
		self.axisNum = axisNum
		self.axis    = self.plot.axis[axisNum]

		self.axis_label       = {'text'      : self.axis.axis_label,
								 'color'     : self.axis.axis_label_text_color}

		self.axis_majorTick   = {'tickIn'    : self.axis.major_tick_in,
								 'tickOut'   : self.axis.major_tick_out,
								 'width'     : self.axis.major_tick_line_width,
								 'color'     : self.axis.major_tick_line_color}  

		self.axis_minorTick   = {'tickIn'    : self.axis.minor_tick_in,
								 'tickOut'   : self.axis.minor_tick_out,
								 'width'     : self.axis.minor_tick_line_width,
								 'color'     : self.axis.minor_tick_line_color}  

 		self.axis_val         = {'color'     : self.axis.axis_line_color,
								 'width'     : self.axis.axis_line_width,
								 'label'     : self.axis_label,
								 'majorTick' : self.axis_majorTick,
								 'minorTick' : self.axis_minorTick}

	def plot_axis(self, color = None, width     = None, 
						label = None, majorTick = None, minorTick = None):
		if color:
			self.axis.axis_line_color                  = color
		if width is not None:
			self.axis.axis_line_width                  = width
		if label:
			self.plot_axis_label(    **label)
		if majorTick:
			self.plot_axis_majorTick(**majorTick)
		if minorTick:
			self.plot_axis_minorTick(**minorTick)

		self.axis_val.update({'color'     : self.axis.axis_line_color})
		self.axis_val.update({'width'     : self.axis.axis_line_width})	
		self.axis_val.update({'label'     : self.axis_label})
		self.axis_val.update({'majorTick' : self.axis_majorTick})						
		self.axis_val.update({'minorTick' : self.axis_minorTick})			
		return self.axis_val

	def plot_axis_label(self, text = None, color = None):
		if text is not None:
			self.axis.axis_label            = text
		if color:
			self.axis.axis_label_text_color = color

		self.axis_label.update({'text'  : self.axis.axis_label})
		self.axis_label.update({'color' : self.axis.axis_label_text_color})
		return self.axis_label

	def plot_axis_majorTick(self, tickIn = None, tickOut = None,
								   width = None, color   = None):
		if tickIn  is not None:
			self.axis.major_tick_in         = tickIn 
		if tickOut is not None:
			self.axis.major_tick_out        = tickOut 
		if width   is not None:
			self.axis.major_tick_line_width = width
		if color:
			self.axis.major_tick_line_color = color

		self.axis_majorTick.update({'tickIn'  : self.axis.major_tick_in})		
		self.axis_majorTick.update({'tickOut' : self.axis.major_tick_out})	
		self.axis_majorTick.update({'width'   : self.axis.major_tick_line_width})
		self.axis_majorTick.update({'color'   : self.axis.major_tick_line_color})		
		return self.axis_majorTick


	def plot_axis_minorTick(self, tickIn = None, tickOut = None, 
								  width  = None, color   = None):
		if tickIn  is not None:
			self.axis.minor_tick_in         = tickIn 
		if tickOut is not None:
			self.axis.minor_tick_out        = tickOut 
		if width   is not None:
			self.axis.minor_tick_line_width = width
		if color:
			self.axis.minor_tick_line_color = color

		self.axis_minorTick.update({'tickOut' : self.axis.minor_tick_out })			
		self.axis_minorTick.update({'tickIn'  : self.axis.minor_tick_in})		
		self.axis_minorTick.update({'width'   : self.axis.minor_tick_line_width})
		self.axis_minorTick.update({'color'   : self.axis.minor_tick_line_color})
		return self.axis_minorTick		