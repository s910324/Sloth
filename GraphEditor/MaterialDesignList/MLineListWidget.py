import sys
from PySide        import QtGui
from PySide.QtGui  import *
from PySide.QtCore import *

class MLineListWidget(QWidget):
	def __init__(self, parent = None):
		super(MLineListWidget, self).__init__(parent)
		self.focus_color = QColor('#314B76')

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

		painter.setPen(QColor(0,0,0,0))

		painter.setBrush(self.focus_color)
		painter.drawRect(3, 2, 3, h-4)



		#title:
		font = QFont("Helvetica", 11, QFont.Bold)
		painter.setFont(font)
		painter.setPen(QColor('#515662'))
		painter.drawText(QRectF((45), (h / 2 - 8), 50, 50), Qt.AlignLeft, 'Text')

		painter.drawLine(15,     h, w - 60, h)
		painter.setPen(Qt.DotLine)
		painter.drawLine(w - 60, h, w,      h)

		painter.setRenderHint(QPainter.Antialiasing and QPainter.SmoothPixmapTransform)

		self.lineRect    = QRectF(15,   8, 16, 16)
		self.previewRect = QRectF(w-56, 6, 20, 20)
		self.menuRect    = QRectF(w-26, 8, 15, 15)
		painter.drawImage(self.lineRect,    QImage("./MaterialDesignList/MIcon/line.svg"))
		painter.drawImage(self.previewRect, QImage("./MaterialDesignList/MIcon/preview.svg"))
		painter.drawImage(self.menuRect,    QImage("./MaterialDesignList/MIcon/menu.svg"))

		

	def setDcFocus(self, focused = True):
		if focused:
			self.focus_color = QColor('#314B76')

		else:
			self.focus_color = QColor('#323232')

		self.update()

	def setLineVisible(self, visible = True):
		if focused:
			self.visible_icon = QImage("./MaterialDesignList/MIcon/preview.svg")

		else:
			self.visible_icon = QImage("./MaterialDesignList/MIcon/No-preview.svg")

		self.update()

	def mousePressEvent(self, event):

		# rect = self.contentSceneRect()
		# if not rect.contains(int(event.scenePos().x()), int(event.scenePos().y())):
		# 	#ungrab mouse
		# 	event.ignore()
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

