import sys
import numpy as np
from PySide.QtCore import *
from PySide.QtGui  import *
from PySide.QtGui  import QFont as QFont
#import matplotlib
#matplotlib.use('Qt4Agg')
#import pylab
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import types

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        self.tabIDCounter = -1
        self.tabColCounter = []
        self.globalVal = [0]
        super(MainWindow, self).__init__(parent)
        self.mainWindow = QMainWindow()
        self.prjTreeView = QTreeWidget(self)
        self.winTreeView = QTreeWidget(self)
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
        self.projDockWidget.setWidget(self.prjTreeView)
        self.fileDockWidget.setWidget(self.winTreeView)
        self.initWinTree()
        
        
    def initToolBar(self):
        self.MainToolbar = QToolBar('Main operations') 
        self.plotbar     = QToolBar('plot options') 
        self.addToolBar( Qt.TopToolBarArea , self.MainToolbar)
        self.addToolBar( Qt.BottomToolBarArea , self.plotbar)
        
        nextAction = QAction('Exit', self)
        self.plotbar.addAction(nextAction)
        nextAction.triggered.connect(self.test2)        
        
        exitAction = QAction('Exit', self)
        openPjAction = QAction('New Project', self)
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
        openPjAction.triggered.connect(self.OpenNewProject)
        openAction.triggered.connect(self.OpenFile)
        newwbAction.triggered.connect(self.OpenNewWorkBook)
        plotAction.triggered.connect(self.PlotData)
        testAction.triggered.connect(self.test)
        addColAction.triggered.connect(self.addCol)
        addRowAction.triggered.connect(self.addRow)
        rmvColAction.triggered.connect(self.rmvCol)
        rmvRowAction.triggered.connect(self.rmvRow)        
        setXAction.triggered.connect(lambda axis = 0 : self.setAxis(axis))
        setYAction.triggered.connect(lambda axis = 1 : self.setAxis(axis))
        setZAction.triggered.connect(lambda axis = 2 : self.setAxis(axis))
        
        
        self.MainToolbar.addAction(exitAction)
        self.MainToolbar.addAction(openPjAction)
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
        
    def initWinTree(self):
        self.winTreeView.setColumnCount(3)

        self.winTreeView.setColumnWidth(0, 90)
        self.winTreeView.setColumnWidth(1, 90)
        self.winTreeView.setColumnWidth(2, 25)
        self.winTreeView.isSortingEnabled()
        self.winTreeView.setHeaderHidden(False)
            
    
