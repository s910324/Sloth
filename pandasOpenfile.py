#-*- coding: utf-8 -*-
import sys
import NightlyBuild as Main
import pandas as pd
from PySide.QtCore import *
from PySide.QtGui  import *
# from QtVariant import QtGui, QtCore
#from PyQt4.QtCore import *
#from PyQt4.QtGui  import *


class PreView(QDialog):
    def __init__(self, parent=None):
        super(PreView, self).__init__(parent)
        self.tabHolderArray = []
        self.setWindowTitle('Open File Options' )
        self.resize(680,500)
        self.initUI()
        
        
    def initUI(self):
        vQLayout = QVBoxLayout()
        fileNameLayout   = QHBoxLayout()
        tableViewLayout  = QHBoxLayout()
        headerSizeLayout = QHBoxLayout()
        typeSelectLayout = QHBoxLayout()
        hLineLayout      = QHBoxLayout()
        finishLayout     = QHBoxLayout()
        
        self.mainTab          = QTabWidget()
        self.filePathLabel    = QLabel('File Path:')
        self.fileFullPath     = QLineEdit()
        self.reSelectFile     = QPushButton('Browse')
        self.fileHeaderLabel  = QLabel('Header Size: ')
        self.fileHeaderSlider = QSlider(Qt.Horizontal)
        self.fileHeaderSizer  = QLCDNumber(3)
        self.tempViewTable    = QTableWidget()
        self.asciiFileType    = QRadioButton('ASCII Format')
        self.csvFileType      = QRadioButton('CSV Format')
        self.excelFileType    = QRadioButton('Excel Format')
        self.hdf5FileType     = QRadioButton('HDF5 Format')
        self.hLine            = QFrame()
        self.finishOperation  = QPushButton('Ok')
        self.cancleOperation  = QPushButton('Cancle')
        
        
        self.reSelectFile.clicked.connect(self.OpenFile)
        self.fileHeaderSlider.valueChanged.connect(self.fileHeaderSizer.display)
        self.fileHeaderSlider.valueChanged.connect(self.SilderChanged)
        self.finishOperation.clicked.connect(self.Submit)
        self.cancleOperation.clicked.connect(self.close)

        self.fileHeaderLabel.setMinimumWidth(80)
        self.fileHeaderSizer.setMinimumWidth(80)
        self.fileHeaderSizer.setMinimumHeight(25)
        
        self.fileHeaderSlider.setTickInterval(1)
        self.fileHeaderSlider.TickPosition(QSlider.TicksBothSides)
        self.fileHeaderSlider.setRange(0, 10)
        self.fileHeaderSlider.setValue(3)
        self.hLine.setFrameShape(QFrame.HLine)
        self.hLine.setFrameShadow(QFrame.Raised)
        
        vQLayout.addLayout(fileNameLayout)
        vQLayout.addSpacing(5)
        vQLayout.addLayout(tableViewLayout)
        vQLayout.addSpacing(20)
        vQLayout.addLayout(headerSizeLayout)        
        vQLayout.addSpacing(15) 
        vQLayout.addLayout(typeSelectLayout)        
        vQLayout.addSpacing(35)
        vQLayout.addLayout(hLineLayout)
        vQLayout.addSpacing(5)
        vQLayout.addLayout(finishLayout)
        vQLayout.addSpacing(5)
        
        
        fileNameLayout.addWidget(self.filePathLabel)
        fileNameLayout.addWidget(self.fileFullPath)
        fileNameLayout.addWidget(self.reSelectFile)
        tableViewLayout.addWidget(self.mainTab)
        headerSizeLayout.addWidget(self.fileHeaderLabel)
        headerSizeLayout.addSpacing(5)
        headerSizeLayout.addWidget(self.fileHeaderSlider)
        headerSizeLayout.addSpacing(15)
        headerSizeLayout.addWidget(self.fileHeaderSizer)
        
        typeSelectLayout.addWidget(self.asciiFileType)
        typeSelectLayout.addWidget(self.csvFileType)
        typeSelectLayout.addWidget(self.excelFileType)
        typeSelectLayout.addWidget(self.hdf5FileType)
        hLineLayout.addWidget(self.hLine)
        finishLayout.addStretch()
        finishLayout.addWidget(self.finishOperation)
        finishLayout.addSpacing(40)
        finishLayout.addWidget(self.cancleOperation)
        finishLayout.addStretch()
        
        self.setLayout(vQLayout)
        self.show()
        
    def OpenFile(self):
        fileName      = QFileDialog.getOpenFileName(self, "Open File.", "/home")
        self.fullPath = fileName[0]
        self.fileFullPath.setText(self.fullPath)
        self.fileContainArray = []
        if len(self.fullPath) != 0:
            extName = self.fullPath.split('.')[-1]
            
            if   extName in 'asc, dat, txt':
                self.asciiFileType.setChecked(True)
                fileContainer = pd.read_table(self.fullPath, header = None)
                self.mainTab.clear()
                tabHolder = self.addNewTab(fileContainer)
                self.tabHolderArray.append(tabHolder)
                self.fileContainArray.append(fileContainer)
            elif extName in 'csv':
                self.csvFileType.setChecked  (True)
                fileContainer = pd.read_csv  (self.fullPath, header = None)
                self.mainTab.clear()
                tabHolder = self.addNewTab(fileContainer)
                self.tabHolderArray.append(tabHolder)
                self.fileContainArray.append(fileContainer)
            elif extName in 'xls, xlsx':
                self.excelFileType.setChecked(True)
                self.mainTab.clear()
                xl = pd.ExcelFile(self.fullPath)
                for names in xl.sheet_names:
                    fileContainer = pd.read_excel(self.fullPath, names, header = None)
                    tabHolder = self.addNewTab(fileContainer, tabName =  unicode(str(names)))
                    self.tabHolderArray.append(tabHolder)
                    self.fileContainArray.append(fileContainer)
            elif extName in 'h5, hdf5, he5, hdf, h4, hdf4, he2':
                self.hdf5FileType.setChecked (True)
                print 'not yet complete.'
