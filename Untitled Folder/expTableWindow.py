import sys
from PySide.QtCore import *
from PySide.QtGui import *
import os

class TableWidgetCustom(QMainWindow):
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)
        self.deletable = False
        self.systemTrayIcon = QSystemTrayIcon(self)
        self.systemTrayIcon.setIcon(QIcon.fromTheme("face-smile"))
        self.systemTrayIcon.setVisible(True)
        self.systemTrayIcon.activated.connect(self.on_systemTrayIcon_activated)

    #     self.button = QPushButton('lock / unlock')
    #     self.button.clicked.connect(self.locker)
    #     self.setCentralWidget(self.button)
    # def locker(self):
    #     self.deletable = True

    def on_systemTrayIcon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                self.close()
                return
        super(TableWidgetCustom, self).changeEvent(event)

    def closeEvent(self, event):
        if self.deletable == True:
            event.accept()
        else:
            event.ignore()
            self.hide()
            self.systemTrayIcon.showMessage('Running', 'Running in the background.')


# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     app.setApplicationName('MyWindow')
#     main = TableWidgetCustom()
#     main.show()
#     sys.exit(app.exec_())