import sys
import numpy as np
import string
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtGui import QFont as QFont
import matplotlib
#matplotlib.use('Qt4Agg')
import pylab
import types
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        self.tabIDCounter = -1
        self.tabColCounter = []
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
        addColAction = QAction('Add Column', self)
        addRowAction = QAction('Add Row', self)
        rmvColAction = QAction('remove Column', self)
        rmvRowAction = QAction('remove Row', self)        
        setXAction = QAction('Set As X', self)
        setYAction = QAction('Set As Y', self)
        setZAction = QAction('Set As Z', self)
        
        exitAction.triggered.connect(self.CreateTableSub)
        openAction.triggered.connect(self.OpenFile)
        newwbAction.triggered.connect(self.OpenNewWorkBook)
        plotAction.triggered.connect(self.PlotData)
        testAction.triggered.connect(self.test)
        addColAction.triggered.connect(self.addCol)
        addRowAction.triggered.connect(self.addRow)
        rmvColAction.triggered.connect(self.rmvCol)
        rmvRowAction.triggered.connect(self.rmvRow)        
        setXAction.triggered.connect(self.setX)
        setYAction.triggered.connect(self.setY)
        setZAction.triggered.connect(self.setZ)
        
        self.MainToolbar.addAction(exitAction)
        self.MainToolbar.addAction(openAction)
        self.MainToolbar.addAction(newwbAction)
        self.MainToolbar.addAction(plotAction)
        self.MainToolbar.addAction(testAction)
        self.MainToolbar.addAction(addColAction)
        self.MainToolbar.addAction(addRowAction)
        self.MainToolbar.addAction(rmvColAction)
        self.MainToolbar.addAction(rmvRowAction)
        self.MainToolbar.addAction(setXAction)
        self.MainToolbar.addAction(setYAction)
        self.MainToolbar.addAction(setZAction)
    
    
    def test(self):
        print self.tabColCounter
        print self.tabIDCounter
        wList = self.mdiArea.subWindowList()
        for i in range( len( wList )):
            print wList[i].widget().statusBar().showMessage('np' )
        
#        selectAry    = []
#        subWinHandle = self.mdiArea.currentSubWindow()
#        tableHandle  = subWinHandle.widget().centralWidget()
#        
#        for i in range( len(tableHandle.selectedRanges())):
#            leftCol  = tableHandle.selectedRanges()[i].topRow()
#            colCount = tableHandle.selectedRanges()[i].rowCount()
#            for j in range( leftCol, leftCol + colCount ):
#                selectAry.append( j )
#        print selectAry
    

        
    
    def addCol(self):
        try:
            subWinHandle = self.mdiArea.currentSubWindow()
            tableHandle  = subWinHandle.widget().centralWidget()
            currentCol   = tableHandle.currentColumn()
            tabID        = int(subWinHandle.widget().statusBar().currentMessage().split('#')[1])
            alfabat      = []
            atoz         = '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if currentCol == -1:
                currentCol = self.tabColCounter[tabID]-1
                
            tableHandle.insertColumn(currentCol + 1)
            self.tabColCounter[tabID] += 1

            headerLable = 'Y('
            root = self.tabColCounter[tabID]
            while( root != 0):
                if root%26 != 0:
                    alfabat.append(root%26)
                    root = root/26
                else:
                    alfabat.append(26)
                    root = (root/26) -1

            for i in range(len(alfabat)):
                alfabat[i] = atoz[alfabat[i]]
            for i in range(len(alfabat)-1, -1, -1):
                headerLable += alfabat[i]
            headerLable += ')'  
            print 'Tab #' + str(tabID) + ' append column #' + str(headerLable)
            tableHandle.setHorizontalHeaderItem(currentCol + 1, QTableWidgetItem(headerLable))
            for i in range(3):
                headerItem = QTableWidgetItem('')
                headerItem.setBackground(QColor('#0066cc'))
                headerItem.setForeground(QColor('#ffffff'))
                headerFont = QFont("Times", 8, QFont.Normal)
                headerItem.setFont(headerFont)
                tableHandle.setItem(i, currentCol + 1, headerItem)
        except AttributeError:
            print 'No active/valid workbook for column appending.'
        
        
    def addRow(self):
        try:
            subWinHandle = self.mdiArea.currentSubWindow()
            tableHandle  = subWinHandle.widget().centralWidget()
            tabID        = int(subWinHandle.widget().statusBar().currentMessage().split('#')[1])
            if tableHandle.currentRow() > 2:
                tableHandle.insertRow(tableHandle.currentRow())
                print 'Tab #' + str(tabID) + ' append row #' + str(tableHandle.currentRow())
                
        except AttributeError:
            print 'No active/valid workbook for  row appending.'
    
    def rmvCol(self):
        try: 
            subWinHandle = self.mdiArea.currentSubWindow()
            tableHandle  = subWinHandle.widget().centralWidget()
            tabID        = int(subWinHandle.widget().statusBar().currentMessage().split('#')[1])
            selectAry    = []

            for i in range( len(tableHandle.selectedRanges())):
                leftCol  = tableHandle.selectedRanges()[i].leftColumn()
                colCount = tableHandle.selectedRanges()[i].columnCount()
                for j in range( leftCol, leftCol + colCount ):
                    selectAry.append( j )

            for i in range( len ( selectAry )):
                tableHandle.removeColumn(selectAry[i] - i)
                self.tabColCounter[tabID] -= 1
                print 'Tab #' + str(tabID) + ' remove column #' + str(selectAry[i])
                
        except AttributeError:
            print 'No active/valid workbook for column removing.'

    def rmvRow(self):
        try:
            subWinHandle = self.mdiArea.currentSubWindow()
            tableHandle  = subWinHandle.widget().centralWidget()
            tabID        = int(subWinHandle.widget().statusBar().currentMessage().split('#')[1])
            selectAry    = []

            for i in range( len(tableHandle.selectedRanges())):
                topRow  = tableHandle.selectedRanges()[i].topRow()
                rowCount = tableHandle.selectedRanges()[i].rowCount()
                for j in range( topRow, topRow + rowCount ):
                    selectAry.append( j )

            for i in range( len ( selectAry )):
                if (selectAry[i] - i) > 2:
                    tableHandle.removeRow(selectAry[i] - i)
                    print 'Tab #' + str(tabID) + ' remove row #' + str(selectAry[i])
                    
        except AttributeError:
            print 'No active/valid workbook for row removing.'
    
    
    def setX(self):
        print'a'

    def setY(self):
        print 'a'

    def setZ(self):
        print 'a'
           
        
        
    def OpenNewProject(self):
        self.treeView.setColumnCount(2)
        projFolder =  QTreeWidgetItem(self.treeView)
        projFolder.setText(0, "Project 1")
        projItem =  QTreeWidgetItem(projFolder)
        projItem.setText(0, "Item 1")
        projItem.setText(1, "Yes")
            

    def OpenNewWorkBook(self):
        tableHandle, subWinHandle, tabID = self.CreateTableSub()
        subWinTitle = "Untitled " + str(tabID)
        subWinHandle.setWindowTitle(subWinTitle)
        self.listView.addItem(subWinTitle)
        tableHandle.setRowCount(200)
        for i in range(3):
            self.addCol()
        #self.tabColCounter[tabID] = 3
