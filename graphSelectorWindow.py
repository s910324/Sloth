import sys
from   PySide.QtGui  import *
from   PySide.QtCore import *


class graphSelector(QMainWindow):
	def __init__(self, parent=None):
		super(graphSelector, self).__init__(parent)
		self.resize(450, 650)
		

def run():
	app = QApplication(sys.argv)
	MainWindow = graphSelector()
	MainWindow.show()
	app.exec_()
run()