#
#                fileContainer = pd.read_hdf  (self.fullPath, 'detector/readout')
#                fileContainer.to_csv( self.fullPath + '.csv')
#                fileContainer = pd.read_csv  (self.fullPath + '.csv', header = None)
#                self.mainTab.clear()
#                tabHolder = self.addNewTab(fileContainer)
#                self.tabHolderArray.append(tabHolder)
                
            else:
                self.asciiFileType.setChecked(True)
                fileContainer = pd.read_table(self.fullPath, header = None)
                self.mainTab.clear()
                tabHolder = self.addNewTab(fileContainer)
                self.tabHolderArray.append(tabHolder)
                self.fileContainArray.append(fileContainer)
        
        
    def addNewTab(self, fileContainer, tabName = 'Default'):
        tempViewTable = QTableWidget()
        self.mainTab.addTab(tempViewTable, tabName)
        headerSize   = self.fileHeaderSlider.value()
        (rowNum, colNum) = fileContainer.shape
            
        showRowNum = 40 if rowNum >=40 else rowNum
        showColNum = 20 if colNum >=20 else colNum

        tempViewTable.setRowCount   (showRowNum)
        tempViewTable.setColumnCount(showColNum)

        for col in range(showColNum):
            for row in range(showRowNum):
                try:
                    contnent =  QTableWidgetItem(unicode(str(fileContainer[col][row])))
                except UnicodeEncodeError:
                    contnent =  QTableWidgetItem(unicode(fileContainer[col][row]))
                contnent.setFlags(contnent.flags() != Qt.ItemIsEditable)
                if row < headerSize:
                    contnent.setBackground(QColor('#0066cc'))
                    contnent.setForeground(QColor('#888888'))
                tempViewTable.setItem(row, col, contnent)
                    
        return tempViewTable    
            
    
    def SilderChanged(self, tabHolderArray):
        val = self.fileHeaderSlider.value()
        for tabHolders in self.tabHolderArray:
            rowNum   = tabHolders.rowCount() 
            colNum   = tabHolders.columnCount()
            if rowNum != 0 and colNum != 0:
                for j in range(colNum):
                    for i in range(rowNum):
                        contnent = QTableWidgetItem(tabHolders.item(i, j).text())
                        contnent.setFlags(contnent.flags() != Qt.ItemIsEditable)
                        if i < val:
                            contnent.setBackground(QColor('#0066cc'))
                            contnent.setForeground(QColor('#888888'))
                        else:
                            contnent.setBackground(QColor('#ffffff'))
                            contnent.setForeground(QColor('#888888'))
                        tabHolders.setItem(i, j, contnent)                    
    
    def SelectTypeChanged(self):
        print 'a'    
        
    def Submit(self):
        try:
            if self.fullPath != 0 and len(self.fullPath) != 0:
                self.accept()
                return self.fullPath, self.fileContainArray, self.fileHeaderSlider.value()
            else:
                return 0,0,0
        except AttributeError:
            print 'No valid file selected.'

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = PreView()
    form.exec_()
    sys.exit(app.exec_())



    
    
    