#        for i in range(3):
#            for j in range(3):
#                headerItem = QTableWidgetItem('')
#                headerItem.setBackground(QColor('#0066cc'))
#                headerItem.setForeground(QColor('#ffffff'))
#                headerFont = QFont("Times", 8, QFont.Normal)
#                headerItem.setFont(headerFont)
#                tableHandle.setItem(i, j, headerItem)
##################################
#        msgCounter = ''
#        for i in range( len( str( colCounter ))):
#            msgCounter += string.ascii_uppercase[int( str(colCounter)[i])]
                #################
        
            
        
    def OpenFile(self):
        ReadFileArray = []
        
        FileName      = QFileDialog.getOpenFileName(self, "Open File.", "/home")
        SubWinTitle   = str(FileName[0].split('/')[-1])
        FileContainer = open(FileName[0], 'r')
        FileLines     = FileContainer.readlines()
        RowNum        = len(FileLines)
        ColNum        = 0
        
        TableHandle, subWinHandle, tabID = self.CreateTableSub()
        subWinHandle.setWindowTitle(SubWinTitle)
        self.listView.addItem(SubWinTitle)
        for i in range(RowNum):
            FileRow = (FileLines[i].strip()).split('\t')
            ReadFileArray.append(FileRow)
            if len(FileRow) > ColNum:
                ColNum = len(FileRow)
        TableHandle.setRowCount(RowNum)
        for i in range(ColNum):
            self.addCol()

        for i in range(3):
            for j in range(ColNum):
                if j < len(ReadFileArray[i]):
                    headerItem = QTableWidgetItem(ReadFileArray[i][j])
                else:
                    headerItem = QTableWidgetItem('')
                headerItem.setBackground(QColor('#0066cc'))
                headerItem.setForeground(QColor('#ffffff'))
                headerFont = QFont("Times", 8, QFont.Normal)
                headerItem.setFont(headerFont)
                TableHandle.setItem(i, j, headerItem)
        for i in range(3, RowNum):
            for j in range(len(ReadFileArray[i])):
                TableHandle.setItem(i, j, QTableWidgetItem(ReadFileArray[i][j]))
        FileContainer.close()
        
    def SaveFile(self):
        print 'a'
        
    def SaveAllFiles(self):
        print 'b'
        
    def CreateTableSub(self):
        self.tabIDCounter += 1
        tabID = self.tabIDCounter
        w = QMainWindow()
        self.mdiArea.addSubWindow(w)
        tableWidget = QTableWidget()
        w.setCentralWidget(tableWidget)
       #tableWidget.setStyleSheet(" ")
       #tableWidget.setStyleSheet(" QTableView::item { background-color: #FFFFFF;selection-background-color: red; } QTableView { background: #E0DFE3;} ")
        w.setAttribute(Qt.WA_DeleteOnClose)
        w.setMinimumSize(QSize(250,250))
        w.statusBar().showMessage('Tab #' + str(tabID) )
        self.tabColCounter.append(0)
        w.showMaximized()
        return tableWidget, w, tabID
        
    def PlotData(self):
        try:
            plotArrayX = []
            plotArrayY = []
            coordinates = []
            subWinHandle = self.mdiArea.currentSubWindow()
            tableHandle = subWinHandle.widget().centralWidget()
            selectedOnes = tableHandle.selectedRanges()
                    
            p = QMainWindow()
            subWinHandle = self.mdiArea.currentSubWindow()
            p.setWindowTitle('[plot]' + subWinHandle.windowTitle())
            tableHandle = subWinHandle.widget().centralWidget()
            self.mdiArea.addSubWindow(p)
            
            selectAry = []
            for i in range( len(tableHandle.selectedRanges())):
                leftCol  = tableHandle.selectedRanges()[i].leftColumn()
                colCount = tableHandle.selectedRanges()[i].columnCount()
                for j in range( leftCol, leftCol + colCount ):
                    selectAry.append( j )
            print selectAry
    
            for j in range(2, tableHandle.rowCount()):
                itemX = tableHandle.item(j,0)
                itemY = tableHandle.item(j,3)
                if ((type(itemX) == types.NoneType) + (type(itemY) == types.NoneType)) == 0:
                    try:
                        [ItemXChk, ItemYChk] = [float(itemX.text()), float(itemY.text())]
                        plotArrayX.append(float(itemX.text()))
                        plotArrayY.append(float(itemY.text()))
                    except ValueError:
                        print 'ValueError at: row# '       + str(j+1)
                    except TypeError:
                        print 'TypeError at: row# '        + str(j+1)
                    except AttributeError:
                        print 'AttributionError at: row# ' + str(j+1)
            plotArrayX = np.array(plotArrayX)
            plotArrayY = np.array(plotArrayY)
    
    
            fig = Figure(figsize=(60,60),  facecolor=(1,1,1), edgecolor=(0,0,0))
            ax = fig.add_subplot(111)
            ax.plot(plotArrayX, plotArrayY)
            plotWidget = FigureCanvas(fig)
            p.setCentralWidget(plotWidget)
            p.showMaximized()
        except AttributeError:
            print 'No active/valid workbook for data plotting.'
  
  ############better faster, stupider######################################################
