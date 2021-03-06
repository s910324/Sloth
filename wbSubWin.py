import sys
from PySide.QtCore import *
from PySide.QtGui  import *

class WorkBookWindow(QMainWindow):
	def __init__(self, parent=None):
		super(WorkBookWindow, self).__init__(parent)
		self.lock = True
		self.ID   = -1

	def getID(self):
		return self.ID
		
	def setID(self, newID):
		self.ID = newID

	def closeEvent(self, event):
		if self.lock:
			self.showMinimized()
			event.ignore()
			
		else:
			event.accept()
			self.showMaximized()

	def unlock(self) :
		self.lock = False

	def lock(self) :
		self.lock = True

if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = WorkBookWindow()
	frame.showMaximized()    
	app.exec_()
	sys.exit
