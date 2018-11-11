# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:50:28 2018

A Forest keeps track of all of trees contained within some rows x cols grid
under some predefined biological-enviornment parameters defined in config.py

@author: Quentin Goehrig
""" 

from forest import Forest
from PyQt5.QtCore import QRectF, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QGraphicsScene, QGraphicsView, QMainWindow,
        QFormLayout, QLayout)
from PyQt5.QtGui import QPen, QBrush, QColor
import config
import time

class ForestViewer(QMainWindow):
    resized = pyqtSignal()
    def  __init__(self, forest, parent=None):
        super(ForestViewer, self).__init__(parent=parent)
        self.forest = forest
        self.ForestDialog = ForestDialog( self.forest ) #or docker widget?
        self.resized.connect( self.handleResize )
        self.setCentralWidget( self.ForestDialog )
        self.setWindowTitle("Chestnut Blight Forest Simulator")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
#        QApplication.setPalette(QApplication.palette())

    def resizeEvent(self, event):
        self.resized.emit()
        return super(ForestViewer, self).resizeEvent(event)

    def handleResize(self):
        self.ForestDialog.tester()

class ForestDialog(QDialog):
    resized2 = pyqtSignal()
    def __init__(self, forest=None, parent=None):
        super(ForestDialog, self).__init__(parent=parent)
        self.forest = forest
        self.resized2.connect( self.dudemang )
        self.setContentsMargins(1,1,1,1)
        self.resize(1200,1000)

        self.createForestView()
        self.createForestControl()
        
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.forest_view_box, 0, 0)
        self.mainLayout.setRowStretch(0, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.addWidget(self.ForestControlBox, 0, 1)
        #mainLayout.setRowStretch(0, 1)
        #mainLayout.setRowStretch(0, 1)
        self.mainLayout.setColumnStretch(0, 5)
        self.mainLayout.setColumnStretch(1, 2)
        self.setLayout(self.mainLayout)

    def resizeEvent(self, event):
        self.resized2.emit()
        return super(ForestDialog, self).resizeEvent(event)

    def dudemang(self):
        self.paintGrid()

    def createForestView(self):
        
        self.forest_view_box = QGroupBox("Forest View")
        forest_scene = QGraphicsScene() #init size?
        forest_scene.setBackgroundBrush(QColor("orange"))
        self.forest_view = QGraphicsView(forest_scene)
#        self.forest_view.setBackgroundBrush(QBrush(QColor("blue")))
#        self.forest_view.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.forest_view_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #size policy for box?
        layout = QHBoxLayout(self)
        layout.addWidget(self.forest_view, 1)
        
        self.forest_view_box.setLayout(layout)
        if self.forest != None:
            self.paintGrid()


    def transition(self):
        print("hello transition!")
        self.forest.set_next_year()
        self.paintGrid()

            
    def createForestControl(self):

        self.ForestControlBox = QGroupBox("Forest Control")
        
        years_to_sim = QSpinBox(self.ForestControlBox)
        years_to_sim.setValue(50)
        
        update_delay = QSpinBox(self.ForestControlBox)
        update_delay.setValue(0)
        forest = self.forest

        button = QPushButton("Next Year")
        button.pressed.connect(self.transition)
        
        layout = QFormLayout()
        layout.addRow(QLabel("Forest Size: " + str(forest.rows) + " x " + str(forest.cols)))
        layout.addRow(QLabel("Years to Simulate:"), years_to_sim)
        layout.addRow(QLabel("Update Delay (seconds):"), update_delay)
        layout.addRow(button)


        self.ForestControlBox.setLayout(layout)

    def paintGrid(self):
        forest = self.forest
        if forest == None:
            print("Return Text('No Forest')")
            return
        view = self.forest_view
        scene = view.scene()
        contents = view.contentsRect()
        w = float(contents.width())
        h = float(contents.height()) #view.childrenRect()

        view.setSceneRect(0, 0, w, h)
        scene.clear()
        
        cell_w = w / forest.cols
        cell_h = h / forest.rows
        
        rad = min(cell_w, cell_h)
        grid = forest.grid
        print("----------------------------------------------")
        forest.print_forest()

        for r in range(forest.rows):
            for c in range(forest.cols):
                #TODO: Maybe redraw with lines?
                x = c * cell_w
                y = r * cell_h
                rect = QRectF(x, y, cell_w, cell_h)
                bg_col = QColor("#EDEDED")
                off_white = QColor("#E8E8E8")
                trans = QColor("transparent")
                scene.addRect(rect, QPen(bg_col), QBrush(off_white))
                tree = grid[r][c]
                if tree != None and tree.stage != config.DEAD:
                    qcol = self.colorFromTree(tree)
                    # define circle radius based on tree stage
                    mrad = tree.stage * 0.24 * rad
                    xe = x + ((cell_w - mrad) / 2)
                    ye = y + ((cell_h - mrad) / 2)
                    scene.addEllipse(xe, ye, mrad, mrad, QPen(trans), QBrush(qcol))
                
    #TODO: Decide if split paint needed         
    def paintTrees(self):
        print("teee")
    
    def colorFromTree(self, tree):
        col = "transparent"
        if tree != None:
            col_switch = {
                config.V: "red",
                config.HV: "turquoise",
                config.HEALTHY: "green"
            }
            col = col_switch.get(tree.rating)
        return QColor(col)
        
    # Scene work
    def tester(self):
        if(self.forest_view):
            self.paintGrid()#print(self.forest_view.size())
            #print(self.scene().size())   


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)    
    test_forest = Forest(10, 10)
    test_forest.init_random()
    gallery = ForestViewer( test_forest )
    gallery.show()
    # Use this when debugging w/ IPython in Spyder IDE
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_()) 









#def advanceProgressBar(self):
#    curVal = self.progressBar.value()
#    maxVal = self.progressBar.maximum()
#    self.progressBar.setValue(curVal + (maxVal - curVal) / 100)
#
#
#def createProgressBar(self):
#    self.progressBar = QProgressBar()
#    self.progressBar.setRange(0, 10000)
#    self.progressBar.setValue(0)
#
#    timer = QTimer(self)
#    timer.timeout.connect(self.advanceProgressBar)
#    timer.start(1000)

## -*- coding: utf-8 -*-
#"""
#Created on Mon Oct 29 16:28:42 2018
#
#@author: Quentin Goehrig
#"""
#
#from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtCore import QDateTime, Qt, QTimer, QRect, QRectF, QPoint
#from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
#        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
#        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
#        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
#        QVBoxLayout, QWidget, QMenuBar, QAction, QMainWindow, 
#        QGraphicsGridLayout, QGraphicsScene, QGraphicsView)
#from PyQt5.QtGui import QPen, QBrush, QColor
#from forest import Forest
#
#
#class ForestViewer(QtWidgets.QMainWindow):
#    resized = QtCore.pyqtSignal()
#    def  __init__(self, forest, parent=None):
#        super(ForestViewer, self).__init__(parent=parent)
#        self.forest = forest
#        
#        #self.createDockerWidget()
#        
#        self.createForestView()
#        self.resized.connect(self.handleResize)
#
#
#    def resizeEvent(self, event):
#        self.resized.emit()
#        return super(FV_Window, self).resizeEvent(event)
#
#    def handleResize(self):
#        print("resize")
#    
#    def createForestView(self):
#        forest_scene = QGraphicsScene(self.home)
#        if self.forest == None:
#            print("no forest")
#            return None
#        cell_w = 10
#        cell_h = 10
#        grid = self.forest
#        for r in range(grid.rows):
#            for c in range(grid.cols):
#                rect = QRectF(c * cell_w, r * cell_h, cell_w, cell_h)
#                brush = QBrush(QColor("white"))
#                forest_scene.addRect(rect, QPen(), brush)        
#
#        self.forest_view = QGraphicsView(forest_scene)
#
#
#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    app.aboutToQuit.connect(app.deleteLater)
#    test_forest = Forest(10, 9)
#    test_forest.init_random()
#    fw = ForestViewer(test_forest )
#    fw.show()
#    sys.exit(app.exec_())
#    sys.quit()