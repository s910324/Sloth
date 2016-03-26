import sys
import types
from   PySide.QtGui       import *
from   PySide.QtCore      import *


class MHLine(QHBoxLayout):
	def __init__(self, *args):
		super(MHLine, self).__init__()
		hline = QFrame()
		hline.setFrameStyle( QFrame.HLine  |  QFrame.Plain )
		hline.setFrameShadow( QFrame.Sunken )
		hline.setLineWidth(1)
		self.addSpacing(5)
		self.addWidget(hline)
		self.addSpacing(5)
		self.setContentsMargins(0,15,0,15)


class MVLine(QVBoxLayout):
	def __init__(self, *args):
		super(MVLine, self).__init__()

		vline = QFrame()
		vline.setFrameStyle( QFrame.VLine  |  QFrame.Plain )
		vline.setFrameShadow( QFrame.Sunken )
		vline.setLineWidth(1)
		self.addSpacing(15)
		self.addWidget(vline)
		self.addSpacing(15)


class MHBoxLayout(QHBoxLayout):
	def __init__(self, *args):
		super(MHBoxLayout, self).__init__()
		if args:
			self.addWidgets(*args)

	def addWidgets(self, *args):
		for widget in args:
			try:
				if widget == 0 :
					self.addStretch()
				elif type(widget) == types.IntType:
					self.addSpacing(widget)
				else:
					self.addWidget(widget)
			except TypeError:
				self.addLayout(widget)
		return self

	def addLayouts(self, *args):
		self.addWidgets(*args)
		return self

	def setFixedWidth(self, width = None):
		if width:
			for widget in [ self.itemAt(i).widget() for i in xrange(self.count())]:
				try:
					widget.setFixedWidth(width)
				except AttributeError:
					pass
		return self

	def setFixedHeight(self, Height = None):
		if Height:
			for widget in [ self.itemAt(i).widget() for i in xrange(self.count())]:
				try:
					widget.setFixedHeight(Height)
				except AttributeError:
					pass
		return self

	def setAlignment(self, Alignment = None):
		if Alignment:
			for widget in [ self.itemAt(i).widget() for i in xrange(self.count())]:
				try:
					widget.setAlignment(Alignment)
				except AttributeError:
					pass

		return self			
			
class MVBoxLayout(QVBoxLayout):
	def __init__(self, *args):
		super(MVBoxLayout, self).__init__()
		if args:
			self.addWidgets(*args)

	def addWidgets(self, *args):
		for widget in args:
			try:
				if widget == 0 :
					self.addStretch()
				elif type(widget) == types.IntType:
					self.addSpacing(widget)
				else:
					self.addWidget(widget)
			except TypeError:
				self.addLayout(widget)
		return self

	def addLayouts(self, *args):
		self.addWidgets(*args)
		return self

	def setFixedWidth(self, width = None):
		if width:
			for widget in [ self.itemAt(i).widget() for i in xrange(self.count())]:
				try:
					widget.setFixedWidth(width)
				except AttributeError:
					pass
		return self

	def setFixedHeight(self, Height = None):
		if width:
			for widget in [ self.itemAt(i).widget() for i in xrange(self.count())]:
				try:
					widget.setFixedHeight(Height)
				except AttributeError:
					pass
		return self

	def setAlignment(self, Alignment = None):
		if Alignment:
			for widget in [ self.itemAt(i).widget() for i in xrange(self.count())]:
				try:
					widget.setAlignment(Alignment)
				except AttributeError:
					print "TypeError"

		return self	
	

class MGroupBox(QWidget):
	def __init__(self, title = None, parent = None):
		super(MGroupBox, self).__init__(parent)	
		
		self.MTitle = MGroupTitle(title)
		self.Midget = QWidget()
		self.v1     = MVBoxLayout(self.MTitle, self.Midget, 25)
		self.v2     = QVBoxLayout()
		self.h1     = MHBoxLayout(30, self.v2)
		


		self.Midget.setLayout(self.h1)

		self.v1.setSpacing(0)
		self.v1.setContentsMargins(0,0,0,0)
		self.setContentsMargins(0,0,0,0)
		self.setLayout(self.v1)
		self.MTitle.statChanged.connect(self.changeVisibility)

	def changeVisibility(self, stat):
		self.Midget.setVisible(stat)	

	def addWidget(self, widget = None):
		try:
			self.v2.addWidget(widget)
		except:
			self.v2.addLayout(widget)

	def addLayout(self, widget = None):	
		self.addWidget(widget)

		return self



class MGroupTitle(QWidget):
	statChanged = Signal(bool)
	def __init__(self, title = None, parent = None):
		super(MGroupTitle, self).__init__(parent)	
		self.setFixedHeight(20)

		self.setContentsMargins(0,0,0,0)
		self.title = title
		self.stat  = True
		m = QHBoxLayout()
		m.setContentsMargins(0,0,0,0)
		m.setSpacing(0)
		l = QLabel(title)
		l.setFont(QFont('Helvetica [Cronyx]', 10, QFont.Bold))
		m.addSpacing(35)
		m.addWidget(l)
		self.setLayout(m)
		

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		self.drawWidget(painter)
		painter.end() 

	def drawWidget(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		w, h     = self.size().width(), self.size().height()-2
		x, y     = self.pos().x(), self.pos().y()+1
		self.ctrlRect = QRectF(x+3, y+2, h-4, h-4)

		pen = QPen(QColor("#353535"))
		br  = QBrush(QColor("#353535"))
		br.setStyle(Qt.Dense4Pattern)
		pen.setWidthF(0.1)
		painter.setPen(pen)
		painter.setBrush(br)
		painter.drawEllipse(self.ctrlRect)
		painter.drawRect(QRect(x+25, y, w, h))


		
		pen = QPen()
		pen.setColor(QColor("#E2065F"))
		painter.setPen(pen)	
		painter.setFont(QFont('Helvetica [Cronyx]', 12, QFont.Bold))
		self.statTXT = "-" if self.stat else "+"
		painter.drawText(self.ctrlRect, Qt.AlignCenter, self.statTXT )
		pen.setColor(QColor("#CCC"))
		painter.setFont(QFont('Helvetica [Cronyx]', 10, QFont.Bold))
		painter.setPen(pen)	
		# painter.drawText(QRect(x+30, y, w, h), Qt.AlignLeft|Qt.AlignVCenter, self.title)


	def mousePressEvent(self, event):
		if self.ctrlRect.contains(event.pos()):
			self.stat = not self.stat
			self.statChanged.emit(self.stat)
			self.update()
