import sys
from PySide.QtCore import *
from PySide.QtGui  import *

class WorkBookWindow(QMainWindow):
	def __init__(self, parent=None):
		super(WorkBookWindow, self).__init__(parent)
		self.lock = True
		self.ID   = -1

	def recurrence(self):
		self.ID -= 1
		return self.ID

	def closeEvent(self, event):
		if not self.lock:
			self.showMinimized()
			event.ignore()

		else:
			self.showMaximized()
			return self.closeChecker(event)

	def closeChecker(self, event):
		closeChk = QMessageBox()
		closeChk.setText("Close Confirm")
		closeChk.setInformativeText("Close an unsaved frame will destory data/plotin this frame.")

		yes    = closeChk.addButton( self.tr("              Close Frame           "), QMessageBox.ActionRole )
		no     = closeChk.addButton( self.tr("               minimize             "), QMessageBox.ActionRole )
		cancle = closeChk.addButton( self.tr("                Cancle              "), QMessageBox.ActionRole )

		closeChk.setDefaultButton(cancle)
		closeChk.exec_()

		if closeChk.clickedButton()   == yes:
			return True
			event.accept()


		elif closeChk.clickedButton() == no:
			self.showMinimized()
			event.ignore()
			return False

		else:
			event.ignore()
			return False

if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = WorkBookWindow()
	frame.showMaximized()    
	app.exec_()
	sys.exit