#    def test(self):
#        print 'a'
#        subWinHandle = self.mdiArea.currentSubWindow()
#        tableHandle  = subWinHandle.widget().centralWidget()
#        tableHandle.close()
#        selectAry = []
#        axisAry   = []
#        clusters  = []
#        cnt = 0
#        for i in tableHandle.selectedRanges():
#            print i
#        
#        for i in range( len(tableHandle.selectedRanges())):
#            leftCol  = tableHandle.selectedRanges()[i].leftColumn()
#            colCount = tableHandle.selectedRanges()[i].columnCount()
#            for currentCol in range( leftCol, leftCol + colCount ):
#                selectAry.append( currentCol )
#                if (str(tableHandle.horizontalHeaderItem(currentCol).text())[0]) == 'X':
#                    axisAry.append(cnt)
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
    
    
    def setAxis(self, axis):
        axisAry      = [ 'X', 'Y', 'Z' ]
        try:
            subWinHandle = self.mdiArea.currentSubWindow()
            tableHandle  = subWinHandle.widget().centralWidget()
            selectAry    = []
            for i in range( len(tableHandle.selectedRanges())):
                leftCol  = tableHandle.selectedRanges()[i].leftColumn()
                colCount = tableHandle.selectedRanges()[i].columnCount()
                for j in range( leftCol, leftCol + colCount ):
                    selectAry.append( j )
            for currentCol in selectAry:
                headerLable = axisAry[axis]
                headerLable += str(tableHandle.horizontalHeaderItem(currentCol).text())[1:]
                tableHandle.setHorizontalHeaderItem(currentCol, QTableWidgetItem(headerLable))
        except AttributeError:
            print 'No active/valid workbook for set as %s operation.' % axisAry[axis]

        
        
    def OpenNewProject(self):
        self.prjTreeView.setColumnCount(2)
        projFolder =  QTreeWidgetItem(self.prjTreeView)
        projFolder.setText(0, "Project 1")
        projItem =  QTreeWidgetItem(projFolder)
        projItem.setText(0, "Item 1")
        projItem.setText(1, "Yes")
    

    
    def AddWinTreeItem(self, subWinTitle, wintype, tabID):
        
        subTreeItem =  QTreeWidgetItem(self.winTreeView)
        subTreeItem.setText(0, subWinTitle)
        subTreeItem.setText(1, wintype)
        subTreeItem.setText(2, str(tabID))
        self.winTreeView.itemDoubleClicked.connect(lambda ID=tabID: self.RaiseSubWin(ID))

    def RaiseSubWin(self, tabID):
        tabID = tabID.text(2)
        wList = self.mdiArea.subWindowList()
        self.mdiArea.setActiveSubWindow(wList[int(tabID)])
        print 'Activating subwindow #' + tabID
                

    def OpenNewWorkBook(self):
        tableHandle, subWinHandle, tabID = self.CreateTableSub()
        subWinTitle = "Untitled " + str(tabID)
        subWinHandle.setWindowTitle(subWinTitle)
        self.AddWinTreeItem(subWinTitle, 'Work Book', tabID)
        tableHandle.setRowCount(200)
        for i in range(3):
            self.addCol()


    def OpenFile(self):
        ReadFileArray = []
        
        FileName      = QFileDialog.getOpenFileName(self, "Open File.", "/home")
        subWinTitle   = str(FileName[0].split('/')[-1])
        FileContainer = open(FileName[0], 'r')
        FileLines     = FileContainer.readlines()
        RowNum        = len(FileLines)
        ColNum        = 0
        
        TableHandle, subWinHandle, tabID = self.CreateTableSub()
        subWinHandle.setWindowTitle(subWinTitle)
        self.AddWinTreeItem(subWinTitle, 'Work Book', tabID)
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
            subWinHandle = self.mdiArea.currentSubWindow()
            tableHandle  = subWinHandle.widget().centralWidget()
            p = QMainWindow()
            subWinTitle = '[plot]' + subWinHandle.windowTitle()
            p.setWindowTitle(subWinTitle)
            self.mdiArea.addSubWindow(p)

            selectAry = []
            axisAry   = []
            clusters  = []
            cnt = 0
            for i in range( len(tableHandle.selectedRanges())):
                leftCol  = tableHandle.selectedRanges()[i].leftColumn()
                colCount = tableHandle.selectedRanges()[i].columnCount()
                for currentCol in range( leftCol, leftCol + colCount ):
                    selectAry.append( currentCol )
                    if (str(tableHandle.horizontalHeaderItem(currentCol).text())[0]) == 'X':
                        axisAry.append(cnt)
                    cnt += 1

            for i in range(len(axisAry)):
                try:
                    clusters.append( selectAry[axisAry[i]  : axisAry[i+1]] )        
                except IndexError:
                    clusters.append( selectAry[axisAry[-1] :             ] )
            
            fig = Figure(figsize=(60,60),  facecolor=(1,1,1), edgecolor=(0,0,0))
            ax = fig.add_subplot(111)

            for k in clusters:
                for i in k[1:]:
                    plotArrayX = []
                    plotArrayY = []
                    for j in range(2, tableHandle.rowCount()):
                        itemX = tableHandle.item(j,k[0])
                        itemY = tableHandle.item(j,i)
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
                    ax.plot(plotArrayX, plotArrayY)
      
            plotWidget = FigureCanvas(fig)

            p.setCentralWidget(plotWidget)
            p.setMinimumSize(QSize(250,250))
            p.showMaximized()
            self.tabIDCounter += 1
            tabID = self.tabIDCounter
            self.tabColCounter.append(-1)
            self.AddWinTreeItem(subWinTitle, 'Plot', tabID)
        except AttributeError:
            print 'No active/valid workbook for data plotting.'
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply ==  QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  
            
    def test(self):
        try:
            subWinHandle = self.mdiArea.currentSubWindow()
            tabID        = int(subWinHandle.widget().statusBar().currentMessage().split('#')[1])
            self.a =ScriptSetVal(tabID, subWinHandle)
        except AttributeError:
            print 'No active/valid workbook for script setting.'   
    def test2(self):
        print a

    def ScriptSetVal(self):
        w = QMainWindow()
        t = QTextEdit()
        self.mdiArea.addSubWindow(w)
        w.setCentralWidget(t)
        w.setAttribute(Qt.WA_DeleteOnClose)
        w.setMinimumSize(QSize(250,250))
        w.setGeometry(QRect(200, 200, 500, 500))
        
        w.show()
        
        
