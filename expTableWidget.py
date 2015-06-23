#!/usr/bin/env python

import sys
from PySide.QtCore import *
from PySide.QtGui import *
import os
# class Form(QDialog):

#     def __init__(self, parent=None):
#         super(Form, self).__init__(parent)
#         tableLabel = QLabel("Behold, some data, in a table:")
#         self.setGeometry(300, 300, 820, 820)
#         self.customTable = TableWidgetCustom()
#         self.customTable.setEditTriggers(QTableWidget.NoEditTriggers)
#         self.customTable.setSelectionBehavior(QTableWidget.SelectItems)
#         self.customTable.setSelectionMode(QTableWidget.ExtendedSelection)
#         layout = QVBoxLayout()
#         layout.addWidget(tableLabel)
#         layout.addWidget(self.customTable)
#         self.setLayout(layout)
#         self.setWindowTitle("QTableWidget Copy and Paste Example")
#         self.customTable.setColumnCount(15)
#         self.customTable.setRowCount(15)
#         for row in range(15):
#             for col in range(15):
#                 item = QTableWidgetItem("Row %d Column %d" % (row+1,
#                                                              col+1))
#                 self.customTable.setItem(row, col, item)
                
class TableWidgetCustom(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy()
        elif event.matches(QKeySequence.Paste):
            self.paste()
        elif event.matches(QKeySequence.Delete):
            self.delete()
        else:
            QTableWidget.keyPressEvent(self, event)

    def copy(self):
        self.tableHandle = self
        selectIdx = []
        if len(self.tableHandle.selectedRanges()) != 0:
            for i in range( len( self.tableHandle.selectedRanges())):
                leftCol  = self.tableHandle.selectedRanges()[i].leftColumn()
                colCount = self.tableHandle.selectedRanges()[i].columnCount()
                topRow   = self.tableHandle.selectedRanges()[i].topRow()
                rowCount = self.tableHandle.selectedRanges()[i].rowCount()
                for currentCol in range( leftCol, leftCol + colCount ):
                    row = []
                    selectIdx.append([ currentCol, row ])
                    for currentRow in range( topRow, topRow + rowCount ):
                        row.append(currentRow )                    


        for i in range(len(selectIdx)):
            for j in range( i+1, len(selectIdx), 1):
                try:
                    if selectIdx[i][0] == selectIdx[j][0]:
                        selectIdx[i][1].extend(selectIdx[j][1])
                        selectIdx[j].pop(0)
                        selectIdx[j].pop(0)
                except IndexError:
                    print 'item({0},{1}) not exist.'.format(i, j)
        copycheck = True
        
        selectIdx =  filter(None, selectIdx)
        
        for i in range(len(selectIdx)-1):
            if len(selectIdx[i][1]) != len(selectIdx[i+1][1]):
                copycheck =False
                print 'alert'
                break
        
        if copycheck == True:
            selectIdx.sort()
            for i in range(len(selectIdx)):
                selectIdx[i][1].sort()
    
            print selectIdx
            copyText = ''
            for col in selectIdx:
                for row in col[1]:
                    item = self.item(row, col[0])
                    if item:
                        copyText += item.text()
                    copyText += '\t'
                copyText += '\n'
            QApplication.clipboard().setText(copyText)
            print 'copied text: ' + copyText


    def paste(self):
        pasteAry = []
        self.tableHandle = self
        [ currCol, currRow ]= [self.tableHandle.currentColumn(), self.tableHandle.currentRow()]
        for i in QApplication.clipboard().text().strip().split('\n'):
            pasteAry.append(i.strip().split('\t'))
        RowNum = 0
        ColNum =len(pasteAry)
        if currCol + currRow != -2:
            for i in range(len(pasteAry)):
                RowNum = len(pasteAry[i]) if RowNum < len(pasteAry[i]) else RowNum
                for j in range(len(pasteAry[i])):
                    self.tableHandle.setItem( currRow + j, currCol + i,  QTableWidgetItem(pasteAry[i][j]))
        self.setRangeSelected(QTableWidgetSelectionRange(currRow, currCol, currRow + RowNum -1, currCol + ColNum -1), True)

        
        '''still need to expand table if array is too big fo it'''

    def delete(self):
        self.tableHandle = self
        selectIdx = []
        if len(self.tableHandle.selectedRanges()) != 0:
            for i in range( len( self.tableHandle.selectedRanges())):
                leftCol  = self.tableHandle.selectedRanges()[i].leftColumn()
                colCount = self.tableHandle.selectedRanges()[i].columnCount()
                topRow   = self.tableHandle.selectedRanges()[i].topRow()
                rowCount = self.tableHandle.selectedRanges()[i].rowCount()
                for currentCol in range( leftCol, leftCol + colCount ):
                    row = []
                    selectIdx.append([ currentCol, row ])
                    for currentRow in range( topRow, topRow + rowCount ):
                        row.append(currentRow )
        for i in selectIdx:
            col = i[0]
            for row in i[1]:
                self.setItem(row, col, QTableWidgetItem(''))
        
# app = QApplication(sys.argv)
# form = Form()
# form.show()
# app.exec_()