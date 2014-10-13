import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from PySide.QtCore import *
from PySide.QtGui  import *



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        plotSym = [ 'o', 's', 't', 'd', '+' ]
        self.initSettingDocker()
        self.resize(850,650)
        self.tb = QToolBar('plot options')
        self.addToolBar( Qt.TopToolBarArea , self.tb)
        ######
        vb = CustomViewBox()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        ######
        self.view = pg.GraphicsLayoutWidget()         
        self.setCentralWidget(self.view)
        self.setWindowTitle('pyqtgraph example: ScatterPlot')
        self.w1 = self.view.addPlot(viewBox=vb, enableMenu=False, title="PlotItem with custom axis and ViewBox<br>Menu disabled, mouse behavior changed: left-drag to zoom, right-click to reset zoom")
        
        l = pg.LegendItem((100,60), offset=(70,70))  # args are (size, offset)
        l.setParentItem(self.w1.graphicsItem())   # Note we do NOT call plt.addItem in this case

        self.s1 = pg.ScatterPlotItem( name = 'sample', pxMode = True, antialias = True, size=8, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 0, 255), symbol = plotSym[2])
        self.s2 = pg.ScatterPlotItem( name = 'sample', pxMode = True, antialias = True, size=8, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 0, 255), symbol = plotSym[3])
        
        self.x = np.array([0,1,2,3,4,5])
        self.y = np.exp(self.x)
        self.z = self.x
        self.s1.addPoints(self.x,self.y)
        self.s2.addPoints(self.x, self.z)
        self.w1.addItem(self.s1)
        self.w1.addItem(self.s2)
        
        l.addItem(self.s1, 'red plot')
        l.addItem(self.s2, 'green plot')
        ######

        self.w1.setLabel(axis = 'left', text= 'y', units= 'a.u.', unitPrefix=None )
        self.w1.setLabel(axis = 'bottom', text= 'x', units= 'a.u.', unitPrefix=None )
        self.w1.setTitle(title='super awsome')
        
        self.w1.showAxis('top', show=True)
        self.w1.showAxis('right', show=True)
        ######
        '''crosshair'''
        


    
    def initSettingDocker(self):
        self.settingDockWidget = QDockWidget("  ::  Settings ::", self)
        self.settingDockWidget.setFeatures(QDockWidget.DockWidgetMovable)
        self.settingDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea and Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.settingDockWidget)
        self.settings = PlotSettings()
        self.settingDockWidget.setWidget(self.settings)

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)
        
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()
            
    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)   

        
                        
class PlotSettings(QWidget):
    def __init__(self, parent = None):
        super(PlotSettings, self).__init__(parent)
        XAxisLabel = QLabel()
        YAxisLabel = QLabel()
        XUnitLabel = QLabel()
        YUnitLabel = QLabel()
        XMaxLabel  = QLabel()
        YMaxLabel  = QLabel() 
        XMinLabel  = QLabel() 
        YMinLabel  = QLabel()
        
        XAxisText  = QLineEdit()       
        XUnitText  = QLineEdit()
        YAxisText  = QLineEdit()
        YUnitText  = QLineEdit()
        

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(XAxisText, 1,0)
        self.setLayout( grid )
        #self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()    
    app.exec_()
    sys.exit
