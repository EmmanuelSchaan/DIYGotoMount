# did not work for me
# probably needs python 3
'''
from guizero import App

app = App(title="Goto Mount Controller")
app.display()
'''



##############################################33
# PyQt5
# did not work for me: probably needs python 3
'''
#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import ( QMainWindow, QApplication, QPushButton,
QWidget, QAction, QTabWidget,QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt5 Tab Example')
        self.setGeometry(100, 100, 640, 300)
        self.setCentralWidget(MyTabWidget(self))
        self.show()
 
class MyTabWidget(QTabWidget):
 
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
 
        # Enable the ability to move tabs and reorganize them, as well
        # as close them. Setting tabs as closable displays a close button
        # on each tab.
        #
        self.setTabsClosable(True)
        self.setMovable(True)
 
        # Create tabs in tab container
        #
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
 
        # Add tabs
        #
        self.addTab(self.tab1,"Tab 1")
        self.addTab(self.tab2,"Tab 2")
        self.addTab(self.tab3,"Long Tab 3")
        self.addTab(self.tab4,"Longer Tab 4")
        self.addTab(self.tab5,"Longest Tab 5")
        self.currentChanged.connect(self.tabSelected)
        self.tabCloseRequested.connect(self.closeRequest)
 
        # Add test content to a few tabs
        #
        self.tab1.setLayout(QVBoxLayout(self))
        self.tab2.setLayout(QVBoxLayout(self))
        self.pushButton1 = QPushButton("PyQt5 Button 1")
        self.tab1.layout().addWidget(self.pushButton1)
        self.pushButton2 = QPushButton("PyQt5 Button 2")
        self.tab2.layout().addWidget(self.pushButton2)
 
    #@pyqtSlot()
    def tabSelected(self):
        print("Selected tab {0}".format(self.currentIndex()+1))
 
    def closeRequest(self):
        print("Tab close request on tab {0}".format(self.currentIndex()+1))
        if self.count() > 1:
            self.removeTab(self.currentIndex())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
'''

##############################################33
# PyQt4: works
'''
import sys
from PyQt4.QtGui import *

from PyQt4.QtCore import QT_VERSION_STR
from PyQt4.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR

a = QApplication(sys.argv)       

w = QWidget()
w.resize(320, 240)
w.setWindowTitle("Goto Mount Controller") 

label = QLabel()
#info = "Qt version:" + QT_VERSION_STR + \
#       "\nSIP version:" + SIP_VERSION_STR + \
#       "\nPyQt version:" + PYQT_VERSION_STR
info = "C'est parti !"
label.setText(info)

hbox = QHBoxLayout()
hbox.addWidget(label)
w.setLayout(hbox)

w.show() 
 
sys.exit(a.exec_())
'''

##############################################33
#

import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):

   def __init__(self):
      super(Window, self).__init__()
      self.setGeometry(50, 50, 500, 500)
      self.setWindowTitle("Goto Mount Controller")
      self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
      self.home()

   def home(self):

      # Quit button 
      self.btn = QtGui.QPushButton("Quit", self)
      self.btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
      self.btn.resize(100,100)
      self.btn.move(300,400)

      # tracking toggle button
      self.btnTracking = QtGui.QPushButton("Tracking ON", self)
      self.btnTracking.setCheckable(True)
      self.btnTracking.setStyleSheet("background-color : lightgreen")
      self.btnTracking.clicked.connect(self.toggleTracking)
      self.btnTracking.resize(100,100)
      self.btnTracking.move(100,400)

      # RA minus
      self.btnRaMinus = QtGui.QPushButton("RA-", self)
      self.btnRaMinus.clicked.connect(self.decreaseRa)
      self.btnRaMinus.resize(100,100)
      self.btnRaMinus.move(100,100)

      # RA plus
      self.btnRaPlus = QtGui.QPushButton("RA+", self)
      self.btnRaPlus.clicked.connect(self.increaseRa)
      self.btnRaPlus.resize(100,100)
      self.btnRaPlus.move(300,100)

      # Dec minus
      self.btnDecMinus = QtGui.QPushButton("Dec-", self)
      self.btnDecMinus.clicked.connect(self.decreaseDec)
      self.btnDecMinus.resize(100,100)
      self.btnDecMinus.move(200,200)

      # Dec plus
      self.btnDecPlus = QtGui.QPushButton("Dec+", self)
      self.btnDecPlus.clicked.connect(self.increaseDec)
      self.btnDecPlus.resize(100,100)
      self.btnDecPlus.move(200,0)

      # Stop
      self.btnStop = QtGui.QPushButton("Stop", self)
      self.btnStop.clicked.connect(self.stop)
      self.btnStop.resize(100,100)
      self.btnStop.move(200,100)

      # Current RA
      self.txtRa = QtGui.QLineEdit("RA", self)
      self.txtRa.resize(100,40)
      self.txtRa.move(0, 0)

      # Current Dec
      self.txtDec = QtGui.QLineEdit("Dec", self)
      self.txtDec.resize(100,40)
      self.txtDec.move(0, 45)

      self.update()
      self.show()

   def toggleTracking(self):
        if self.btnTracking.isChecked(): 
            # setting background color to light-blue 
            self.btnTracking.setStyleSheet("background-color : red") 
            self.btnTracking.setText("Tracking OFF")
        else: 
            # set background color back to light-grey 
            self.btnTracking.setStyleSheet("background-color : lightgreen")
            self.btnTracking.setText("Tracking ON")

   def increaseRa(self):
      '''Set positive speed target for RA
      '''
      pass
   
   def decreaseRa(self):
      '''Set negative speed target for RA
      '''
      pass

   def increaseDec(self):
      '''Set positive speed target for Dec
      '''
      pass
   
   def decreaseDec(self):
      '''Set negative speed target for Dec
      '''
      pass

   def stop(self):
      '''Halts the motors, interrupt or not the tracking
      '''
      pass
        
def run():
   app = QtGui.QApplication(sys.argv)
   GUI = Window()
   sys.exit(app.exec_())

run()
