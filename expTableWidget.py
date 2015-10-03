#!/usr/bin/env python

import sys
from PySide.QtCore import *
from PySide.QtGui import *
import os

class TableWidgetCustom(QTableWidget):
	def __init__(self, parent=None):
		super(TableWidgetCustom, self).__init__(parent)
		self.col_count = 0
		self.row_count = 0

	def addCol(self, num = 1):
		try:
			atoz      = '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'
			labelList = []
			for i in range(num):
				alfabat    = []
				currentCol = self.currentColumn()
				if currentCol == -1:
					currentCol = self.col_count - 1
					
				self.insertColumn(currentCol + 1)
				self.col_count += 1
	
				labling = ''
				root    = self.col_count
				while( root != 0):
					if root%26 != 0:
						alfabat.append(root%26)
						root = root/26
					else:
						alfabat.append(26)
						root = (root/26) -1
	
				for i in xrange(len(alfabat)):
					alfabat[i] = atoz[alfabat[i]]
				for i in xrange(len(alfabat)-1, -1, -1):
					labling += alfabat[i]

				headerLable = 'Y({0})'.format(labling)
				labelList.append(headerLable)
				self.setHorizontalHeaderItem(currentCol + 1, QTableWidgetItem(headerLable))
				for i in range(3):
					headerItem = QTableWidgetItem('')
					headerItem.setBackground(QColor('#0066cc'))
					headerItem.setForeground(QColor('#ffffff'))
					headerFont = QFont("Times", 8, QFont.Normal)
					headerItem.setFont(headerFont)
					self.setItem(i, currentCol + 1, headerItem)
			return  labelList
		except AttributeError:
			raise AttributeError
	

	def addRow(self):
		try:
			if self.currentRow() > 2:
				self.insertRow(tableHandle.currentRow())
				return self.currentRow()
		except AttributeError:
			raise AttributeError


	def rmvCol(self):
		try: 
			selectAry    = []
			for i in range( len(self.selectedRanges())):
				leftCol  = self.selectedRanges()[i].leftColumn()
				colCount = self.selectedRanges()[i].columnCount()
				for j in range( leftCol, leftCol + colCount ):
					selectAry.append( j )

			for i in range( len ( selectAry )):
				self.removeColumn(selectAry[i] - i)
				self.col_count -= 1
			return selectAry
		except AttributeError:
			raise AttributeError


	def rmvRow(self):
		try:
			selectAry    = []
			for i in range( len(self.selectedRanges())):
				topRow   = self.selectedRanges()[i].topRow()
				rowCount = self.selectedRanges()[i].rowCount()
				for j in range( topRow, topRow + rowCount ):
					selectAry.append( j )

			for i in range( len ( selectAry )):
				if (selectAry[i] - i) > 2:
					self.removeRow(selectAry[i] - i)
			return selectAry
					
		except AttributeError:
			raise AttributeError


	def setAxis(self, axis):
		axisAry          = [ 'X', 'Y', 'Z' ]
		try:
			selectAry    = []
			for i in xrange( len(self.selectedRanges())):
				leftCol  = self.selectedRanges()[i].leftColumn()
				colCount = self.selectedRanges()[i].columnCount()
				for j in xrange( leftCol, leftCol + colCount ):
					selectAry.append( j )
			for currentCol in selectAry:
				headerLable  = axisAry[axis]
				headerLable += str(self.horizontalHeaderItem(currentCol).text())[1:]
				self.setHorizontalHeaderItem(currentCol, QTableWidgetItem(headerLable))
		except AttributeError:
			raise AttributeError



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