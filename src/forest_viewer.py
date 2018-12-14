# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:50:28 2018

A visualization for the Chestnut Blight fungus simulation.

@author: Quentin Goehrig
""" 

from forest import Forest
from PyQt5.QtCore import QRectF, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStyleFactory, 
        QGraphicsScene, QGraphicsView, QDialog, QGridLayout, QGroupBox, 
        QSpinBox, QCheckBox, QHBoxLayout, QLabel, QProgressBar,
        QPushButton, QSizePolicy, QFormLayout)

from PyQt5.QtGui import QPen, QBrush, QColor
import config

class ForestViewer(QMainWindow):
    def  __init__(self, forest, parent=None):
        super(ForestViewer, self).__init__(parent=parent)
        self.forest = forest
        self.ForestDialog = ForestDialog( self.forest )
        self.setCentralWidget( self.ForestDialog )
        self.setWindowTitle("Chestnut Blight Forest Simulator")
        QApplication.setStyle(QStyleFactory.create('Fusion'))

class ForestDialog(QDialog):
    resized = pyqtSignal()
    def __init__(self, forest=None, parent=None):
        super(ForestDialog, self).__init__(parent=parent)
        self.forest = forest
        self.resized.connect( self.handleResizeEvent )
        self.setContentsMargins(1,1,1,1)
        self.resize(1200,1000)

        self.createForestView()
        self.createForestControl()
        
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.forest_view_box, 0, 0)
        self.mainLayout.setRowStretch(0, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.addWidget(self.ForestControlBox, 0, 1)
        self.mainLayout.setColumnStretch(0, 5)
        self.mainLayout.setColumnStretch(1, 2)
        self.setLayout(self.mainLayout)

    def handleResizeEvent(self, event):
        self.resized.emit()
        return super(ForestDialog, self).resizeEvent(event)

    def handleResize(self):
        self.paintGrid()

    def createForestView(self):
        self.forest_view_box = QGroupBox("Forest View")
        forest_scene = QGraphicsScene() #init size?
        forest_scene.setBackgroundBrush(QColor("orange"))
        self.forest_view = QGraphicsView(forest_scene)
        self.forest_view_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout = QHBoxLayout(self)
        layout.addWidget(self.forest_view, 1)
        
        self.forest_view_box.setLayout(layout)
        if self.forest != None:
            self.paintGrid()


    def transition(self):
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


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)    
    test_forest = Forest(30, 30)
    test_forest.grid = test_forest.generate_grid()
    fv = ForestViewer( test_forest )
    fv.show()
    # Use this when debugging w/ IPython in Spyder IDE
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_()) 