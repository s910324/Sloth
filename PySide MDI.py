import sys
from PySide.QtCore import *
from PySide.QtGui import *
import matplotlib
#matplotlib.use('Qt4Agg')
import pylab

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        self.globalVal = [0]
        super(MainWindow, self).__init__(parent)
        self.mainWindow = QMainWindow()
        self.treeView = QTreeWidget(self)
        self.listView = QListWidget(self)
        self.mdiArea = QMdiArea(self)
        self.initMenuBar()
        self.initDocker()
        self.initToolBar()
        self.statusBar().showMessage('Ready')
        self.setCentralWidget(self.mdiArea)

    def initMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        viewMenu = menubar.addMenu('&View')
        plotMenu = menubar.addMenu('&Plot')
        colMenu = menubar.addMenu('&Colume')
        wksheetMenu = menubar.addMenu('&Worksheet')
        analysisMenu = menubar.addMenu('&Analysis')
        statisticsMenu = menubar.addMenu('&Statistics')
        imageMenu = menubar.addMenu('&Image')
        toolsMenu = menubar.addMenu('&Tools')
        formatMenu = menubar.addMenu('&Format')
        windowMenu = menubar.addMenu('&Window')
        helpMenu = menubar.addMenu('&Help')
        
    
    def initDocker(self):
        self.projDockWidget = QDockWidget("  ::  Projects ::", self)
        self.fileDockWidget = QDockWidget("  ::   Files   ::", self)
        self.projDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
        self.fileDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
        self.projDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea and Qt.RightDockWidgetArea)
        self.fileDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea and Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.projDockWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.fileDockWidget)
        self.projDockWidget.setWidget(self.treeView)
        self.fileDockWidget.setWidget(self.listView)
        
        
    def initToolBar(self):
        self.MainToolbar = QToolBar('Main operations') 
        self.plotbar     = QToolBar('plot options') 
        self.addToolBar( Qt.TopToolBarArea , self.MainToolbar)
        self.addToolBar( Qt.BottomToolBarArea , self.plotbar)
        
        plotAction = QAction('Exit', self)
        
        self.plotbar.addAction(plotAction)


        exitAction = QAction('Exit', self)
        openAction = QAction('Open', self)
        newwbAction = QAction('New WorkBook', self)
        plotAction = QAction('Plot', self)
        testAction = QAction('Test', self)
        
        exitAction.triggered.connect(self.CreateTableSub)
        openAction.triggered.connect(self.OpenFile)
        newwbAction.triggered.connect(self.OpenNewWorkBook)
        plotAction.triggered.connect(self.PlotData)
        testAction.triggered.connect(self.test)
        self.MainToolbar.addAction(exitAction)
        self.MainToolbar.addAction(openAction)
        self.MainToolbar.addAction(newwbAction)
        self.MainToolbar.addAction(plotAction)
        self.MainToolbar.addAction(testAction)
    
    
    def test(self):
        print 'a'
        
           
        
        
    def OpenNewProject(self):
        self.treeView.setColumnCount(2)
        projFolder =  QTreeWidgetItem(self.treeView)
        projFolder.setText(0, "Project 1")
        projItem =  QTreeWidgetItem(projFolder)
        projItem.setText(0, "Item 1")
        projItem.setText(1, "Yes")
            

    def OpenNewWorkBook(self):
        TableHandle, subWinHandle = self.CreateTableSub()
        self.globalVal[0] += 1
        SubWinTitle = "Untitled " + str(self.globalVal[0])
        subWinHandle.setWindowTitle(SubWinTitle)
        self.listView.addItem(SubWinTitle)
            
        
    def OpenFile(self):
        ReadFileArray = []
        
        FileName      = QFileDialog.getOpenFileName(self, "Open File.", "/home")
        SubWinTitle   = str(FileName[0].split('/')[-1])
        FileContainer = open(FileName[0], 'r')
        FileLines     = FileContainer.readlines()
        RowNum        = len(FileLines)
        ColNum        = 0
        
        TableHandle, subWinHandle = self.CreateTableSub()
        subWinHandle.setWindowTitle(SubWinTitle)
        self.listView.addItem(SubWinTitle)
        for i in range(RowNum):
            FileRow = (FileLines[i].strip()).split('\t')
            ReadFileArray.append(FileRow)
            if len(FileRow) > ColNum:
                ColNum = len(FileRow)
        TableHandle.setRowCount(RowNum)
        TableHandle.setColumnCount(ColNum)
        for i in range(RowNum):
            for j in range(len(ReadFileArray[i])):
                TableHandle.setItem(i, j, QTableWidgetItem(ReadFileArray[i][j]))
        FileContainer.close()
        
    def SaveFile(self):
        print 'a'
        
    def SaveAllFiles(self):
        print 'b'
        
    def CreateTableSub(self):
        
        w = QMainWindow()
        self.mdiArea.addSubWindow(w)
        tableWidget = QTableWidget()
        tableWidget.setRowCount(100)
        tableWidget.setColumnCount(3)
        w.setCentralWidget(tableWidget)
        tableWidget.setStyleSheet(" ")
        tableWidget.setStyleSheet(" QTableView::item { background-color: #fFFFFF; } QTableView { background: #E0DFE3; }")
       
        w.setAttribute(Qt.WA_DeleteOnClose)
        w.showMaximized()
        
        return tableWidget, w
        
    def PlotData(self):
        plotArrayX = []
        plotArrayY = []
        ary = []
        subWinHandle = self.mdiArea.currentSubWindow()
        tableHandle = subWinHandle.widget().centralWidget()
        b =  tableHandle.selectedItems()
        for i in range(len(b)/2):
            plotArrayX.append(float(b[i].text()))
        for i in range(len(b)/2, len(b)):
            plotArrayY.append(float(b[i].text()))
        
        for i in range(len(b)/2):
            ary.append([plotArrayX[i], plotArrayY[i]])
        
        print ary

        p = QMainWindow()
        subWinHandle = self.mdiArea.currentSubWindow()
        p.setWindowTitle('[plot]' + subWinHandle.windowTitle())
        tableHandle = subWinHandle.widget().centralWidget()
        tableHandle.setItem(1,1, QTableWidgetItem('aaa'))        
        
        self.mdiArea.addSubWindow(p)
        fig = Figure(figsize=(60,60),  facecolor=(1,1,1), edgecolor=(0,0,0))
        ax = fig.add_subplot(111)
        ax.plot(plotArrayY, plotArrayX)
        plotWidget = FigureCanvas(fig)
        p.setCentralWidget(plotWidget)
        p.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()    
    app.exec_()
    sys.exit