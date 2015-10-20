from   PySide        import QtGui
from   PySide.QtGui  import *
from   PySide.QtCore import *

class QLineNumber(QLineEdit):
	def __init__(self, parent=None):
		super(QLineNumber, self).__init__(parent)
		valid    = QtGui.QDoubleValidator()
		self.setValidator(valid)
		self.textChanged.connect(self.checkValue)

	def checkValue(self):
		try:
			value = float(self.text())
			self.setStyleSheet("border: 1px solid None;")
			return value
		except ValueError:
			self.setStyleSheet("border: 1px solid red;")
			return None