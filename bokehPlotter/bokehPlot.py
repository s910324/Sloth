from bokehAxis import bokehAxis
class bokehPlot(object):
	def __init__(self, plot, parent=None):
		super(bokehPlot, self).__init__()
		self.viewNum  = None
		self.plot     = plot
		self.axis     = []
		# self.xaxis    = self.plot.axis[0]
		# self.yaxis    = self.plot.axis[1]

		self.spec              = {'width'      : self.plot.plot_width,
								  'height'     : self.plot.plot_height,
								  'tools'      : self.plot.tools,
								  'background' : self.plot.background_fill,
								  'borderfill' : self.plot.border_fill,
								  'viewNum'    : self.viewNum} 

		self.title             = {'text'    : self.plot.title,
								  'color'   : self.plot.title_text_color ,
								  'style'   : self.plot.title_text_font_style,
								  'size'    : self.plot.title_text_font_size}

		# self.xaxis_label       = {'text'    : self.xaxis.axis_label,
		# 						  'color'   : self.xaxis.axis_label_text_color}

		# self.yaxis_label       = {'text'    : self.yaxis.axis_label,
		# 						  'color'   : self.yaxis.axis_label_text_color}

		# self.xaxis_majorTick   = {'tickIn'  : self.xaxis.major_tick_in,
		# 						  'tickOut' : self.xaxis.major_tick_out,
		# 						  'width'   : self.xaxis.major_tick_line_width,
		# 						  'color'   : self.xaxis.major_tick_line_color}  

		# self.xaxis_minorTick   = {'tickIn'  : self.xaxis.minor_tick_in,
		# 						  'tickOut' : self.xaxis.minor_tick_out,
		# 						  'width'   : self.xaxis.minor_tick_line_width,
		# 						  'color'   : self.xaxis.minor_tick_line_color}  
 
		# self.yaxis_majorTick   = {'tickIn'  : self.yaxis.major_tick_in,
		# 						  'tickOut' : self.yaxis.major_tick_out,
		# 						  'width'   : self.yaxis.major_tick_line_width,
		# 						  'color'   : self.yaxis.major_tick_line_color}  

		# self.yaxis_minorTick   = {'tickIn'  : self.yaxis.minor_tick_in,
		# 						  'tickOut' : self.yaxis.minor_tick_out,
		# 						  'width'   : self.yaxis.minor_tick_line_width,
		# 						  'color'   : self.yaxis.minor_tick_line_color}   

	def plot_spec(self,  width      = None, height     = None, tools   = None, 
						 background = None, borderfill = None, viewNum = None):
		if width is not None:
			self.plot.plot_width                   = width
			self.spec.update({'width' : width})
		if height is not None:
			self.plot.plot_height                  = height
			self.spec.update({'height' : height})
		if background:
			self.plot.background_fill              = background
			self.spec.update({'background' : background})
		if borderfill:
			self.plot.border_fill                  = borderfill
			self.spec.update({'borderfill' : borderfill})
		if viewNum is not None:
			self.viewNum                           = viewNum
			self.spec.update({'viewNum' : viewNum})
		return self.spec


	def plot_title(self, text  = None, color = None, 
						 style = None, size  = None):
		if text is not None:
			self.plot.title                        = text
			self.title.update({'text' : text})
		if color:
			self.plot.title_text_color             = color
			self.title.update({'color' : color})
		if style:
			self.plot.title_text_font_style        = style
			self.title.update({'style' : style})
		if size is not None:
			self.plot.title_text_font_size         = str(size)+"pt"
			self.title.update({'size' : str(size) + "pt"})

		return self.title


	# def plot_xaxis(self, color     = None, width     = None, label = None,
	# 					 majorTick = None, minorTick = None):
	# 	if color:
	# 		self.xaxis_color                  = color
	# 	if width is not None:
	# 		self.xaxis_width                  = width
	# 	if label:
	# 		self.plot_xaxis_label(**label)
	# 	if majorTick:
	# 		self.plot_xaxis_majorTick(**majorTick)
	# 	if minorTick:
	# 		self.plot_xaxis_minorTick(**minorTick)

	# 	return self.xaxis


	# def plot_xaxis_label(self, text = None, color = None):
	# 	if text is not None:
	# 		self.xaxis.axis_label            = text
	# 		self.xaxis_label.update({'text' : text})
	# 	if color:
	# 		self.xaxis.axis_label_text_color = color
	# 		self.xaxis_label.update({'color' : color})
	# 	return self.xaxis_label


	# def plot_xaxis_majorTick(self, tickIn = None, tickOut = None, width = None, color  = None):
	# 	if tickIn  is not None:
	# 		self.xaxis.major_tick_in         = tickIn 
	# 		self.xaxis_majorTick.update({'tickIn' : tickIn})
	# 	if tickOut is not None:
	# 		self.xaxis.major_tick_out        = tickOut 
	# 		self.xaxis_majorTick.update({'tickOut' : tickOut})
	# 	if width   is not None:
	# 		self.xaxis.major_tick_line_width = width
	# 		self.xaxis_majorTick.update({'width' : width})
	# 	if color:
	# 		self.xaxis.major_tick_line_color = color
	# 		self.xaxis_majorTick.update({'color' : color})

	# 	return self.xaxis_majorTick


	# def plot_xaxis_minorTick(self, tickIn = None, tickOut = None, width = None, color  = None):
	# 	if tickIn  is not None:
	# 		self.xaxis.minor_tick_in         = tickIn 
	# 		self.xaxis_minorTick.update({'tickIn' : tickIn})
	# 	if tickOut is not None:
	# 		self.xaxis.minor_tick_out        = tickOut 
	# 		self.xaxis_minorTick.update({'tickOut' : tickOut})
	# 	if width   is not None:
	# 		self.xaxis.minor_tick_line_width = width
	# 		self.xaxis_minorTick.update({'width' : width})
	# 	if color:
	# 		self.xaxis.minor_tick_line_color = color
	# 		self.xaxis_minorTick.update({'color' : color})

	# 	return self.xaxis_minorTick


	# def plot_yaxis(self, color     = None, width     = None, label = None,
	# 					 majorTick = None, minorTick = None):
	# 	if color:
	# 		self.yaxis_color                  = color
	# 	if width is not None:
	# 		self.yaxis_width                  = width
	# 	if label:
	# 		self.plot_yaxis_label(**label)
	# 	if majorTick:
	# 		self.plot_yaxis_majorTick(**majorTick)
	# 	if minorTick:
	# 		self.plot_yaxis_minorTick(**minorTick)

	# 	return self.yaxis

	# def plot_yaxis_label(self, text = None, color = None):
	# 	if text is not None:
	# 		self.yaxis.axis_label            = text
	# 		self.yaxis_label.update({'text' : text})
	# 	if color:
	# 		self.yaxis.axis_label_text_color = color
	# 		self.yaxis_label.update({'color' : color})
	# 	return self.yaxis_label


	# def plot_yaxis_majorTick(self, tickIn = None, tickOut = None, width = None, color  = None):
	# 	if tickIn  is not None:
	# 		self.yaxis.major_tick_in         = tickIn 
	# 		self.yaxis_majorTick.update({'tickIn' : tickIn})
	# 	if tickOut is not None:
	# 		self.yaxis.major_tick_out        = tickOut 
	# 		self.yaxis_majorTick.update({'tickOut' : tickOut})
	# 	if width   is not None:
	# 		self.yaxis.major_tick_line_width = width
	# 		self.yaxis_majorTick.update({'width' : width})
	# 	if color:
	# 		self.yaxis.major_tick_line_color = color
	# 		self.yaxis_majorTick.update({'color' : color})

	# 	return self.yaxis_majorTick


	# def plot_yaxis_minorTick(self, tickIn = None, tickOut = None, width = None, color  = None):
	# 	if tickIn  is not None:
	# 		self.yaxis.minor_tick_in         = tickIn 
	# 		self.yaxis_minorTick.update({'tickIn' : tickIn})
	# 	if tickOut is not None:
	# 		self.yaxis.minor_tick_out        = tickOut 
	# 		self.yaxis_minorTick.update({'tickOut' : tickOut})
	# 	if width   is not None:
	# 		self.yaxis.minor_tick_line_width = width
	# 		self.yaxis_minorTick.update({'width' : width})
	# 	if color:
	# 		self.yaxis.minor_tick_line_color = color
	# 		self.yaxis_minorTick.update({'color' : color})

	# 	return self.yaxis_minorTick	


	# def plot_axis(self, num   = None, color     = None, width     = None, 
	# 					label = None, majorTick = None, minorTick = None):
	# 	if num is not None:
	# 		axis = self.plot.axis[num]
	# 		if color:
	# 			axis.axis_line_color                  = color
	# 		if width is not None:
	# 			axis.axis_line_width                  = width
	# 		if label:
	# 			self.plot_axis_label(    num = num, **label)
	# 		if majorTick:
	# 			self.plot_axis_majorTick(num = num, **majorTick)
	# 		if minorTick:
	# 			self.plot_axis_minorTick(num = num, **minorTick)

	# 		# return axis


	# def plot_axis_label(self, num = None, text = None, color = None):
	# 	if num is not None:
	# 		axis = self.plot.axis[num]
	# 		if text is not None:
	# 			axis.axis_label                  = text
	# 		if color:
	# 			axis.axis_label_text_color       = color

	# 	axis_label = {'text'    : axis.axis_label,
	# 				  'color'   : axis.axis_label_text_color}

	# 	return axis_label

	# def plot_axis_majorTick(self, num     = None, tickIn = None, 
	# 							  tickOut = None, width  = None, color  = None):
	# 	if num is not None:
	# 		axis = self.plot.axis[num]
	# 		if tickIn  is not None:
	# 			axis.major_tick_in          = tickIn 
	# 		if tickOut is not None:
	# 			axis.major_tick_out         = tickOut 
	# 		if width   is not None:
	# 			axis.major_tick_line_width  = width
	# 		if color:
	# 			axis.major_tick_line_color  = color

	# 		axis_majorTick   = {'tickIn'  : axis.major_tick_in,
	# 							'tickOut' : axis.major_tick_out,
	# 							'width'   : axis.major_tick_line_width,
	# 							'color'   : axis.major_tick_line_color}
	# 	return axis_majorTick


	# def plot_axis_minorTick(self, num     = None, tickIn = None, 
	# 							  tickOut = None, width  = None, color  = None):
	# 	if num is not None:
	# 		axis = self.plot.axis[num]
	# 		if tickIn  is not None:
	# 			axis.minor_tick_in          = tickIn 
	# 		if tickOut is not None:
	# 			axis.minor_tick_out         = tickOut 
	# 		if width   is not None:
	# 			axis.minor_tick_line_width  = width
	# 		if color:
	# 			axis.minor_tick_line_color  = color
				
	# 		axis_minorTick   = {'tickIn'  : axis.minor_tick_in,
	# 							'tickOut' : axis.minor_tick_out,
	# 							'width'   : axis.minor_tick_line_width,
	# 							'color'   : axis.minor_tick_line_color}
	# 	return axis_minorTick 	
