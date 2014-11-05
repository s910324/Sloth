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
        
        self.filePathLabel = QLabel('File Path:')
        self.fileFullPath  = QLineEdit()
        self.reSelectFile  = QPushButton('Browse')
        self.fileHeaderLabel = QLabel('Header Size: ')
        self.fileHeaderSlider = QSlider(Qt.Horizontal)
        self.fileHeaderSizer = QLCDNumber(3)
        self.tempViewTable = QTableWidget()
        self.csvFileType   = QRadioButton('CSV Format')
        self.asciiFileType  = QRadioButton('ASCII Format')
        self.excelFileType  = QRadioButton('Excel Format')
        self.hLine           = QFrame()
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
        self.csvFileType.setChecked(True)
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
        tableViewLayout.addWidget(self.tempViewTable)
        headerSizeLayout.addWidget(self.fileHeaderLabel)
        headerSizeLayout.addSpacing(5)
        headerSizeLayout.addWidget(self.fileHeaderSlider)
        headerSizeLayout.addSpacing(15)
        headerSizeLayout.addWidget(self.fileHeaderSizer)

        typeSelectLayout.addWidget(self.csvFileType)
        typeSelectLayout.addWidget(self.asciiFileType)
        typeSelectLayout.addWidget(self.excelFileType)
        hLineLayout.addWidget(self.hLine)
        finishLayout.addStretch()
        finishLayout.addWidget(self.finishOperation)
        finishLayout.addSpacing(40)
        finishLayout.addWidget(self.cancleOperation)
        finishLayout.addStretch()
        
        self.setLayout(vQLayout)
        self.show()
        
    def OpenFile(self):
        ReadFileArray = []
        self.FileName      = QFileDialog.getOpenFileName(self, "Open File.", "/home")
        self.fileFullPath.setText(self.FileName[0])
        if len(self.FileName[0]) != 0:
            FileContainer = open(self.FileName[0], 'r')
            FileLines     = FileContainer.readlines()
                 
                
            RowNum = 25 if len(FileLines) >= 25 else len(FileLines)
            ColNum        = 0
            headerSize   = self.fileHeaderSlider.value()
            for i in range(RowNum):
                FileRow = (FileLines[i].strip()).split('\t')
                ReadFileArray.append(FileRow)
                if len(FileRow) > ColNum:
                    ColNum = len(FileRow)
                    
            ColNum = 6 if ColNum >=6 else ColNum  
            self.tempViewTable.setRowCount(RowNum)
            self.tempViewTable.setColumnCount(ColNum)
            
            for i in range(headerSize):  #header size
                for j in range(ColNum):
                    if j < len(ReadFileArray[i]):
                        headerItem = QTableWidgetItem(ReadFileArray[i][j])
                        headerItem.setFlags(headerItem.flags() != Qt.ItemIsEditable)
                    else:
                        headerItem = QTableWidgetItem('')
                        headerItem.setFlags(headerItem.flags() != Qt.ItemIsEditable)
                    headerItem.setBackground(QColor('#0066cc'))
                    headerItem.setForeground(QColor('#888888'))
                    self.tempViewTable.setItem(i, j, headerItem)
            for i in range(headerSize, RowNum):
                for j in range(len(ReadFileArray[i])):
                    contnent =  QTableWidgetItem(ReadFileArray[i][j])
                    contnent.setFlags(contnent.flags() != Qt.ItemIsEditable)
                    self.tempViewTable.setItem(i, j, contnent)
            FileContainer.close()


    def SilderChanged(self):
        RowNum = self.tempViewTable.rowCount() 
        ColNum = self.tempViewTable.columnCount()
        val = self.fileHeaderSlider.value()
        if RowNum != 0 and ColNum != 0:
            for j in range(ColNum):
                for i in range(val):
                    headerItem = QTableWidgetItem(self.tempViewTable.item(i, j).text())
                    headerItem.setFlags(headerItem.flags() != Qt.ItemIsEditable)
                    headerItem.setBackground(QColor('#0066cc'))
                    headerItem.setForeground(QColor('#888888'))
                    self.tempViewTable.setItem(i, j, headerItem)
                for i in range(val, 10, 1):
                    nonHeaderItem = QTableWidgetItem(self.tempViewTable.item(i, j).text())
                    nonHeaderItem.setFlags(nonHeaderItem.flags() != Qt.ItemIsEditable)
                    nonHeaderItem.setBackground(QColor('#ffffff'))
                    nonHeaderItem.setForeground(QColor('#888888'))
                    self.tempViewTable.setItem(i, j, nonHeaderItem)
        
    def Submit(self):
        try:
            if len(self.FileName[0]) != 0:
                self.accept()
                return self.FileName[0], self.fileHeaderSlider.value()
        except AttributeError:
            print 'No valid file selected.'
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = PreView()
    form.exec_()
    sys.exit(app.exec_())