# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 17:50:28 2018

A Forest keeps track of all of trees contained within some rows x cols grid
under some predefined biological-enviornment parameters defined in config.py

@author: Quentin Goehrig
""" 

from forest import Forest
from PyQt5.QtCore import QDateTime, Qt, QTimer, QRect, QRectF, QPoint, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QGraphicsScene, QGraphicsView, QMainWindow)
from PyQt5.QtGui import QPen, QBrush, QColor


class ForestViewer(QMainWindow):
    resized = pyqtSignal()
    def  __init__(self, forest, parent=None):
        super(ForestViewer, self).__init__(parent=parent)
        self.forest = forest
        self.widgetGallery = WidgetGallery( self.forest )
        #self.createDockerWidget()
        self.resized.connect(self.handleResize)
        self.setCentralWidget( self.widgetGallery)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(ForestViewer, self).resizeEvent(event)

    def handleResize(self):
        self.widgetGallery.tester()#.getSceneRect()
    

class WidgetGallery(QDialog):
    def __init__(self, forest, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.setContentsMargins(1,1,1,1)
        self.forest = forest
        self.originalPalette = QApplication.palette()
        self.resize(800, 600)
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createForestView()
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.forest_view, 0, 0)
        self.mainLayout.addWidget(self.bottomRightGroupBox, 0, 1)
        self.mainLayout.addWidget(self.progressBar, 1, 0, 1, 2)
        #mainLayout.setRowStretch(0, 1)
        #mainLayout.setRowStretch(0, 1)
        self.mainLayout.setColumnStretch(0, 5)
        self.mainLayout.setColumnStretch(1, 2)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Chestnut Blight Forest Simulator")
        self.changeStyle('Fusion')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createForestView(self):
        forest_scene = QGraphicsScene() #init size?
#        forest_scene.setBackgroundBrush(QBrush(QColor("blue")))
        self.forest_view = QGraphicsView(forest_scene)
#        self.forest_view.setContentsMargins(5,5,5,5)
        self.forest_view.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #self.forest_view.setGeometry(1,1,1,1)
        if self.forest != None:
            self.paintGrid()


    def paintGrid(self):
        grid = self.forest
        if grid == None:
            print("Return Text('No Forest')")
            return
        view = self.forest_view
        scene = view.scene()
        size = view.size()
#        w = (size.width())
#        h = (size.height())
        rect = scene.itemsBoundingRect()
        w = float(view.contentsRect().width())
        h = float(view.contentsRect().height())
        print(rect)
        print(view.contentsRect())
        print(view.childrenRect())
#        w = rect.width()
#        h = rect.height()
#        w = w if w > rect.width() else rect.width()
#        h = h if h > rect.height() else rect.height()
        
        view.setSceneRect(0, 0, w, h);
        drect = QRectF(0, 0, w, h)
        scene.clear()
        scene.addRect(drect, QPen(), QBrush(QColor("blue")))
#        view.setSceneRect(0,0,w,h)
#        scene.setSceneRect(0,0,w,h)
#        view.setGeometry(0, 0, w, h)
#        view.setGeometry(0, 0, w, h)
        
        cell_w = w / grid.cols
        cell_h = h / grid.rows
#        if cell_w < cell_h:
#            cell_h = cell_w
#        else:
#            cell_w = cell_h
        scene.clear()
        for r in range(grid.rows):
            for c in range(grid.cols):
                rect = QRectF(c * cell_w, r * cell_h, cell_w, cell_h)
                brush = QBrush(QColor("white"))
                scene.addRect(rect, QPen(), brush)
                
    def paintTrees(self):
        print("teee")
    
    
    # Scene work
    def tester(self):
        if(self.forest_view):
            self.paintGrid()#print(self.forest_view.size())
            #print(self.scene().size())

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Group 2")

        defaultPushButton = QPushButton("Default Push Button")
        defaultPushButton.setDefault(True)

        togglePushButton = QPushButton("Toggle Push Button")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)
        
        # okay move this here too
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")


    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    # Use this when debugging w/ IPython in Spyder IDE
    
    test_forest = Forest(30, 30)
    test_forest.init_random()
    gallery = ForestViewer( test_forest )
    gallery.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_()) 



























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