class ScriptSetVal(QMainWindow):
    def __init__(self, tabID, subWinHandle, parent=None):
        super(ScriptSetVal,  self).__init__(parent)
        self.tabID = tabID    
        self.subWinHandle = subWinHandle
        self.tableHandle  = subWinHandle.widget().centralWidget()
        self.initUI()
        self.initToolBar()
        self.initDocker()
        
    def initUI(self): 
        self.t = QTextEdit()
        self.initFont()
        self.setCentralWidget(self.t)
        self.setGeometry(QRect(200, 200, 410, 610))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.show()
    
    def initToolBar(self):
        self.scriptbar    = QToolBar('plot options') 
        self.addToolBar( Qt.BottomToolBarArea , self.scriptbar)
        scriptAction = QAction('set script', self)
        self.scriptbar.addAction(scriptAction)
        scriptAction.triggered.connect(self.RelectRng)

    def initFont(self):
        self.tabStop = 4
        self.font = QFont('Courier')
        self.metrics = QFontMetrics(self.font)
        self.t.setTabStopWidth(self.tabStop * self.metrics.width(' '));
        self.font.setStyleHint(QFont.Monospace);
        self.font.setFixedPitch(True);
        self.font.setPointSize(12)
        self.p = self.t.palette()
        self.p.setColor(QPalette.Base, QColor(0, 0, 0))
        self.p.setColor(QPalette.Text, QColor(255, 255, 255))
        self.t.setPalette(self.p)
        self.t.setFont(self.font)
        self.highlighter = Highlighter(self.t.document())

    def initDocker(self):
        self.elog = QTextEdit()
        self.elogDockWidget = QDockWidget("  ::  error log ::", self)
        self.elogDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
        self.elogDockWidget.setAllowedAreas(Qt.TopDockWidgetArea and Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.elogDockWidget)
        self.elogDockWidget.setWidget(self.elog)
        self.p = self.elog.palette()
        self.p.setColor(QPalette.Base, QColor(0, 0, 0))
        self.p.setColor(QPalette.Text, QColor(255, 0, 0))
        self.elog.setPalette(self.p)
        self.elog.setReadOnly(True)

          

    def RelectRng(self):
        try:
            self.selectAry = []
            if len(self.tableHandle.selectedRanges()) != 0:
                for i in range( len(self.tableHandle.selectedRanges())):
                    self.leftCol  = self.tableHandle.selectedRanges()[i].leftColumn()
                    self.colCount = self.tableHandle.selectedRanges()[i].columnCount()
                    for currentCol in range( self.leftCol, self.leftCol + self.colCount ):
                        self.selectAry.append( currentCol )
                self.leftCol  = self.tableHandle.selectedRanges()[0].leftColumn()
                self.colCount = self.tableHandle.selectedRanges()[0].columnCount()
                self.topRow   = self.tableHandle.selectedRanges()[0].topRow()
                self.rowCount = self.tableHandle.selectedRanges()[0].rowCount()
                
                rows = []
                cols = []
                for i in range(self.topRow,  self.topRow  + self.rowCount, 1):
                    rows.append(i)
                for i in range(self.leftCol, self.leftCol + self.colCount, 1):
                    cols.append(i)

                try:
                    exec(self.t.toPlainText())
                except Exception, e:
                    self.elog.moveCursor(QTextCursor.End)
                    self.elog.textCursor().insertHtml('<span style="color:#FF0000">Error: '+str(e)+'</span><br>')
                    

                    print str(e)
            else:
                print 'workbook hava not been selected.'

        except AttributeError:
            print 'No active/valid workbook for script setting.'
    
    def setItem(self, col, row, val):
        try:
            self.tableHandle.setItem(col, row, QTableWidgetItem(str(val)))
        except Exception, e:
            print str(e)       
            
    def view(self, text):
        self.elog.moveCursor(QTextCursor.End)
        self.elog.textCursor().insertHtml('<span style="color:#FFFFFF">'+text+'</span><br>')

class Highlighter( QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
 
        keywordFormat =  QTextCharFormat()
        keywordFormat.setForeground( Qt.darkBlue)
        keywordFormat.setFontWeight( QFont.Bold)
 
        keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
                "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
                "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                "\\bvolatile\\b"]
 
        self.highlightingRules = [( QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]
 
        classFormat =  QTextCharFormat()
        classFormat.setFontWeight( QFont.Bold)
        classFormat.setForeground( Qt.darkMagenta)
        self.highlightingRules.append(( QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))
 
        singleLineCommentFormat =  QTextCharFormat()
        singleLineCommentFormat.setForeground( Qt.red)
        self.highlightingRules.append(( QRegExp("//[^\n]*"),
                singleLineCommentFormat))
 
        self.multiLineCommentFormat =  QTextCharFormat()
        self.multiLineCommentFormat.setForeground( Qt.red)
 
        quotationFormat =  QTextCharFormat()
        quotationFormat.setForeground( Qt.darkGreen)
        self.highlightingRules.append(( QRegExp("\".*\""),
                quotationFormat))
 
        functionFormat =  QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground( Qt.blue)
        self.highlightingRules.append(( QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))
 
        self.commentStartExpression =  QRegExp("/\\*")
        self.commentEndExpression =  QRegExp("\\*/")
 
    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression =  QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
 
        self.setCurrentBlockState(0)
 
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)
 
        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)
 
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = text.length() - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()
 
            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()    
    app.exec_()
    sys.exit
