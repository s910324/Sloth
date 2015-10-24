import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class MLineListWidget(QWidget):
	LineVisibilityChanged = Signal(bool)
	DcFocusStateChanged   = Signal(bool)
	def __init__(self, title = 'line', parent = None):
		super(MLineListWidget, self).__init__(parent)
		self.focus_color  = QColor('#314B76')
		self.title        = title
		self.lineVisible  = True
		self.shadow       = 0
		self.visible_icon = QImage("./MaterialDesignList/MIcon/preview.svg")
		self.setFocusPolicy(Qt.StrongFocus)
		self.setDcFocus(False)
		self.show()

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		self.drawWidget(painter)
		painter.end()


	def drawWidget(self, painter):
		painter.setRenderHint(QPainter.Antialiasing)
		size = self.size()
		w    = size.width()
		h    = size.height()

		#header:
		painter.setPen(QColor(0,0,0,0))
		painter.setBrush(QColor(167, 167, 167))
		painter.drawRect(0, 0, w, h)

		#status:
		painter.setPen(QColor(0,0,0,0))
		painter.setBrush(self.focus_color)
		painter.drawRect(0, 0, 3, h-1)

		#title:
		font = QFont("Helvetica", 11, QFont.Bold)
		painter.setFont(font)
		painter.setPen(QColor('#515662'))
		painter.drawText(QRectF((45), (h / 2 - 8), 50, 50), Qt.AlignLeft, self.title)


		#icon:
		painter.setRenderHint(QPainter.Antialiasing and QPainter.SmoothPixmapTransform)

		self.lineRect    = QRectF(15,   8, 16, 16)
		self.previewRect = QRectF(w-56, 6, 20, 20)
		self.menuRect    = QRectF(w-26, 8, 15, 15)
		painter.drawImage(self.lineRect,    QImage("./MaterialDesignList/MIcon/line.svg"))
		painter.drawImage(self.previewRect, self.visible_icon)
		painter.drawImage(self.menuRect,    QImage("./MaterialDesignList/MIcon/menu.svg"))
		painter.setBrush(QColor('#2D2D2D'))

		#shadow:
		linearGradient = QLinearGradient(w/2, 0, w/2, 5)
		linearGradient.setColorAt(0.0,QColor(0,0,0,self.shadow))
		linearGradient.setColorAt(1.0,QColor(20,20,20,0))
		painter.setPen(QColor(0,0,0,0))
		painter.setBrush(linearGradient)
		painter.drawRect(0, 0, w, 5)

		#split line:
		painter.setPen(QColor('#757575'))
		painter.drawLine(15,     h, w - 60, h)

	def addShadow(self):
		self.shadow = 180
		self.update()
		

	def setDcFocus(self, focused = True):
		if focused:
			self.focus_color = QColor('#314B76')

		else:
			self.focus_color = QColor('#323232')
		self.DcFocusStateChanged.emit(focused)
		self.update()

	def setLineVisible(self, visible = True):
		if visible:
			self.visible_icon = QImage("./MaterialDesignList/MIcon/preview.svg")
		else:
			self.visible_icon = QImage("./MaterialDesignList/MIcon/No-preview.svg")
		self.lineVisible = visible
		self.LineVisibilityChanged.emit(visible)
		self.update()

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			if self.previewRect.contains(int(event.x()), int(event.y())):
				self.setLineVisible(not self.lineVisible)
				
			elif self.menuRect.contains(int(event.x()), int(event.y())):
				event.ignore()
			else:
				event.ignore()
		else:
			event.ignore()
		# 	self.ignore = True
		# 	return
				
		# self.ignore = False
		# if event.button() == Qt.RightButton:
		# 	self.menu = QMenu()
		# 	self.menu.addAction('[x] delete this Node', self.selfDestory)
		# 	self.menu.addAction('[+] add input', self.addPlug)
		# 	self.menu.popup(event.screenPos())
			
		# 	# connect(menu, SIGNAL(triggered(QAction *)),object, SLOT(triggered(QAction *)))
		# 	self.resizeMode = False
			

		# if event.button() == Qt.LeftButton:
		# 	self.moveMode = True  
		# 	self.offset = event.scenePos() - self.contentPos
		# 	for plug in self.jack:
		# 		plug.moveMode = True  
		# 		plug.offset = event.scenePos() - plug.contentPos
		# 	for source in self.drain:
		# 		source.moveMode = True  
		# 		source.offset = event.scenePos() - source.contentPos	
			
		# 	for part in self.parts:
		# 		if type(part) is not QGraphicsProxyWidget:
		# 			part.moveMode = True  
		# 			part.offset = event.scenePos() - part.contentPos
		# 		else:
		# 			part.offset = event.scenePos() - part.contentPos
				
def run():
	app = QApplication(sys.argv)
	MainWindow = MViewBoxListWidget()
	MainWindow.show()
	app.exec_()


# run()