#        for i in range(len(tableHandle.selectedIndexes())):
#            coordinate = ((str(tableHandle.selectedIndexes()[i]).split('<PySide.QtCore.QModelIndex('))[1].split('QTableModel')[0]).split(',')
#            coordinate = [int(coordinate[0]), int(coordinate[1])]
#            coordinates.append( coordinate )
#        
#        cluster = []
#        group = []
#        length = len(coordinates)
#        while ( length != 0 ):
#            if len(cluster) == 0:
#                cluster.append(coordinates[0])
#                coordinates.pop(0)
#            else:
#                if cluster[0][1] == coordinates[0][1]:
#                    cluster.append(coordinates[0])
#                    coordinates.pop(0)
#                else:
#                    group.append(cluster)
#                    cluster = []
#            length = len(coordinates)
#        group.append(cluster)   
#        plotArrayX = group[0]
#        plotArrayY = group[1]
#        for i in range(len(plotArrayX)):
#            plotArrayX[i] = float(tableHandle.item(plotArrayX[i][0],plotArrayX[i][1]).text())
#        for i in range(len(plotArrayY)):
#            plotArrayY[i] = float(tableHandle.item(plotArrayY[i][0],plotArrayY[i][1]).text())
#        
#        p = QMainWindow()
#        subWinHandle = self.mdiArea.currentSubWindow()
#        p.setWindowTitle('[plot]' + subWinHandle.windowTitle())
#        tableHandle = subWinHandle.widget().centralWidget()
#
#        self.mdiArea.addSubWindow(p)
#        fig = Figure(figsize=(60,60),  facecolor=(1,1,1), edgecolor=(0,0,0))
#        ax = fig.add_subplot(111)
#        ax.plot(plotArrayX, plotArrayY)
#        plotWidget = FigureCanvas(fig)
#        p.setCentralWidget(plotWidget)
#        p.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()    
    app.exec_()
    sys.exit
    
    
    
"""
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.1);
y1 = np.sin(x)
y2 = np.cos(x)
plt.plot(x, y1)
plt.plot(x, y2)
plt.show()

"""